"""
Unified File type.

Author: J. Cameron Cooper (jccooper@rice.edu)
Copyright (C) 2009 Rice University. All rights reserved.

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

# TODO: workflow

from Products.Archetypes import atapi
from Products.ATContentTypes.content.image import ATImage as BaseType
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from zope.interface import implements
from zope import event
from zope.app.event import objectevent
from OFS.CopySupport import CopyError
from zExceptions import BadRequest

from Products.UniFile.interfaces import IUnifiedFile
from Products.UniFile import unifileMessageFactory as _

schema = BaseType.schema.copy()
schema['image'].sizes = None

class UnifiedFile(BaseType):
    """File type that also handles Images; like a combined version of the
    traditional File and Image types.
    """
    implements(IUnifiedFile)

    portal_type = "UniFile"
    archetypes_name = "File"
    
    schema = schema
    
    mimetype = BaseType.getContentType

    def download(self):
        """Override of parent 'download' to make sure we set file attachment name,
        just in case the field gets confused.
        """
        # if data field is missing filename for whatever reason, update it
        # (such a case probably due to migration)
        # we cannot just set the header ourself; inside download (OFS.Image.index_html)
        # is a RESPONSE.write that writes to the browser before we can change the headers
        field = self.getPrimaryField()
        filename = field.getFilename(self)
        if not filename:
            field.setFilename(self, self.getId())

        return BaseType.download(self)

atapi.registerType(UnifiedFile)



## Zope CA views; see configure.zcml for wiring

# hard-coding is okay; browser support changes v. slowly and only these three have wide support
# see http://en.wikipedia.org/wiki/Comparison_of_web_browsers#Image_format_support
BROWSER_MIMETYPES = (
  'image/gif',
  'image/x-png',
  'image/png',
  'image/jpeg',
)

class UniFileBrowserView(BrowserView):
    """Foundation view class for UniFile."""
    def realParent(self):
        """Get containing object.
        Just getting the aq_parent doesn't really work in the case of FactoryTool,
        as it throws other crazy objects in the acquisition path. Look through the acquisition
        chain for the next real object.
        """
        ob = self.context.aq_parent
        while hasattr(ob, 'aq_parent') \
              and getattr(ob, 'meta_type', None) == None or ob.meta_type == self.context.meta_type:
            ob = ob.aq_parent
        return ob

class UniFileView(UniFileBrowserView):
    """View class for the UnifiedFile type handing data for template(s)."""
    def isNew(self):
        factorytool = getToolByName(self.context, 'portal_factory')
        return factorytool.isTemporary(self.context)
    
    def hasFile(self):
        return self.context.size() != 0
    
    def readableSize(self):
        return self.context.getObjSize(self.context)

    def content_type(self):
        return self.context.getContentType()
    
    def isViewableImage(self):
        imgsize = self.context.getSize()
        isImage = imgsize[0] and imgsize[1] or False
        isViewable = self.content_type() in BROWSER_MIMETYPES
        return isImage and isViewable
    
    def isViewableText(self):
        return self.content_type().startswith('text/')  # TODO: max size?
    
    def isViewableData(self):
        return self.isViewableImage() or self.isViewableText()
    
    def data(self):
        return self.context.data
    
    def inEditMode(self):
        return False
    
    def inViewMode(self):
        return self.isViewableData()

class UniFileEdit(UniFileView):
    """View class for the UnifiedFile type handing data for template(s),
    slightly specialized for text edit.
    """
    def inEditMode(self):
        return self.isViewableData()
    
    def inViewMode(self):
        return False

class UniFileTextEdit(UniFileBrowserView):
    """Form-handling view for text edit box in edit mode."""
    # FIXME: use formlib or something like it
    def __call__(self):
        request = self.request
        context = self.context
        
        # cancel button: noop, leave edit
        if request.has_key('form.button.Cancel'):
            request.response.redirect(context.absolute_url() + "/view")
            return
        
        # save button or no button (form default)
        text = request.get('text', None)
        field = context.getPrimaryField()
        filename = field.getFilename(context)   # setting ImageField to a string will lose the name...
        field.set(context, text)
        field.setFilename(context, filename)      # so we preserve it and restore it
        
        context.reindexObject()
        
        event.notify(objectevent.ObjectModifiedEvent(context))
        
        request.response.redirect(context.absolute_url() + "/edit")

class UniFileUpload(UniFileBrowserView):
    """Form-handling view for the UnifiedFile file upload."""
    # FIXME: use formlib or something like it
    def __call__(self):
        request = self.request
        context = self.context
        
        # cancel button: noop, leave edit
        if request.has_key('form.button.Cancel'):
            request.response.redirect(self.realParent().absolute_url() + "/contents")
            return
        
        # save button or no button (form default)
        factorytool = getToolByName(context, 'portal_factory')
        temporary = factorytool.isTemporary(context)
        file = request.get('file', None)
        
        try:
            oldid = context.getId()
            if temporary:
                context = factorytool.doCreate(context, context.getId())  # concretize
            
            context.setImage(file)
            #context.getPrimaryField().set(self.context, file)
            
            # setImage above handles rename on create; we have to handle it for subsequent uploads
            field = context.getPrimaryField()
            filename = field.getFilename(context, fromBaseUnit=False)
            if context.getId() != filename:
                context.setId(filename)
            
            context.reindexObject()
            
            if not temporary:  # used on new objects; don't say modified if just created
                event.notify(objectevent.ObjectModifiedEvent(context))
        except (CopyError, BadRequest):
            context.setId(oldid)
            message = _("text_error_file_exists", "Can not upload: file of that name already exists.")
            plone_utils = getToolByName(self.context, 'plone_utils')
            plone_utils.addPortalMessage(message)
        
        request.response.redirect(context.absolute_url() + "/view")
