#!/usr/bin/python3

import telnetlib
import csv
import io
import extractinfo

PORT_NER_SERVER=9191
PORT_POSTAG_SERVER=9192

def sendToNLPServer(string,port):
    try:
        tn=telnetlib.Telnet('localhost',port,1)
        string+='\n'
        tn.write(string.encode('ascii',errors='ignore'))
        raw_csv=tn.read_all().decode('utf-8')
        return raw_csv
    except:
        print('Error occurred when talking to NLP server on port {}\n'.format(port))

def NERAnalysis(string):
    resp=sendToNLPServer(string,PORT_NER_SERVER)
    f=io.StringIO(resp)
    rdr=csv.reader(f,delimiter='\t')
    ret_list=list(rdr)
    ret_list=[[e[0].strip(),e[1]] for e in ret_list]
    return ret_list

def POSTag(string):
    resp=sendToNLPServer(string,PORT_POSTAG_SERVER)
    str_list=resp.split(' ')
    if str_list[-1]=='':
        del str_list[-1]
    str_list=[e.split('_') for e in str_list]
    return str_list

def paragraphAnalysis(string):
    string=preProcessing(string)
    a=NERAnalysis(string)
    b=POSTag(string)
    assert len(a)==len(b), 'ERROR: NER and POS got results of different length'
    for i,e in enumerate(a):
        assert a[i][0]==b[i][0], 'ERROR: Different word found'
        e.append(b[i][1])
    return a

def preProcessing(string):
    ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(math.floor(n/10)%10!=1)*(n%10<4)*n%10::4])

    return string

if __name__=='__main__':
    s='The suspects made a number of unsubstantiated threats including a statement that they would “shoot up campus” and indicated bombs were placed in duffel bags with one located at the main entrance of a library. University Police immediately responded and located an unidentified bag in the area of Ohio State’s 18th Avenue Library.'
    print(paragraphAnalysis(s))
