# -*- coding: iso-8859-15
import unittest
from lxml import etree
import os
import json
import zipfile


class ParseTests(unittest.TestCase):
    """ just runs a parse of the rendering.xml file """
    # -----------------------------------------------------------------------

    def setUp(self):
        print(os.getcwd())
        self.workDir = '..'
        self.buildDir = os.path.join(self.workDir, 'build')
        if not os.path.exists(self.buildDir):
            os.makedirs(self.buildDir)


        print(" --> starting Test: %s" % __name__)

    def tearDown(self):
        return

    # -----------------------------------------------------------------------

    def testParseAndBuildOSF(self):

        for fname in os.listdir(self.workDir):
            base, ext = os.path.splitext(fname)
            if ext != '.xml':
                continue
            print('parsing: %s' % fname)
            fPath = os.path.join(self.workDir, fname)
            etree.parse(fPath)


            # BUILD THE OSF FILE
            osfPath = os.path.join(self.buildDir, 'items.json')
            items_dict = {
                "version": 1,
                "items": [
                    {
                        "type": "FILE",
                        "file": r"\/rendering\/%s" % fname,
                        "subtype": "rendering_style"
                    },
                ]
            }
            
            styleName = base.replace('.render', '')
            j = json.dumps(items_dict, indent=4)
            #open(osfPath, 'w').write(j)
            zipPath = os.path.join(self.buildDir, '%s.osf' % styleName)
            zip_file = zipfile.ZipFile(zipPath, 'w')
            zip_file.write(fPath, arcname='rendering/%s' % fname)
            zip_file.write(osfPath, arcname='items.json')
            zip_file.close()
