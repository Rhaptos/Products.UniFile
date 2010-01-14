#------------------------------------------------------------------------------#
#   test_uni_file.py                                                           #
#                                                                              #
#       Authors:                                                               #
#       Rajiv Bakulesh Shah <raj@enfoldsystems.com>                            #
#                                                                              #
#           Copyright (c) 2009, Enfold Systems, Inc.                           #
#           All rights reserved.                                               #
#                                                                              #
#               This software is licensed under the Terms and Conditions       #
#               contained within the "LICENSE.txt" file that accompanied       #
#               this software.  Any inquiries concerning the scope or          #
#               enforceability of the license should be addressed to:          #
#                                                                              #
#                   Enfold Systems, Inc.                                       #
#                   4617 Montrose Blvd., Suite C215                            #
#                   Houston, Texas 77006 USA                                   #
#                   p. +1 713.942.2377 | f. +1 832.201.8856                    #
#                   www.enfoldsystems.com                                      #
#                   info@enfoldsystems.com                                     #
#------------------------------------------------------------------------------#
"""Unit tests.
$Id: $
"""


from Products.RhaptosTest import config
import Products.UniFile
config.products_to_load_zcml = [('configure.zcml', Products.UniFile),]
config.products_to_install = ['UniFile']
config.extension_profiles = ['Products.UniFile:default']

from Products.UniFile.interfaces import IUnifiedFile
from Products.RhaptosTest import base


class TestUniFile(base.RhaptosTestCase):

    def afterSetUp(self):
        # XXX:  This next line of code shouldn't be necessary.
        # Products.RhaptosTest should already add this generic setup profile,
        # as specified above.  But for some reason, it doesn't.  Please fix
        # this.
        self.addProfile('Products.UniFile:default')

        # PloneTestCase already gives us a folder, so within that folder,
        # create a UniFile.
        self.folder.invokeFactory('UnifiedFile', 'file')
        self.file = self.folder.file

    def beforeTearDown(self):
        pass

    def test_file_interface(self):
        # Make sure that the file content object implements the expected interface.
        self.failUnless(IUnifiedFile.providedBy(self.file))

    def test_file_type(self):
        # Make sure that the file reports its correct portal type.
        self.assertEqual(self.file.portal_type, 'UnifiedFile')

    def test_file(self):
        self.assertEqual(1, 1)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestUniFile))
    return suite
