import numpy
import Crypto
import xml.sax as xs

import FILES.file2
import FILES.file3
import FILES.file4

def test_expat_entityresolver(self):
        parser = xs.expatreader.create_parser()
        parser.setEntityResolver(self.TestEntityResolver())
        result = xs.StringIO()
        parser.setContentHandler(xs.XMLGenerator(result))

        parser.feed('<!DOCTYPE doc [\n')
        parser.feed('  <!ENTITY test SYSTEM "whatever">\n')
        parser.feed(']>\n')
        parser.feed('<doc>&test;</doc>')
        parser.close()

        self.assertEqual(result.getvalue(), "<doc><entity></entity></doc>")

def main():
   print ('module imported', __name__)
   return
if __name__=='__main__':
   main()