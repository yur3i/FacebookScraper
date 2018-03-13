#!/usr/bin/python2.7

import sys
import requests
import pyquery
from bs4 import BeautifulSoup
import re
def login(session, email, password):
    
    '''
    Attempt to login to Facebook. Returns user ID, xs token and
    fb_dtsg token. All 3 are required to make requests to
    Facebook endpoints as a logged in user. Returns False if
    login failed.
    '''

    response = session.get('https://m.facebook.com')
    
    response = session.post('https://m.facebook.com/login.php', data={
        'email': email,
        'pass': password
    }, allow_redirects=False)
    
    if 'c_user' in response.cookies:

        homepage_resp = session.get('https://m.facebook.com/home.php')
        dom = pyquery.PyQuery(homepage_resp.text.encode('utf8'))
        fb_dtsg = dom('input[name="fb_dtsg"]').val()

        return fb_dtsg, response.cookies['c_user'], response.cookies['xs']
    else:
        return False 



def getbasicinfo(session, target):

    '''
    Attempt to go to a targets page and get their basic information.
    eg: Place of work, study, DoB etc, 'target' argument should be 
    their username: eg facebook.com/foo, target would be foo
    '''

    targetpage = session.get('https://m.facebook.com/'+target+'/about')
    soup = BeautifulSoup(targetpage.text, 'html.parser')
    basicinfo = str(soup.findAll("div", id='basic-info'))
    soup = BeautifulSoup(basicinfo[1:-1], 'html.parser')
    titles = ['Year of birth', 'Gender', 'Pronoun', 'Languages', 'Religous views']
    for title in titles:
        soup = BeautifulSoup(basicinfo[1:-1], 'html.parser')
        try:
            soup = soup.find('div', title=title)
            value = soup.find('div', class_='dw')
            print title+': '+value.text
        except AttributeError:
            return 0

def findpartner(session, target):

    '''
    Attempt to discern a targets partner. If not found, estimates partner by
    checking tagged photos. The person who is tagged the most in photos is 
    assumed to be the Partner. Not always accurate but useful information anyways.
    '''
    print 'Attempting to find a possible partner...'


session = requests.session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:39.0) Gecko/20100101 Firefox/57.0'
})

try:
    fb_dtsg, user_id, xs = login(session, sys.argv[1], sys.argv[2])
except TypeError:
    print "TypeError occured\nUsually due to incorrect login information"
except IndexError:
    print "Not enough information is given.\nformat ./facebook.py [username] [password] [target]"
    quit()
try:
    getbasicinfo(session, sys.argv[3])
except IndexError:
    print "Not enough information is given.\nformat ./facebook.py [username] [password] [target]"
try:
    findpartner(session, sys.argv[3])


