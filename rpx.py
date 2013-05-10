import datetime
import hashlib
import os
import urllib
import urllib2
import webapp2
import logging

from webapp2_extras import auth
from webapp2_extras import sessions
from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError

import json

from google.appengine.api import urlfetch
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

# configure the RPX iframe to work with the server were on (dev or real)
ON_LOCALHOST = ('Development' == os.environ['SERVER_SOFTWARE'][:11])
if ON_LOCALHOST:
    import logging
    if os.environ['SERVER_PORT'] == '80':
        BASE_URL = 'localhost'
    else:
        BASE_URL = 'localhost:%s' % os.environ['SERVER_PORT']
else:
    BASE_URL = 'k-sketch-test.appspot.com'
LOGIN_IFRAME = '<iframe src="http://gae-sesssions-demo.rpxnow.com/openid/embed?token_url=http%3A%2F%2F' + BASE_URL + '%2Frpx_response" scrolling="no" frameBorder="no" allowtransparency="true" style="width:400px;height:240px"></iframe>'

class UTC(datetime.tzinfo):
  def utcoffset(self, dt):
    return datetime.timedelta(hours=0)
    
  def dst(self, dt):
    return datetime.timedelta(0)
    
  def tzname(self, dt):
    return "UTC"

# create our own simple users model to track our user's data
class User(db.Model):
  email           = db.EmailProperty()
  display_name    = db.StringProperty()
  real_name       = db.StringProperty()
  created         = db.DateTimeProperty(auto_now_add=True)
  modified        = db.DateTimeProperty(auto_now=True)

  def to_dict(self):
       d = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       d["id"] = self.key().id()
       return d
       
  @staticmethod
  def get_name(model_id):
    #Retrieves display name
    if int(model_id) == 0:
      return "Anonymous User"
    else:
      try:
        entity = User.get_by_id(int(model_id))
        
        if entity:
          return entity.display_name
        else:
          return "N/A"
      except ValueError:
        return "N/A"    
      
  @staticmethod
  def search_users_by_name(user_string):
    theQuery = User.all()
    objects = theQuery.run()
    entities = []
    if user_string != "":
      if user_string.lower() in "Anonymous User".lower():
        entities.append(0)
      for object in objects:
        include = True
        if user_string.lower() in object.display_name.lower():
          include = True
        else:
          include = False
        
        if include:
          entities.append(object.key().id())
          
    return entities
    
  @staticmethod
  def edit_entity(model_id, data):
    jsonData = json.loads(data)
    entity = User.get_by_id(long(model_id))
    result = {'method':'edit_entity',
              'model':'User',
              'success':False}
    if entity:
      if jsonData['u_realname']:
        entity.realname = jsonData['u_realname']
        #Other fields to be added as necessary.
      entity.put()
    
      result = {'method':'edit_entity',
              'model':'User',
              'success':True}
              
    return result
    
class BaseHandler(webapp2.RequestHandler):
    """
      BaseHandler for all requests
       Holds the auth and session properties so they are reachable for all requests
    """

    def dispatch(self):
      """
        Save the sessions for preservation across requests
      """
      try:
          response = super(BaseHandler, self).dispatch()
          self.response.write(response)
      finally:
          self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def auth(self):
        return auth.get_auth()

    @webapp2.cached_property
    def session_store(self):
        return sessions.get_store(request=self.request)
    
    @webapp2.cached_property
    def session(self):
      # Returns a session using the default cookie key.
      return self.session_store.get_session()

    @webapp2.cached_property
    def auth_config(self):
      """
        Dict to hold urls for login/logout
      """
      return {
          'login_url': '/index.html',
          'logout_url': '/index.html'
      }    
    
class RPXTokenHandler(BaseHandler):
    """Receive the POST from RPX with our user's login information."""
    def post(self):
        token = self.request.get('token')
        url = 'https://rpxnow.com/api/v2/auth_info'
        args = {
            'format': 'json',
            'apiKey': '5fa9fabfa1141896e2d4025efd640ea5c1f54776',
            'token': token
        }
        r = urlfetch.fetch(url=url,
                           payload=urllib.urlencode(args),
                           method=urlfetch.POST,
                           headers={'Content-Type':'application/x-www-form-urlencoded'})
        json_data = json.loads(r.content)

        if json_data['stat'] == 'ok':
          # extract some useful fields
          info = json_data['profile']
          oid = info['identifier']
          email = info.get('email', '')
          try:
            display_name = info['displayName']
          except KeyError:
            display_name = email.partition('@')[0]

          # check if there is a user present with that auth_id
          user = self.auth.store.user_model.get_by_auth_id(oid)
          if not user:
            success, user = self.auth.store.user_model.create_user(oid, email=email, display_name=display_name, real_name=display_name)
            logging.info('New user created in the DS')
            
          userid = user.get_id()
          token = self.auth.store.user_model.create_auth_token(userid)
          self.auth.get_user_by_token(userid, token)
          logging.info('The user is already present in the DS')
          
          # assign a session
          self.session.add_flash('You have successfully logged in', 'success')
          self.redirect('/')
        else:
          self.session.add_flash('There was an error while processing the login', 'error')
          self.redirect('/')

