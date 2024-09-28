# -*- coding: iso-8859-15
import unittest
from lxml import etree
import os
import codecs
import json
import zipfile

PHONE_PATH = '/run/user/1000/gvfs/mtp:host=wheatek_BV8800_BV8800EEA0022112/Interner gemeinsamer Speicher/Documents/obb/net.osmand/rendering'


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
                        "file": "/rendering/%s" % fname,
                        "subtype": "rendering_style"
                    },
                ]
            }

            styleName = base.replace('.render', '')
            j = json.dumps(items_dict, indent=4)
            open(osfPath, 'w').write(j)
            zipPath = os.path.join(self.buildDir, '%s.osf' % styleName)
            zip_file = zipfile.ZipFile(zipPath, 'w')
            zip_file.write(fPath, arcname='rendering/%s' % fname)
            zip_file.write(osfPath, arcname='items.json')
            zip_file.close()

            # if exists, copy to phone.
            if os.path.exists(PHONE_PATH):
                with codecs.open(fPath, mode='r', encoding='utf-8') as fp:
                    xml = fp.read()

                with codecs.open(os.path.join(PHONE_PATH, fname), mode='w', encoding='utf-8') as fp:
                    fp.write(xml)

                print('written to %s' % PHONE_PATH)
            else:
                raise RuntimeError('connection to phone not possible')

