import os
from wifi_parms import *
import time
import pprint
import sys
# input is a wifi interface ('wlan0') - output is a dictionary w available wifi networks
# {1 : [ ['Signal level'  , -38],
#        ['Secured'       , 'on'],
#        ['Signal Quality', 0.71],
#        ['Name'          , 'OldisOnTheManJay'],
#      ],
#  2 : [ ['Signal level'  , -50],
#        ['Secured'       , 'on]',
#        ['Name'          , 'OtherNetWork'],
#      ]
# }
#   Notes:  
# 	1. if the 'parse_char' is not found in the string, the key/value will be ignored
#       2. sometimes the scan returns a SSID='\x00\x00\x00\x00'  in this case SSID will be returned as
#	   'Unknown'
#       3. if a key is found, but the value is not found, value will be set to 'Not Found'
#       4. in the CleanScan function, if mode=de-dupe, then it will remove cells that have the same 'Name'
#          and select the dupe with the highest 'selectby' and toss all others

def scanparse(workingscan, rules):
    wifilist          = []
# parse out cell info
    keyword       = rules[0]
    start         = workingscan.find(keyword)
    endword       = rules[1].get('end_char')
    end           = start + workingscan[start:].find(endword)
    scanlen       = workingscan.count(keyword)
    ignore_data   = False

    for i in range(scanlen):
      if rules[1].get('replace_char') is None:   # if there's no replace char, just strip off trailing
                                                 # blanks and split into key/value
        x1        = workingscan[start:end].rstrip().split(rules[1].get('parse_char',1))
      else:
        x         = workingscan[start:end].rstrip()
        x         = x.replace(rules[1].get('replace_char'),"")
        x1        = x.split(rules[1].get('parse_char',1))
      if len(x1)  == 1:
        x1.append('no parse character - garbage')
        ignore_data = True
      y           = workingscan[end+1:]
      if rules[1].get('end_char') is None:
        rules[1].update({'end_char': rules[0]})  # if no end char, use the rule name
      nend        = y.find(rules[0])
      z           = y[:nend]
      if x1[1].count('\\x00') > 0:  # sometimes network names come back as garbage chars
       x1[1]      = 'Unknown'
      newlist     = [x1[0],x1[1],z]
      try:    # convert the value to a number if it can be
        num       = int(newlist[1])
        del newlist[1]
        newlist.insert(1,num)
      except:
        try:
          num     = round(eval(newlist[1]),2)
          del newlist[1]
          newlist.insert(1,num)
        except:
          temp = 1
      if ignore_data is not True:
        wifilist.append(newlist)
      workingscan = y[nend:]
      start=workingscan.find(keyword)
      end         = start + workingscan[start:].find(endword)
#endloop

    return wifilist

def convert_to_friendly(name):  #converts the wifi scan paramter name to a user friendly name
  for vars in range(len(STR_RULES)):
    if STR_RULES.get(vars)[0] == name:
      if STR_RULES.get(vars)[1].get('friendly_name') is None:
        return name
      else:
        return STR_RULES.get(vars)[1].get('friendly_name')

def WifiScan(nwinterface):
  command           = WIFI_SCAN_CMD % {'nwinterface': nwinterface}
  try:
     rawscan           = os.popen(command).read()
  except:  # occasionally a wifi card will error when being checked.  just wait and try again works every time
     time.sleep(100)
     try:
       rawscan           = os.popen(command).read()
     except:
       return 1

  parsedlist        = scanparse(rawscan,STR_RULES.get(0))
  scan_results    = {}
  for cells in range(len(parsedlist)):
    value_list      = []
    value_pair      = []
    for rules in range(1, len(STR_RULES)):
      rule          = scanparse(parsedlist[cells][2],STR_RULES.get(rules))
      if rule == []:
        temp_list   = []
        temp_list.append(STR_RULES.get(rules)[0])
        temp_list.append('Not found')
        rule.append(temp_list)
      value_pair.append(convert_to_friendly(rule[0][0]))
      value_pair.append(rule[0][1])
      value_list.append(value_pair)
      value_pair    = []
      if rules == len(STR_RULES)-1:
        scan_results[parsedlist[cells][1]] = value_list

  scan_results      = CleanScan(scan=scan_results, mode='remove', fieldname='Name', value='Unknown')
  scan_results      = CleanScan(scan=scan_results, mode='remove', fieldname='Name', value='')
  scan_results      = CleanScan(scan=scan_results, mode='de-dupe', fieldname='Name', selectby='Signal Quality')

  return scan_results

def CleanScan(**kwargs): # mode: de-dupe or remove
                         # fieldname: the field name to act upon for mode
                         # value: the value (used for remove)
                         # scan:  wifi scan results in dictionary form
  scanvar      = kwargs.get('scan')
  varvalue     = kwargs.get('value')
  if kwargs.get('mode') == 'remove':
    if varvalue is '':
       varvalue = "''"
    if str(scanvar).find(varvalue) <= 0:  # quick check to see if the value to be removed
                                          # is even in the scan at all
        return scanvar

    for i in range(1, len(scanvar)+1):
      try:
        temp = scanvar.get(i)[0][0]
        if scanvar.get(i)[0][0] == kwargs.get('fieldname') and scanvar.get(i)[0][1] == kwargs.get('value'):
          del scanvar[i]
          i+=1
      except:
        temp = 0
  elif kwargs.get('mode') == 'de-dupe':
     tmpscanvar       = scanvar.copy()
     deldict          = {}
     for network1 in scanvar.items():
       n1dict         = dict(network1[1])
       n1dict['Cell'] = network1[0]
       tmpscanvarindex= tmpscanvar.copy()
       for network2 in tmpscanvarindex.items():
         n2dict         = dict(network2[1])
         n2dict['Cell'] = network2[0]
         if n2dict.get('Cell') is not n1dict.get('Cell') and n2dict.get('Name') == n1dict.get('Name') and deldict.get(n1dict.get('Cell')) is not 'Marked for Delete':
           if n2dict.get(kwargs.get('selectby')) < n1dict.get(kwargs.get('selectby')):
             del tmpscanvar[n2dict.get('Cell')]
             deldict[n2dict.get('Cell')] = 'Marked for Delete'
           else:
             del tmpscanvar[n1dict.get('Cell')]
             deldict[n1dict.get('Cell')] = 'Marked for Delete'

# delete all the scan network entries that were marked for deletion
     for deletes in deldict:
       del scanvar[deletes]

#  re-index so count goes consequtively
  reindex     = {}
  x           = list(scanvar.items())
  for index in range(1, len(x)+1):
    reindex[index] = x[index-1][1]

  scanvar     = reindex
  return scanvar

results  = WifiScan('wlan0')
print(sys.version_info)
print('Scan results......')
pprint.pprint(results)
