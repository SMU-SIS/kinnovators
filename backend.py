"""Backend Module

@created: Goh Kian Wei (Brandon)
@code_adapted_from: Chris Boesch, Daniel Tsou
"""
"""
Note to self: json.loads = json string to objects. json.dumps is object to json string.
"""
import datetime
import logging
import os
import urllib
import urllib2

import webapp2
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app

import json

"""
Attributes and functions for User entity (incl. Janrain login)
"""
    
#class User(db.Model):
  #user_name = db.StringProperty(required=True)
  #full_name = db.StringProperty()
  #email = db.StringProperty()
  #pass_word = db.StringProperty()
  #google_id = db.TextProperty()
  #created = db.DateTimeProperty(auto_now_add=True) #The time that the model was created

"""
Attributes and functions for Sketch entity
"""

class UTC(datetime.tzinfo):
  def utcoffset(self, dt):
    return datetime.timedelta(hours=0)
    
  def dst(self, dt):
    return datetime.timedelta(0)
    
  def tzname(self, dt):
    return "UTC"

class Sketch(db.Model):
  #Use backend record id as the model id for simplicity
  sketchId = db.IntegerProperty(required=True)
  version = db.IntegerProperty(required=True)
  changeDescription = db.StringProperty()
  fileName = db.StringProperty(required=True)
  owner = db.StringProperty(required=True) #might be changed
  fileData = db.TextProperty(required=True)
  original = db.StringProperty(required=True) #might be changed
  created = db.DateTimeProperty(auto_now_add=True) #The time that the model was created    
  modified = db.DateTimeProperty(auto_now=True)
  
  def to_dict(self):
       d = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       d["id"] = self.key().id()
       return d

      
  @staticmethod
  def add(data):
    #update ModelCount when adding
    jsonData = json.loads(data)
    modelCount = ModelCount.all().filter('en_type','Sketch').get()
    
    #For sketch files saved through "Save As"
    if jsonData['sketchId'] == '':
      if modelCount:
        modelCount.count += 1
        modelCount.put()
      else:
        modelCount = ModelCount(en_type='Sketch', count=1)
        modelCount.put()
      jsonData['sketchId'] = str(modelCount.count)
    #For sketch files saved through "Save As" that were not derived from another file  
    if jsonData['original'] == ':':
      jsonData['original'] = 'original'
    
    #update VersionCount when adding  
    versionCount = VersionCount.all().filter('sketchId', long(jsonData['sketchId'])).get()
    if versionCount:
      versionCount.lastVersion += 1
      versionCount.put()
    else:
      versionCount = VersionCount(sketchId=long(jsonData['sketchId']), lastVersion=1)
      versionCount.put()
    
    jsonData['version'] = str(versionCount.lastVersion)
     
    entity = Sketch(sketchId=long(jsonData['sketchId']),
                    version=long(jsonData['version']),
                    changeDescription=jsonData['changeDescription'],
                    fileName=jsonData['fileName'],
                    owner=jsonData['owner'],
                    fileData=jsonData['fileData'],
                    original=jsonData['original'])
    
    entity.put()
    
    result = {'id': entity.key().id(), 
              'data': jsonData} #this would also check if the json submitted was valid
        
    return result
  
  @staticmethod
  def get_entities(offset=0, limit=50, criteria=""):
    utc = UTC()
    #update ModelCount when adding
    theQuery = Sketch.all()
    #if model:
      #theQuery = theQuery.filter('model', model)

    objects = theQuery.fetch(limit=limit, offset=offset)

    entities = []
    for object in objects:
      include = True
      if criteria != "":
        #Change this soon!
        if criteria.lower() in object.fileName.lower():
          include = True
        elif criteria.lower() in object.owner.lower():
          include = True
        else:
          include = False
          
      if include:
        data = {'sketchId': object.sketchId,
              'version': object.version,
              'changeDescription': object.changeDescription,
              'fileName': object.fileName,
              'owner': object.owner,
              'fileData': object.fileData,
              'original': object.original}
        entity = {'id': object.key().id(),
              'created': object.created.replace(tzinfo=utc).strftime("%Y-%m-%d %H:%M:%S"),
              'modified': object.modified.replace(tzinfo=utc).strftime("%Y-%m-%d %H:%M:%S"), 
              'data': data}
        entities.append(entity)
    
    count = 0
    modelCount = ModelCount.all().filter('en_type','Sketch').get()
    if modelCount:
      count = modelCount.count
    result = {'method':'get_entities',
              'en_type': 'Sketch',
              'count': count,
              'offset': offset,
              'limit':limit,
              'entities': entities}
    return result
    
  @staticmethod
  def get_entity(model_id):
    utc = UTC()
    theobject = Sketch.get_by_id(long(model_id))
    
    data = {'sketchId': theobject.sketchId,
              'version': theobject.version,
              'changeDescription': theobject.changeDescription,
              'fileName': theobject.fileName,
              'owner': theobject.owner,
              'fileData': theobject.fileData,
              'original': theobject.original}
    
    result = {'method':'get_model',
                  'id': model_id,
                  'created': theobject.created.replace(tzinfo=utc).strftime("%Y-%m-%d %H:%M:%S"),
                  'modified': theobject.modified.replace(tzinfo=utc).strftime("%Y-%m-%d %H:%M:%S"), 
                  'data': data
                  }
    return result
  
  @staticmethod
  def clear():
    #update model count when clearing model on api
    count = 0
    for object in Sketch.all():
      count += 1
      object.delete()
      
    modelCount = ModelCount.all().filter('en_type','Sketch').get()
    if modelCount:
      modelCount.delete()
    result = {'items_deleted': count}
    return result
  
  #You can't name it delete since db.Model already has a delete method
  @staticmethod
  def remove(model_id):
    #update model count when deleting
    entity = Sketch.get_by_id(long(model_id))
    
    if entity:
        entity.delete()
    
        result = {'method':'delete_model_success',
                  'id': model_id
                  }
    else:
        result = {'method':'delete_model_not_found'}
        
    modelCount = ModelCount.all().filter('en_type','Sketch').get()
    if modelCount:
        modelCount.count -= 1
        modelCount.put()
    
    return result

  #data is a dictionary that must be merged with current json data and stored. 
  @staticmethod
  def edit_entity(model_id, data):
    jsonData = json.loads(data)
    entity = Sketch.get_by_id(long(model_id))
    
    if jsonData['sketchId']!='':
      entity.sketchId=long(jsonData['sketchId'])
    if jsonData['version']!='':
      entity.version=long(jsonData['version'])
    if jsonData['changeDescription']!='':
      entity.changeDescription=jsonData['changeDescription']
    if jsonData['fileName']!='':
      entity.fileName=jsonData['fileName']
    if jsonData['owner']!='':
      entity.owner=jsonData['owner']
    if jsonData['fileData']!='':
      entity.fileData=jsonData['fileData']
    if jsonData['original']!='':
      entity.original=jsonData['original']
    entity.put()
    
    result = {'id': entity.key().id(), 
              'data': json.dumps(jsonData) #this would also check if the json submitted was valid
              }
    return result
    
