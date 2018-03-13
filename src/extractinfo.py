#!/usr/bin/python3
import re
import nlpclient
import code
from collections import OrderedDict

paragraph_min_char = 40
addr_anchor = ['in','on','around','of']

# 2-phase personal trait finder
personal_desc_anchor_phase1 = ['suspect','described','report','stand','shoe','glasses']
personal_desc_anchor_phase2 = ['male','hair','wear','ages','fled','weigh','build','shoe','glasses']

crime_anchor = ['jail','robbery','burglary','murder','assault','arson','riot']

# Regex address matching for hybrid address matching
reg_addr_pattern1=r'(\d+ )?((E(ast)?|W(est)?|N(orth)?|S(outh)?)\.? )?(([A-Z]|\d)\w{0,} )+(Ave(nue)?|St(reet)?|Dr(ive)?|R(oa)?d|Al(le)?y|Blvd)\.?'
reg_addr_pattern2=r'(\d+ )?((E(ast)?|W(est)?|N(orth)?|S(outh)?)\.? )?(([A-Z]|\d)\w{0,}( |\.)){0,}'
reg_addr_pattern3=r'(\d+ )?((E(ast)?|W(est)?|N(orth)?|S(outh)?)\.? )?(([A-Z]|\d)\w{0,} )+(Ave((nue)|\.)|St((reet)|\.)|Dr((ive)|\.)|R((oad)|d\.)|Al((ley)|y\.)|Blvd)( [A-Z]\w{0,})*'
addr_matcher = re.compile(reg_addr_pattern3)

# This is supposed to fixup some minor flaws of the NLP engine
mute_list=['ohio','dear','police','cpd','safety','columbus','tip','crime']

def matchDate(input):
    pattern = r"\d{1,2}\/\d{1,2}(\/((\d{4})|(\d{2})))?"
    res = re.search(pattern,input)
    return res

def matchTime(input):
    pattern = r"(\d{1,2}(:\d{1,2})? ((a\.?m\.?)|(p\.?m\.?)))|noon|midnight"
    res = re.search(pattern,input)
    return res

def isNumString(string):
    if string[0].isdigit():
        return string.endswith('th') or string.endswith('st') or string.endswith('nd') \
        or string.endswith('rd')
    return False

# Find a list of start positions of possible location names
def tryFindNames(NLPStruct):
    # NLPStruct[..][0]=word [1]=NER [2]=tag
    i=0
    ptr=-1
    ret={'person':[],'location':[]}
    end=len(NLPStruct)
    current_type=''
    while i<end:
        if NLPStruct[i][0].lower() in mute_list:
            # Treat words in the "silence list" as first priority, dispose current match in progress and
            ptr=-1
            current_type=''
            i+=1
            while NLPStruct[i][1]=='LOCATION' or NLPStruct[i][1]=='ORGANIZATION':
                i+=1
            # Ensure conformity of the loop
            #i-=1
        elif NLPStruct[i][1]=='LOCATION' or NLPStruct[i][1]=='ORGANIZATION' or NLPStruct[i][1]=='PERSON':
            if ptr<0: # not matching
                current_type=NLPStruct[i][1]
                ptr=i
                # search backward to find possible omitted words
                while ptr-1>=0 and isNumString(NLPStruct[ptr-1][0]):
                    ptr-=1
        elif NLPStruct[i][2]=='CC' \
            and (NLPStruct[i+1][1]=='LOCATION' \
            or NLPStruct[i+1][1]=='ORGANIZATION'):
            # conjunction words
            pass
        else:
            if ptr>=0:# stop matching
                if current_type=='PERSON':
                    ret['person'].append([ptr,i])
                else:
                    ret['location'].append([ptr,i])
                current_type=''
                ptr=-1
        i+=1
    return ret

def getSubstringFromNLPS(NLPStruct,r):
    b=r[0]
    e=r[1]
    ret=NLPStruct[b][0]
    b+=1
    while b<e:
        ret+=' '
        ret+=NLPStruct[b][0]
        b+=1
    return ret

def regexAddrMatch(string):
    it = addr_matcher.finditer(string)
    ret = []
    for e in it:
        ret.append((e.group().strip(),e.span()))
    return ret

def checkMute(string):
    string=string.lower()
    for e in mute_list:
        if string.find(e)>=0:
            return True
    return False

def containName(A,B):
    for eb in B:
        if eb.lower().find(A.lower()) >=0:
            return True
    return False

def mergeNameResults(A,B):
    ret=B
    for ea in A:
        if not containName(ea,B):
            ret.append(ea)
    return ret

