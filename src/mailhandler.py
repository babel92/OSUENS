#!/usr/bin/python3

import extractinfo
import outlook
import sys
import json
import KEY
import time
import copy
from pathlib import Path
import requests
import geocoding

def commitDataToDjango(dict):
    r=requests.post('http://localhost/api/add',data=dict)
    print(r.status_code,r.reason)

def addrToMarkerScript(al):
    al=al.split('\n')
    if len(al)>2:
        # If there are too many addresses, we leave it to the manager
        print('Auto MarkerScript generation failed: too many addresses')
        return ''
    elif len(al)==2:
        al=[' & '.join(al)]
    ret=''
    gi=geocoding.addrsToInfoList(al)
    for ind,e in enumerate(gi):
        coord=e['coord']
        ret+='circle,%f,%f,%d,%s\n'%(coord[0],coord[1],50,al[ind])
    return ret


if __name__=='__main__':
    if len(sys.argv) <2:
        print("Usage: mailhandler.py <filename>\n       mailhandler.py runserver")
        sys.exit(0)
    if sys.argv[1]=='runserver':
        SLEEP_TIME=120
        m=outlook.Outlook()
        m.login(KEY.OSU_EMAIL,KEY.OSU_EMAIL_PWD)
        m.inbox()
        print('Mail client is watching. Press Ctrl+C to exit.')
        try:
            while True:
                unread_mail=m.unreadIds()
                if m.hasUnread():
                    for mailID in unread_mail:
                        print('Fetching unread email. ID:',mailID)
                        m.getEmail(mailID)
                        # ensure this is a mail from OSUEM
                        if m.mailfrom().find('emergencymanagement') >= 0:
                            print('Emergency message found. Start working...')
                            data=extractinfo.collectDataFromArticle(m.mailbody())
                            data['marker_script']=addrToMarkerScript(data['address'])
                            commitDataToDjango(info)
                time.sleep(SLEEP_TIME)
        except KeyboardInterrupt:
            print('Interrupted!')

    else:
        with open(sys.argv[1], 'r',errors='ignore') as content_file:
            content = content_file.read()
            data=extractinfo.collectDataFromArticle(content)
            data4print=copy.deepcopy(data)
            data4print['original_email']='...'
            print(data4print)
            data['marker_script']=addrToMarkerScript(data['address'])
            commitDataToDjango(data)