#Quick retrieval for supported models metadata and count stats
class ModelCount(db.Model):
  en_type = db.StringProperty(required=True,default='Default-entype')
  count = db.IntegerProperty(required=True, default=0)
  
class VersionCount(db.Model):
  sketchId = db.IntegerProperty(required=True, default=0)
  lastVersion = db.IntegerProperty(required=True, default=0)
  
class Comment(db.Model):
  sketch_id = db.IntegerProperty(required=True)
  user_id = db.IntegerProperty(required=True)
  content = db.StringProperty(required=True)
  reply_to_id = db.IntegerProperty()
  created = db.DateTimeProperty(auto_now_add=True) #The time that the model was created
  
class Permissions(db.Model):
  sketch_id = db.IntegerProperty(required=True)
  view_private = db.BooleanProperty(required=True)
  view_public = db.BooleanProperty(required=True)
  view_group = db.TextProperty()
  view_user = db.TextProperty()
  edit_private = db.BooleanProperty(required=True)
  edit_public = db.BooleanProperty(required=True)
  edit_group = db.TextProperty()
  edit_user = db.TextProperty()
  comment = db.BooleanProperty(required=True)
  
class Group(db.Model):
  group_name = db.StringProperty(required=True)
  group_sketches = db.TextProperty()
  created = db.DateTimeProperty(auto_now_add=True) #The time that the model was created
  
  def to_dict(self):
       d = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       d["id"] = self.key().id()
       return d

  @staticmethod
  def add(data):
    #update ModelCount when adding
    jsonData = json.loads(data)       
    if jsonData['group_name'] != '':
      if jsonData['user_id'] != '':
    
        entity = Group(group_name=jsonData['group_name'])
      
        entity.put()
        
        usergroupmgmt = UserGroupMgmt(user_id=int(jsonData['user_id']),
                                      group_id=entity.key().id(),
                                      role="Founder")
        usergroupmgmt.put()
        
    result = {'g_name': jsonData['group_name'],
              'u_id': jsonData['user_id'],
              'role': "Founder"}
              
    return result
    
  @staticmethod
  def get_name(model_id):
    try:
      entity = Group.get_by_id(int(model_id))
      
      if entity:
        return entity.group_name
      else:
        return "N/A"
    except ValueError:
      return "N/A"
      
  @staticmethod
  def get_entities(criteria=""):
    utc = UTC()
    theQuery = UserGroupMgmt.all()
    objects = theQuery.run()
    group = ""
    entities = []
    for object in objects:
      include = True
      if criteria != "":
        #Change this soon!
        if int(criteria) == object.user_id:
          include = True
        else:
          include = False
          
      if include:
        group = Group.get_name(object.group_id)
        data = {'group_name': group,
              'user': object.user_id, #placeholder
              'role': object.role}
        entity = {'id': object.group_id, 
              'data': data}
        entities.append(entity)
    result = {'method':'get_entities',
              'en_type': 'Group',
              'entities': entities}
    return result
    
  @staticmethod
  def get_entity(model_id):
    utc = UTC()
    theobject = Group.get_by_id(long(model_id))
    
    user_groups_query = UserGroupMgmt.all().filter('group_id', theobject.key().id()).run()
    u_groups = []
    
    if user_groups_query:
      for u_g in user_groups_query:
        u_entity = {'user': u_g.user_id, #placeholder
              'role': u_g.role}
        u_groups.append(u_entity)    
    
    result = {'method':'get_entity',
                  'id': model_id,
                  'group_name': theobject.group_name,
                  'u_groups': u_groups
                  }
    return result    
  
