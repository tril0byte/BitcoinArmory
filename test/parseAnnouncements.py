import os
import sys
import unittest

sys.path.append('..')

from armoryengine.parseAnnounce import *
from armoryengine.ArmoryUtils import *

testingText = """
# This is a comment

       # Nothing to see here
#----------------------------------

Version 0.31

   - Major Feature 1
        This is a description of the first major feature.

   - Major Feature 2
        Description of 
        the second 
        big feature.  
 - Major Feature 3

        Indentations might be
    malformed


Version 0.30

   - Major Feature 4
        Another multi-line 
        description

# I debated whetehr to put this next feature in there...
   # In the end I did
   - Major Feature 5
        Description of the fifth big feature.  

Version 0.25

   # I realize these feature numbers don't make sense for decreasing 
   # version numbers
   - Major Feature 6
        # Can we put comments
        This feature requires
        # in the middle of
        # the descriptions?
        interspersed comments

   - Major Feature 7

   - Major Feature 8
"""



fullFeatureLists = \
[ \
    [ '0.31', 
        [ \
            ['Major Feature 1', 'This is a description of the first major feature.'], 
            ['Major Feature 2', 'Description of the second big feature.'], 
            ['Major Feature 3', 'Indentations might be malformed'] \
        ] \
    ], 
    [ '0.30', 
        [ \
            ['Major Feature 4', 'Another multi-line description'], 
            ['Major Feature 5', 'Description of the fifth big feature.'] \
        ] \
    ], 
    [ '0.25', 
        [ \
            ['Major Feature 6', 'This feature requires interspersed comments'], 
            ['Major Feature 7', ''], 
            ['Major Feature 8', ''] \
        ] \
    ] \
]
    


downloadTestText = """

   -----BEGIN BITCOIN SIGNED MESSAGE-----
   # Armory for Windows
   Armory 0.91 Windows XP        32     http://url/armory_0.91_xp32.exe  3afb9881c32
   Armory 0.91 Windows XP        64     http://url/armory_0.91_xp64.exe  8993ab127cf
   Armory 0.91 Windows Vista,7,8 32,64  http://url/armory_0.91.exe       7f3b9964aa3


   # Various Ubuntu/Debian versions
   Armory 0.91 Ubuntu 10.04,10.10  32   http://url/armory_10.04-32.deb   01339a9469b59a15bedab3b90f0a9c90ff2ff712ffe1b8d767dd03673be8477f
   Armory 0.91 Ubuntu 12.10,13.04  32   http://url/armory_12.04-32.deb   5541af39c84
   Armory 0.91 Ubuntu 10.04,10.10  64   http://url/armory_10.04-64.deb   9af7613cab9
   Armory 0.91 Ubuntu 13.10        64   http://url/armory_13.10-64.deb   013fccb961a

   # Offline Bundles
   ArmoryOffline 0.90 Ubuntu 10.04  32  http://url/offbundle-32-90.tar.gz 641382c93b9
   ArmoryOffline 0.90 Ubuntu 12.10  32  http://url/offbundle-64-90.tar.gz 5541af39c84
   ArmoryOffline 0.88 Ubuntu 10.04  32  http://url/offbundle-32-88.tar.gz 641382c93b9
   ArmoryOffline 0.88 Ubuntu 12.10  32  http://url/offbundle-64-88.tar.gz 5541af39c84

   # Windows 32-bit Satoshi (Bitcoin-Qt/bitcoind)
   Satoshi 0.9.0 Windows XP,Vista,7,8 32,64 http://btc.org/win0.9.0.exe   837f6cb4981314b323350353e1ffed736badb1c8c0db083da4e5dfc0dd47cdf1
   Satoshi 0.9.0 Ubuntu  10.04        32    http://btc.org/lin0.9.0.deb   2aa3f763c3b
   Satoshi 0.9.0 Ubuntu  10.04        64    http://btc.org/lin0.9.0.deb   2aa3f763c3b

   -----BEGIN BITCOIN SIGNATURE-----
   ac389861cff8a989ae57ae67af43cb3716ca189aa178cff893179531
   -----END BITCOIN SIGNATURE-----

"""







class parseVersionsTest(unittest.TestCase):


   def setUp(self):
      pass
      
   def tearDown(self):
      pass


   # TODO: This test needs more verification of the results.
   def testReadAll(self):
      
      testOutput     = parseVersionsText(testingText)
      expectedOutput = fullFeatureLists[:]

      for test,expect in zip(testOutput, expectedOutput):
         self.assertEqual( test[0], expect[0] )
         
         for testFeat, expectFeat in zip(test[1], expect[1]):
            self.assertEqual( testFeat, expectFeat )


   def testStopAt028(self):

      testOutput     = parseVersionsText(testingText, getVersionInt([0,28,0,0]))
      expectedOutput = fullFeatureLists[:-1]

      for test,expect in zip(testOutput, expectedOutput):
         self.assertEqual( test[0], expect[0] )
         
         for testFeat, expectFeat in zip(test[1], expect[1]):
            self.assertEqual( testFeat, expectFeat )


class parseDownloadTest(unittest.TestCase):
   
   def setUp(self):
      self.dl = downloadLinkHandler(filetext=downloadTestText)

   def tearDown(self):
      pass


   def testParseDL(self):

      dllink = self.dl.getDownloadLink('Armory','0.91','Windows','XP','32')
      self.assertEqual(dllink, ['http://url/armory_0.91_xp32.exe', '3afb9881c32'])

      dllink = self.dl.getDownloadLink('Armory','0.91','Windows','Vista','32')
      self.assertEqual(dllink, ['http://url/armory_0.91.exe', '7f3b9964aa3'])

      # This is a real file with a real hash, for testing DL in Armory
      dllink = self.dl.getDownloadLink('Satoshi','0.9.0','Windows','7','64')
      self.assertEqual(dllink, ['http://btc.org/win0.9.0.exe',
            '837f6cb4981314b323350353e1ffed736badb1c8c0db083da4e5dfc0dd47cdf1'])

      dllink = self.dl.getDownloadLink('ArmoryOffline','0.88','Ubuntu','10.04','32')
      self.assertEqual(dllink, ['http://url/offbundle-32-88.tar.gz', '641382c93b9'])

      dllink = self.dl.getDownloadLink('Armory','1.01','WIndows','10.04','32')
      self.assertEqual(dllink, None)

if __name__ == "__main__":

   # This is just a fun way to look at the download data
   #dl = downloadLinkHandler(filetext=downloadTestText)
   #dl.printDownloadMap()

   unittest.main()


