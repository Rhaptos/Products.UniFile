= UniFile =

Plone-style Image and File handling all in one object, so that users don't have to
try to distinguish between Image and File.

author: J Cameron Cooper (jccooper@rice.edu)
Started 13 Apr 2009
Copyright (c) 2009, Rice University. All rights reserved.

This Zope/Plone Product is used as part of the Rhaptos system (http://rhaptos.org),
created to run Connexions (http://cnx.org.)

Install through GenericSetup, or through standard QuickInstaller, which runs GenericSetup,
in any portal after installing the code in the standard (non-egg/buildout) manner for Products:
that is, put the directory in /Products. QuickInstaller is most useful in Rhaptos context,
because we cannot yet run all steps; QI runs only seelcted steps that are needed for this product.

If you wish to transform existing Files and Images to UniFiles, there's a script in Upgrades
called migrateFiles.zctl that does this. Run it with 'zopectl run'.

Used mostly in Rhaptos contexts by its developers and maintainers, so report any
infelicities when used in standard Plone.

Special Features:
  - if a 'super' slot, like in RhaptosSite's customization of main_template, is provided
    a UniFile will use the parent's tabs, highlighting the 'files' action.
  - if a 'content_title_header' slot is similarly provided, it will fill that with the
    usual module header, provided it can find 'module_template'