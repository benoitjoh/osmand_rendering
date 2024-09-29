# -*- coding: iso-8859-15
import unittest
from lxml import etree
import os
import codecs
import json
import zipfile

PHONE_PATH = '/run/user/1000/gvfs/mtp:host=wheatek_BV8800_BV8800EEA0022112/Interner gemeinsamer Speicher/Documents/net.osmand/rendering'


class ParseTests(unittest.TestCase):
    """ just runs a parse of the rendering.xml file
        creates a osmand import file for the xml ( .osf file)
        uploads the xml to a phone to the path above for testing """
    # -----------------------------------------------------------------------

    def setUp(self):
        self.workDir = '..'
        self.buildDir = os.path.join(self.workDir, 'build')
        if not os.path.exists(self.buildDir):
            os.makedirs(self.buildDir)

        print(" --> starting Test: %s" % __name__)

    def tearDown(self):
        return

    # -----------------------------------------------------------------------

    def _getXmlFileList(self):
        fileList = []
        for fname in os.listdir(self.workDir):
            baseName, ext = os.path.splitext(fname)
            fPath = os.path.join(self.workDir, fname)
            if ext != '.xml':
                continue
            fileList.append((fname, fPath, baseName))
        return fileList

    def test_1_parseXml(self):

        for fname, fPath, baseName in self._getXmlFileList():
            etree.parse(fPath)

    def test_2_buildOSF(self):
        for fname, fPath, baseName in self._getXmlFileList():
            # BUILD THE OSF FILE
            osfManifestPath = os.path.join(self.buildDir, 'items.json')
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

            styleName = baseName.replace('.render', '')
            j = json.dumps(items_dict, indent=4)
            open(osfManifestPath, 'w').write(j)
            zipPath = os.path.join(self.buildDir, '%s.osf' % styleName)
            zip_file = zipfile.ZipFile(zipPath, 'w')
            zip_file.write(fPath, arcname='rendering/%s' % fname)
            zip_file.write(osfManifestPath, arcname='items.json')
            zip_file.close()

    def test_3_uploadXmlToPhone(self):

        for fname, fPath, baseName in self._getXmlFileList():
            # if exists, copy to phone.
            if os.path.exists(PHONE_PATH):
                with codecs.open(fPath, mode='r', encoding='utf-8') as fp:
                    xml = fp.read()

                with codecs.open(os.path.join(PHONE_PATH, fname), mode='w', encoding='utf-8') as fp:
                    fp.write(xml)

                print('written to %s' % PHONE_PATH)
            else:
                raise RuntimeError('connection to phone not possible')

