#!/usr/bin/python

import os,sys,re,urllib2
from selenium import webdriver

#global vars initialization
browser=None
hrefs=set([])
removed=set([])
output=[]


def readPhantomPath():
    global browser
    with open('phantompath.txt', 'r') as myfile:
        path = myfile.read().strip()
        browser=webdriver.PhantomJS(executable_path=path)
        #browser.webdriver.FireFox()  #use this in case phantomJS isn't working


#actual functionality: open site and scrape/parse
def parseSite(url,arg,flag):
    global basearg,hrefs,removed,browser,output

    if (flag):
        basearg=arg
        hrefs.add(basearg)
        print "Found these email addresses:"
    
    browser.get(arg)
    html=browser.page_source
    arg=browser.current_url #takes care of redirection

    if arg[-1] == '/':
	    arg=arg[:-1]
    

    #find all hrefs
    #one of two formats applicable:
    # - basearg + anywords
    # - / + anywords
    hrefs=hrefs | set(re.findall(r'href=\"'+re.escape(arg)+'[\S]+\"',html))
    hrefs=hrefs | set(re.findall(r'href=\"\/[\S]+\"',html))
    
    listhrefs=list(hrefs)
    pattern=re.compile(r'href=\"[\S]+[.][\w]+\"')
    for url1 in listhrefs:
        # manage unwanted urls with extensions other than .html
        if pattern.match(url1): #if url1 has an extension
            url1list=url1.split('.')
            if url1list[-1] != 'html':
                listhrefs.remove(url1)

        #delete url if already visited
        if url1 in removed and url1 in listhrefs:
            listhrefs.remove(url1)

    
    hrefs=set(listhrefs)

    #find all emails matching the following pattern:
    #  mailbox name (1 or more instances of any character)
    #  @
    #  domain name (any word in ascii)
    #  the literal . 
    #  the ending of a domain name (ie. .com, .husky.neu.edu, etc...) 
    emails = set(re.findall(r'[\w.-]+@[\w]+[.][\w.-]+', html))
    for email in emails:
        if email not in output:
            print email
            output.append(email)


    removed.add(url)

    while hrefs:
        url1=hrefs.pop()
        arg2=url1.split('"')[1]
    	if '://' not in url1:
    	    arg2=basearg+arg2

    	parseSite(url1,arg2,False)



def main():
    arg = sys.argv[1:] #remove script name 
    if '://' not in arg:
        arg='http://'+arg[0]

    readPhantomPath();

    basearg=arg
    parseSite(arg,arg,True)


#to run only when script is executed, not imported
if __name__ == "__main__":
    try:
        main()
        browser.quit()
    except RuntimeError as e:
        browser.quit()

