"""
Initialization and package-wide constants.

Author: J. Cameron Cooper (jccooper@rice.edu)
Copyright (C) 2009 Rice University. All rights reserved.

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

from zope.i18nmessageid import MessageFactory
from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore import utils
#from Products.CMFCore.DirectoryView import registerDirectory

from config import GLOBALS, PROJECTNAME
from config import ADD_CONTENT_PERMISSIONS

unifileMessageFactory = MessageFactory('unifile')

#registerDirectory(config.SKINS_DIR, config.GLOBALS)

##Import Types here to register them
import File

def initialize(context):
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    utils.ContentInit(
        '%s Content' % PROJECTNAME,
        content_types      = content_types,
        permission         = ADD_CONTENT_PERMISSIONS['UnifiedFile'],
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

from Extensions import Install  # check syntax on startup
del Install
