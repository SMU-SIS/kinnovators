"""Backend Module

Created on Dec 6, 2012
@author: Chris Boesch
@modified: Goh Kian Wei (Brandon)
"""
"""
Note to self: json.loads = json string to objects. json.dumps is object to json string.
"""
import datetime
import logging

import webapp2 as webapp

from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext.webapp.util import run_wsgi_app

import json

"""
Attributes and functions for Sketch entity
"""
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
  def get_entities(offset=0, limit=50):
    #update ModelCount when adding
    theQuery = Sketch.all()
    #if model:
      #theQuery = theQuery.filter('model', model)

    objects = theQuery.fetch(limit=limit, offset=offset)

    entities = []
    for object in objects:
      data = {'sketchId': object.sketchId,
              'version': object.version,
              'changeDescription': object.changeDescription,
              'fileName': object.fileName,
              'owner': object.owner,
              'fileData': object.fileData,
              'original': object.original}
      entity = {'id': object.key().id(),
              'created': object.created,
              'modified': object.modified, 
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
  
class User(db.Model):
  user_name = db.StringProperty(required=True)
  full_name = db.StringProperty(required=True)
  email = db.StringProperty()
  pass_word = db.StringProperty(required=True)
  google_id = db.TextProperty()
  created = db.DateTimeProperty(auto_now_add=True) #The time that the model was created
  
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
  
class UserGroupMgmt(db.Model):
  user_id = db.IntegerProperty(required=True)
  group_id = db.IntegerProperty(required=True)
  role = db.StringProperty(required=True)
  
class ActionHandler(webapp.RequestHandler):
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

application = webapp.WSGIApplication([
    webapp.Route('/metadata', handler=ActionHandler, handler_method='metadata'),
    webapp.Route('/sketch/<model_id>/delete', handler=ActionHandler, handler_method='delete_sketch'), 
    webapp.Route('/sketch/<model_id>', handler=ActionHandler, handler_method='get_or_edit_sketch'), 
    webapp.Route('/sketch', handler=ActionHandler, handler_method='add_or_list_sketch'),
    ],
    debug=True)


