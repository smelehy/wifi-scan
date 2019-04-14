# wifi-scan
Scans for available wifi networks using linux iwlist and formats output to Python dictionary
input is a wifi interface ('wlan0') - output is a dictionary w available wifi networks


 {1 : [ ['Signal level'  , -38],
        ['Secured'       , 'on'],
        ['Signal Quality', 0.71],
        ['Name'          , 'OldisOnTheManJay'],
      ],
  2 : [ ['Signal level'  , -50],
        ['Secured'       , 'on]',
        ['Name'          , 'OtherNetWork'],
      ]
 }

Notes:  
       1. if the 'parse_char' is not found in the string, the key/value will be ignored
       2. sometimes the scan returns a SSID='\x00\x00\x00\x00'  in this case SSID will be returned as
          'Unknown'
       3. if a key is found, but the value is not found, value will be set to 'Not Found'
       4. in the CleanScan function, if mode=de-dupe, then it will remove cells that have the same 'Name'
          and select the dupe with the highest 'selectby' and toss all others
