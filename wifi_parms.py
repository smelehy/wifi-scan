WIFI_SCAN_CMD   = 'sudo iwlist %(nwinterface)s scan'
WIFI_CARD_NAME  = 'wlan0'

# wifi scan parameters
# These rules dictate what and how information is pulled out of the iwscan results (which returns raw text)
# STR_RULES is a dictionary of lists.  each list has an embedded dictionary with key/values that specify
# the 'how'.  parse_char is what separates the key from the value in the string.  the app will pull out 
# a string for each key value pair terminated by the 'end_char'.  replace_char will be removed from the string

STR_RULES       = {
                   0  : ('Cell', 
                               {'parse_char'   : ' ',
                                'end_char'     : '-',
                               },
                        ),
                   1  : ('ESSID', 
                               {'parse_char'   : ':',
                                'replace_char' : '"',
                                'end_char': '\n',
                                'friendly_name': 'Name',
                               },
                        ),
                   2  : ('Encryption key', 
                               {'parse_char'   : ':',
                                'end_char': '\n',
                                'friendly_name': 'Secured',
                               },
                        ),
                   3  : ('Quality', 
                               {'parse_char'   : '=',
                                'end_char'     : 'Sig',
                                'friendly_name': 'Signal Quality',
                               },
                        ),
                   4  : ('Signal level', 
                               {'parse_char'   : '=',
                                'replace_char' : 'dBm',
                                'end_char'     : '\n',   # when scan finds the rule name ('signal level')
                                                        # pull out a string that starts with that and ends
                                                        # with this character
                               },
                        ),
                 }