class UserGroupMgmt(db.Model):
  user_id = db.IntegerProperty(required=True)
  group_id = db.IntegerProperty(required=True)
  role = db.StringProperty(required=True)
  
class ActionHandler(webapp2.RequestHandler):
    """Class which handles bootstrap procedure and seeds the necessary
    entities in the datastore.
    """
        
    def respond(self,result):
        """Returns a JSON response to the client.
        """
        callback = self.request.get('callback')
        self.response.headers['Content-Type'] = 'application/json'
        #self.response.headers['Content-Type'] = '%s; charset=%s' % (config.CONTENT_TYPE, config.CHARSET)
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH, HEAD'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, X-Requested-With'
        self.response.headers['Access-Control-Allow-Credentials'] = 'True'

        #Add a handler to automatically convert datetimes to ISO 8601 strings. 
        dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
        if callback:
            content = str(callback) + '(' + json.dumps(result,default=dthandler) + ')'
            return self.response.out.write(content)
            
        return self.response.out.write(json.dumps(result,default=dthandler)) 

    def metadata(self):
        #Fetch all ModelCount records to produce metadata on currently supported models. 
        models = []
        for mc in ModelCount.all():
          models.append({'model':mc.model, 'count': mc.count})
    
        result = {'method':'metadata',
                  'model': "metadata",
                  'count': len(models),
                  'entities': models
                  } 
        
        return self.respond(result)

    def add_or_list_sketch(self):
        #Check for GET paramenter == model to see if this is an add or list. 
        #Call Sketch.add(model, data) or
        #Fetch all models and return a list. 
                
        #Todo - Check for method.
        logging.info(self.request.method)
        if self.request.method=="POST":
          logging.info("in POST")
          logging.info(self.request.body)
          result = Sketch.add(self.request.body)
          #logging.info(result)
          return self.respond(result)
    
        else:
          data = self.request.get("obj")
          if data: 
            logging.info("Adding new data: "+data)
            result = Sketch.add(data)
          else:
            offset = 0
            new_offset = self.request.get("offset")
            if new_offset:
              offset = int(new_offset)

            result = Sketch.get_entities(offset=offset)
          
          return self.respond(result)

    def delete_sketch(self, model_id):
        result = Sketch.remove(model_id)
        
        return self.respond(result)
      
    def get_or_edit_sketch(self, model_id):
        #Check for GET parameter == model to see if this is a get or an edit
        logging.info("**********************")
        logging.info(self.request.method)
        logging.info("**********************")

        if self.request.method=="DELETE":
          logging.info("It was options")
          result = Sketch.remove(model_id)
          logging.info(result)
          return self.respond(result)#(result)
        
        elif self.request.method=="PUT":
          logging.info("It was PUT")
          logging.info(self.request.body)
          result = Sketch.edit_entity(model_id,self.request.body)
          return self.respond(result)#(result)          
        else:
          data = self.request.get("obj")
          if data:
              result = Sketch.edit_entity(model_id,data)
          else:
              result = Sketch.get_entity(model_id)
          return self.respond(result) 
          
    def search_sketch(self, criteria):
        #Check for GET parameter == model to see if this is a get or an edit
        logging.info("**********************")
        logging.info(self.request.method)
        logging.info("**********************")

        offset = 0
        new_offset = self.request.get("offset")
        if new_offset:
          offset = int(new_offset)

        result = Sketch.get_entities(offset=offset, criteria=criteria)
        return self.respond(result)
      
    def list_sketch(self):
        #Check for GET parameter == model to see if this is a get or an edit
        logging.info("**********************")
        logging.info(self.request.method)
        logging.info("**********************")

        offset = 0
        new_offset = self.request.get("offset")
        if new_offset:
          offset = int(new_offset)

        result = Sketch.get_entities(offset=offset)
        return self.respond(result)
      
    def get_sketch(self, model_id):
        #Check for GET parameter == model to see if this is a get or an edit
        logging.info("**********************")
        logging.info(self.request.method)
        logging.info("**********************")

        data = self.request.get("obj")
        if data:
          result = Sketch.edit_entity(model_id,data)
        else:
          result = Sketch.get_entity(model_id)
        return self.respond(result) 
        
    def add_group(self):
        #Check for GET paramenter == model to see if this is an add or list. 
        #Call Sketch.add(model, data) or
        #Fetch all models and return a list. 
                
        #Todo - Check for method.
        logging.info(self.request.method)
        if self.request.method=="POST":
          logging.info("in POST")
          logging.info(self.request.body)
          result = Group.add(self.request.body)
          #logging.info(result)
          return self.respond(result)
    
        else:
          data = self.request.get("obj")
          if data: 
            logging.info("Adding new data: "+data)
            result = Group.add(data)
          return self.respond(result)

    def get_group(self, model_id):
        #Check for GET parameter == model to see if this is a get or an edit
        logging.info("**********************")
        logging.info(self.request.method)
        logging.info("**********************")

        result = Group.get_entity(model_id)
        return self.respond(result) 

    def user_group(self, criteria):
        #Check for GET parameter == model to see if this is a get or an edit
        logging.info("**********************")
        logging.info(self.request.method)
        logging.info("**********************")

        offset = 0
        new_offset = self.request.get("offset")
        if new_offset:
          offset = int(new_offset)

        result = Group.get_entities(criteria=criteria)
        return self.respond(result)
        
application = webapp2.WSGIApplication([
    webapp2.Route('/metadata', handler=ActionHandler, handler_method='metadata'),
    webapp2.Route('/sketch/<model_id>/delete', handler=ActionHandler, handler_method='delete_sketch'), 
    webapp2.Route('/sketch/<model_id>', handler=ActionHandler, handler_method='get_or_edit_sketch'), 
    webapp2.Route('/sketch', handler=ActionHandler, handler_method='add_or_list_sketch'), 
    webapp2.Route('/list/sketch', handler=ActionHandler, handler_method='list_sketch'), 
    webapp2.Route('/list/sketch/<criteria>', handler=ActionHandler, handler_method='search_sketch'),
    webapp2.Route('/get/sketch/<model_id>', handler=ActionHandler, handler_method='get_sketch'),
    webapp2.Route('/group', handler=ActionHandler, handler_method='add_group'), 
    webapp2.Route('/get/group/<model_id>', handler=ActionHandler, handler_method='get_group'),
    webapp2.Route('/list/group/<criteria>', handler=ActionHandler, handler_method='user_group')
    ],
    debug=True)