class GetUser(webapp2.RequestHandler):

    @webapp2.cached_property
    def auth(self):
        return auth.get_auth()
        
    def edit(self, **kwargs):
      utc = UTC()
      jsonData = json.loads(self.request.body)
      auser = self.auth.get_user_by_session()
      result = {'method':'edit_entity',
              'model':'User',
              'success':False}
      if auser:
        userid = auser['user_id']
        if userid:
          result = User.get_by_id(userid)
          
      result = json.dumps(result)
                        
      callback = self.request.get('callback')
      self.response.headers['Content-Type'] = 'application/json'
      self.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD'
        
      if callback:
        content = str(callback) + '(' + str(result) + ')'
        return self.response.out.write(content)
      
      return self.response.out.write(result)    
    
    def get(self, **kwargs):
      utc = UTC()
      result = {'id': 0,
                'u_login': "Not logged in",
                'u_name': "Anonymous User",
                'u_realname': "Anonymous User",
                'u_email': "",
                'g_hash': "",
                'u_created': ""}
      auser = self.auth.get_user_by_session()
      if auser:
        userid = auser['user_id']
        if userid:
          user = User.get_by_id(userid)
          if user:
            email_hasher = hashlib.md5()
            email_hasher.update(user.email.lower())
            g_hash = email_hasher.hexdigest()
            if (not user.real_name):
              user.real_name = user.display_name #default to display name
              user.put()
            result = {'id': userid,
                      'u_login': bool(True),
                        'u_name': user.display_name,
                        'u_realname': user.real_name,
                        'u_email': user.email,
                        'g_hash': g_hash,
                        'u_created': user.created.replace(tzinfo=utc).strftime("%d %b %Y %H:%M:%S")}
            result = json.dumps(result)
                        
      callback = self.request.get('callback')
      self.response.headers['Content-Type'] = 'application/json'
      self.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD'
        
      if callback:
        content = str(callback) + '(' + str(result) + ')'
        return self.response.out.write(content)
      
      return self.response.out.write(result)    
    
    def get_by_id(self, id, **kwargs):
      utc = UTC()
      result = {'id': 0,
                'u_login': "Not logged in",
                'u_name': "Anonymous User",
                'u_realname': "Anonymous User",
                'u_email': "",
                'g_hash': "",
                'u_created': ""}
      auser = self.auth.get_user_by_session()
      if auser:
        user = User.get_by_id(id)
        if user:
          email_hasher = hashlib.md5()
          email_hasher.update(user.email.lower())
          g_hash = email_hasher.hexdigest()
          if (not user.real_name):
            user.real_name = user.display_name #default to display name
            user.put()
          result = {'id': userid,
                    'u_login': bool(True),
                      'u_name': user.display_name,
                      'u_realname': user.real_name,
                      'u_email': user.email,
                      'g_hash': g_hash,
                      'u_created': user.created.replace(tzinfo=utc).strftime("%d %b %Y %H:%M:%S")}
          result = json.dumps(result)
                        
      callback = self.request.get('callback')
      self.response.headers['Content-Type'] = 'application/json'
      self.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD'
        
      if callback:
        content = str(callback) + '(' + str(result) + ')'
        return self.response.out.write(content)
      
      return self.response.out.write(result) 
      
class LogoutPage(BaseHandler):
    def get(self):
      self.auth.unset_session()
      # User is logged out, let's try redirecting to login page
      try:
          self.redirect(self.auth_config['login_url'])
      except (AttributeError, KeyError), e:
          return "User is logged out"

webapp2_config = {}
webapp2_config['webapp2_extras.sessions'] = {
		'secret_key': 'n\xd99\xd4\x01Y\xea5/\xd0\x8e\x1ba\\:\x91\x10\x16\xbcTA\xe0\x87lf\xfb\x0e\xd2\xc4\x15\\\xaf\xb0\x91S\x12_\x86\t\xadZ\xae]\x96\xd0\x11\x80Ds\xd5\x86.\xbb\xd5\xcbb\xac\xc3T\xaf\x9a+\xc5',
	}

application = webapp2.WSGIApplication([
    webapp2.Route('/getuser', handler=GetUser, handler_method='get'),
    webapp2.Route('/getuser/<id>', handler=GetUser, handler_method='get_by_id'),
    webapp2.Route('/edituser', handler=GetUser, handler_method='edit'),
    webapp2.Route('/logout', handler=LogoutPage),
    webapp2.Route('/janrain', handler=RPXTokenHandler)],
    config=webapp2_config,
    debug=True)