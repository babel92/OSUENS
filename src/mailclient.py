#!/usr/bin/python3

import outlook
import code
import KEY
import time
import extractinfo
import requests
import geocoding

SLEEP_TIME=120

def pushDataToDjango(dict):
    r=requests.post('http://localhost/api/add',data=dict)
    print(r.status_code,r.reason)

if __name__=='__main__':
    m=outlook.Outlook()
    m.login(KEY.OSU_EMAIL,KEY.OSU_EMAIL_PWD)
    m.inbox()
    print('Mail client is watching. Press Ctrl+C to exit.')
    try:
        while True:
            unread_mail=m.unreadIds()
            if len(unread_mail)>0:
                for mailID in unread_mail:
                    m.getEmail(mailID)
                    # ensure this is a mail from OSUEM
                    if m.mailfrom().find('emergencymanagement') >= 0:
                        info=extractinfo.collectDataFromArticle(m.mailbody())
                        pushDataToDjango(info)
            time.sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        print('Interrupted!')
