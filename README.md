# wifi-scan
Scans for available wifi networks using linux iwlist and formats output to Python dictionary.  

Input is a wifi interface ('wlan0') - output is a dictionary w available wifi networks
 
 {
 1: [['Name', 'Network-1'],
     ['Secured', 'on'],
     ['Signal Quality', 1.0],
     ['Signal level', -23]],
 
 2: [['Name', 'Network-2'],
     ['Secured', 'on'],
     ['Signal Quality', 0.76],
     ['Signal level', -57]],
 
 3: [['Name', 'Network-3'],
     ['Secured', 'on'],
     ['Signal Quality', 0.87],
     ['Signal level', -49]],
 
 4: [['Name', 'Network-4'],
     ['Secured', 'on'],
     ['Signal Quality', 0.99],
     ['Signal level', -41]],
 
 5: [['Name', 'Network-5'],
     ['Secured', 'on'],
     ['Signal Quality', 0.43],
     ['Signal level', -80]],
}
 
Notes:  
       1. if the 'parse_char' is not found in the string, the key/value will be ignored

       2. sometimes the scan returns a SSID='\x00\x00\x00\x00'  in this case SSID will be returned as
          'Unknown'
       
       3. if a key is found, but the value is not found, value will be set to 'Not Found'
       
       4. in the CleanScan function, if mode=de-dupe, then it will remove cells that have the same 'Name'
          and select the dupe with the highest 'selectby' and toss all others