'''
def findNamesInParagraph(string):
    NLPS=nlpclient.paragraphAnalysis(string)
    b=tryFindNames(NLPS)
    regex_match=regexAddrMatch(string)
    regex_match=[e for e in regex_match if len(e[0])>10]
    if len(regex_match) > 0:
        print('REGEX match')
        regex_match=[e for e in regex_match if not checkMute(e[0])]
        print([e[0] for e in regex_match])
        return {'person':[getSubstringFromNLPS(NLPS,e) for e in b['person']],'location':[e[0] for e in regex_match]}
    else:
        print('NLP match')
        print([getSubstringFromNLPS(NLPS,e) for e in b['location']])
        return {'person':[getSubstringFromNLPS(NLPS,e) for e in b['person']],'location':[getSubstringFromNLPS(NLPS,e) for e in b['location']]}
'''
def findNamesInParagraph(string):
    NLPS=nlpclient.paragraphAnalysis(string)
    b=tryFindNames(NLPS)
    regex_match=regexAddrMatch(string)
    regex_match=[e for e in regex_match if len(e[0])>10 and not checkMute(e[0]) ]
    regex_match=[e[0] for e in regex_match]
    nlp_match=[getSubstringFromNLPS(NLPS,e) for e in b['location']]
    nlp_match=[e for e in nlp_match if e!=e.upper()]
    print('REGEX Match:',regex_match)
    print('NLP Match:',nlp_match)
    return {'person':[getSubstringFromNLPS(NLPS,e) for e in b['person']],'location':mergeNameResults(regex_match,nlp_match)}

def splitArticleIntoParagraphs(article):
    ret = article.split('\n')
    # Use a rule of thumb to filter out some too-short paragraphs
    ret = [e.strip() for e in ret if len(e) > paragraph_min_char ]
    return ret

def expandFromIndex(string,ind):
    a=ind
    while string[ind]!='.' and ind !=0:
        ind-=1
    if ind!=0:
        ind+=2
    while string[a]!='.':
        a+=1
    return string[ind:a+1]

def findPersonTraitsInParagraph(string):
    for e in personal_desc_anchor_phase1:
        ind=string.find(e)
        if ind != -1:
            print('PT phase 1 hit: {}'.format(e))
            string1=expandFromIndex(string,ind)
            for e1 in personal_desc_anchor_phase2:
                ind1=string1.find(e1)
                if ind1!= -1:
                    print('PT phase 2 hit: {}'.format(e1))
                    return string1
    return ''

def strNotOccuredAfterInd(list,s,ind):
    l=len(list)
    ind+=1
    while ind < l:
        if list[ind].find(s)>=0:
            return False
        ind+=1
    return True

def removeDuplication(strlist):
    if len(strlist)<2 :
        return strlist
    strlist.sort(key=len)
    return [string for ind, string in enumerate(strlist) \
        if strNotOccuredAfterInd(strlist,string,ind)]

def strListToMultiLine(l):
    if len(l)==0:
        return ''
    else:
        return '\n'.join(l)

emgcy_type=OrderedDict([('harass','HR'),
    ('sexual','HR'),
    ('burglary','BG'),
    ('rob','RB'),
    ('grab','RB'),
    ('demand','RB'),
    ('theft','TH'),
    ('stole','TH'),
    ('arson','AR'),
    ('assault','AS'),
    ('murder','MD'),
    ('kill','MD')
    ])

def emergencyTypeClassifier(article):
    for k,v in emgcy_type.items():
        if article.find(k)>=0:
            return v
    return 'OT'

def removeWrongNames(pn,addr):
    return [e for e in pn if addr.find(e)<0]

def collectDataFromArticle(article):
    paras=splitArticleIntoParagraphs(article)
    pt=[]
    addr=[]
    person=[]
    typ=emergencyTypeClassifier(article)
    i=1
    for p in paras:
        print('\tProcessing paragraph %d/%d'%(i,len(paras)))
        i=i+1
        ppt=findPersonTraitsInParagraph(p)
        if ppt:
            pt.append(ppt)
        names=findNamesInParagraph(p)
        person+=names['person']
        addr+=names['location']
    addr=strListToMultiLine(removeDuplication(addr))
    person=strListToMultiLine(removeWrongNames(removeDuplication(person),addr))
    return {'time':matchDate(article).group()+' '+matchTime(article).group(),
    'suspect_traits':strListToMultiLine(pt),
    'address':addr,
    'image_url':'',
    'original_email':article,
    'suspect_name':person,
    'emergency_type':typ,
    'optional_info':''}

if __name__ == '__main__':

    code.interact(local=locals())
