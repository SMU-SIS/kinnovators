import datetime
import logging
import os
import urllib

import json

from backend import User

from google.appengine.api import urlfetch
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from gaesessions import get_current_session

BASE_URL = 'k-sketch-test.appspot.com' # Change based on host url
LOGIN_IFRAME = '<iframe src="http://k-sketch.rpxnow.com/openid/embed?token_url=http%3A%2F%2F' + BASE_URL + '%2Frpx_response" scrolling="no" frameBorder="no" allowtransparency="true" style="width:400px;height:240px"></iframe>'

def redirect_with_msg(h, msg, dst='/'):
    get_current_session()['msg'] = msg
    h.redirect(dst)
    
class JanrainHandler(webapp.RequestHandler):
  def post(self):
    token = self.request.get('token')
    url = 'https://rpxnow.com/api/v2/auth_info'
    args = {
        'format': 'json',
        'apiKey': 'insert API key here',
        'token': token
    }
    r = urlfetch.fetch(url=url,
                       payload=urllib.urlencode(args),
                       method=urlfetch.POST,
                       headers={'Content-Type':'application/x-www-form-urlencoded'})
    json_data = json.loads(r.content)
      
    session = get_current_session()
    if session.is_active():
      session.terminate()
        
    if json_data['stat'] == 'ok':
      info = json_data['profile']
      oid = info['identifier']
      email = info.get('email', '')
      try:
        user_name = info['displayName']
      except KeyError:
        user_name = email.partition('@')[0]
        
      user = MyUser.get_or_insert(oid, user_name=user_name, email=email)
      
      session['current'] = user
      
      redirect_with_msg(self, 'success!')
    else:  
      redirect_with_msg(self, 'Error in logging in!')
      
class GetUser(webapp.RequestHandler):
  def get(self):
    session = get_current_session()
    d = dict()
    if session.has_key('msg'):
      d['login'] = False
      d['msg'] = session['msg']
      del session['msg']
      
    callback = self.request.get('callback')
    if callback:
      content = str(callback) + '(' + json.dumps(d) + ')'
      return self.response.out.write(content)
      
    return self.response.out.write(json.dumps(d))
    
class Logout(webapp.RequestHandler):
  def get(self):
    session = get_current_session()
    if session.has_key('current'):
      user = session['current']
      user.put()
      session.terminate()
      redirect_with_msg(self, 'Logout complete - goodbye, ' + user.display_name)
    else:
      redirect_with_msg(self, "You can't log out if you weren't logged in,")
      
application = webapp.WSGIApplication([('/getuser', GetUser),
                                    ('/logout', Logout),
                                    ('/janrain', JanrainHandler),
                                    ])
    
def main(): run_wsgi_app(application)
if __name__ == '__main__': main()      