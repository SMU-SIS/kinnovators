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

from webapp2_extras import auth
from webapp2_extras import sessions
from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError

import webapp2
from google.appengine.api import memcache
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import json
from rpx import User
from rpx import AppUserCount

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

#Handles Sketch data, and saving and loading of sketches
class Sketch(db.Model):
  #Use backend record id as the model id for simplicity
  sketchId = db.IntegerProperty(required=True)
  version = db.IntegerProperty(required=True)
  changeDescription = db.StringProperty()
  fileName = db.StringProperty(required=True)
  owner = db.IntegerProperty(required=True)
  fileData = db.TextProperty(required=True)
  thumbnailData = db.TextProperty()
  original_sketch = db.IntegerProperty(required=True) #might be changed
  original_version = db.IntegerProperty(required=True)
  created = db.DateTimeProperty(auto_now_add=True) #The time that the model was created    
  modified = db.DateTimeProperty(auto_now=True)
  appver = db.FloatProperty()
  
  def to_dict(self):
       d = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       d["id"] = self.key().id()
       return d

      
  @staticmethod
  def add(data):
    result = {}
    try:
      #update ModelCount when adding
      jsonData = json.loads(data)
      if jsonData['fileName'].strip() != "":
        modelCount = ModelCount.get_counter()
        
        #For sketch files saved through "Save As"
        if jsonData['sketchId'] == "":
          ModelCount.increment_counter()
          jsonData['sketchId'] = str(modelCount.count)
        # #For sketch files saved through "Save As" that were not derived from another file - this might be changed. 
        
        #update VersionCount when adding  
        versionCount = VersionCount.get_and_increment_counter(long(jsonData['sketchId']))
        
        check_original = False
        if jsonData['originalVersion'] == "":
          if jsonData['originalSketch'] == "":
            check_original = True
            jsonData['originalVersion'] = versionCount
            jsonData['originalSketch'] = str(modelCount.count)
        
        #update AppVersionCount when adding
        AppVersionCount.increment_counter(float(jsonData['appver']), check_original)
        
        jsonData['version'] = str(versionCount)
        file = jsonData['fileData']
        thumbnail = jsonData['thumbnailData']
        change = jsonData['changeDescription']
        change = change[:255]
          
        entity = Sketch(sketchId=long(jsonData['sketchId']),
                        version=long(jsonData['version']),
                        changeDescription=change,
                        fileName=jsonData['fileName'],
                        owner=long(jsonData['owner_id']),
                        fileData=file,
                        thumbnailData=thumbnail,
                        original_sketch=long(jsonData['originalSketch']),
                        original_version=long(jsonData['originalVersion']),
                        appver=float(jsonData['appver']))
        
        verify = entity.put()
        
        if (verify):
        
          permissions_key = Permissions.add(entity.key().id(),
                                            bool(long(jsonData['p_view'])),
                                            bool(jsonData['p_edit']),
                                            bool(jsonData['p_comment']))
          #Update group permissions when adding
          
          group_count = 0
          try:
            if jsonData['group_permissions']:
              group_permissions = jsonData['group_permissions']
              for g_p in group_permissions:
                group_key = Sketch_Groups.add(entity.key().id(),
                                              long(g_p['group_id']),
                                              bool(g_p['edit']),
                                              bool(g_p['comment']))
                if group_key != -1:
                  group_count += 1
          except:
            group_count = 0
        
          if (permissions_key != -1):
            result = {'id': entity.key().id(), 
                      'status': "success",
                      'data': jsonData} #this would also check if the json submitted was valid
          
          else:
            #Rollback
            rollback = Sketch.get_by_id(entity.key.id())
            if rollback:
              rollback.delete()
            result = {'status': "error",
                     'message': "Save unsuccessful. Please try again."}
          
        else:
          result = {'status': "error",
                    'message': "Save unsuccessful. Please try again."}

      else:
        result = {'status': "error",
                  'message': "Save unsuccessful. Please try again."}
    except:
     result = {'status': "error",
               'message': "Save unsuccessful. Please try again."}
    
    return result
  
  @staticmethod
  def get_entities(criteria="", userid=""):
    utc = UTC()
    #update ModelCount when adding
    theQuery = Sketch.all()
    #if model:
      #theQuery = theQuery.filter('model', model)

    objects = theQuery.run()

    entities = []
    possible_users = User.get_matching_ids(criteria)
    count = 0
    for object in objects:
      include = True
      if criteria != "":
        include = False
        if criteria.lower() in object.fileName.lower():
          include = True
        if object.owner in possible_users:
          include = True
        
      if include:
        #Check Permissions
        permissions = Permissions.user_access_control(object.key().id(),userid)
          
        if bool(permissions['p_view']):
          user_name = User.get_name(object.owner)
          data = {'sketchId': object.sketchId,
                'version': object.version,
                'changeDescription': object.changeDescription,
                'fileName': object.fileName,
                'thumbnailData': object.thumbnailData,
                'owner': user_name,
                'owner_id': object.owner,
                'originalSketch': object.original_sketch,
                'originalVersion': object.original_version,
                'originalName': Sketch.get_sketch_name(object.original_sketch,object.original_version),
                'appver': object.appver,
                'p_view': 1,
                'p_edit': bool(permissions['p_edit']),
                'p_comment': bool(permissions['p_comment'])}
          
          entity = {'id': object.key().id(),
                'created': object.created.replace(tzinfo=utc).strftime("%d %b %Y %H:%M:%S"),
                'modified': object.modified.replace(tzinfo=utc).strftime("%d %b %Y %H:%M:%S"), 
                'data': data}
          
          entities.append(entity)
          count += 1
    
    result = {'method':'get_entities',
              'en_type': 'Sketch',
              'count': count,
              'entities': entities}
    return result

  @staticmethod
  def get_entities_by_id(criteria="",userid=""):
    utc = UTC()
    #update ModelCount when adding
    theQuery = Sketch.all()
    #if model:
      #theQuery = theQuery.filter('model', model)

    objects = theQuery.run()

    entities = []
    count = 0
    for object in objects:
      if long(criteria) == object.owner:
        #Check Permissions
        permissions = Permissions.user_access_control(object.key().id(),userid)
          
        if bool(permissions['p_view']):
          user_name = User.get_name(object.owner)
          data = {'sketchId': object.sketchId,
                'version': object.version,
                'changeDescription': object.changeDescription,
                'fileName': object.fileName,
                'thumbnailData': object.thumbnailData,
                'owner': user_name,
                'owner_id': object.owner,
                'originalSketch': object.original_sketch,
                'originalVersion': object.original_version,
                'originalName': Sketch.get_sketch_name(object.original_sketch,object.original_version),
                'appver': object.appver,
                'p_view': 1,
                'p_edit': bool(permissions['p_edit']),
                'p_comment': bool(permissions['p_comment'])}
          
          entity = {'id': object.key().id(),
                'created': object.created.replace(tzinfo=utc).strftime("%d %b %Y %H:%M:%S"),
                'modified': object.modified.replace(tzinfo=utc).strftime("%d %b %Y %H:%M:%S"), 
                'data': data}
          
          entities.append(entity)
          count += 1
    
    result = {'method':'get_entities_by_id',
              'en_type': 'Sketch',
              'count': count,
              'entities': entities}
    return result

  @staticmethod
  def get_entity_by_versioning(sketchId=-1,version=-1, purpose="View", userid=""):
    utc = UTC()
    versionmatch = True
    result = {'method':'get_entity_by_versioning',
                  'success':"no",
                  'id': 0,
                  'created': datetime.datetime.now().replace(tzinfo=utc).strftime("%d %b %Y %H:%M:%S"),
                  'modified': datetime.datetime.now().replace(tzinfo=utc).strftime("%d %b %Y %H:%M:%S"),
                  'data': ""
                  }
    
    try:
      #Retrieve Sketch with given Sketch ID and version
      query = Sketch.all()
      query.filter('sketchId =', long(sketchId)).filter('version =', long(version))
      
      theobject = query.get()
      
      #If unable to find Sketch, attempt to retrieve latest available version.
      if theobject is None:
        versionCount = VersionCount.get_counter(long(sketchId))
        if long(version) != -1:
          versionmatch = False
        
        if versionCount:
          query = Sketch.all()
          query.filter('sketchId =', long(sketchId)).filter('version =', long(versionCount.lastVersion))
          theobject = query.get()
      
      if theobject:
        #Check Permissions
        permissions = Permissions.user_access_control(theobject.key().id(),userid)
        
        #Check access type (view/edit):
        access = False
        if purpose == "Edit":
          access = bool(permissions['p_edit'])
        else:
          access = bool(permissions['p_view'])
        
        if access:
          user_name = User.get_name(theobject.owner)
          data = {'sketchId': theobject.sketchId,
                    'version': theobject.version,
                    'changeDescription': theobject.changeDescription,
                    'fileName': theobject.fileName,
                    'owner': user_name,
                    'owner_id': theobject.owner,
                    'fileData': theobject.fileData,
                    'thumbnailData': theobject.thumbnailData,
                    'originalSketch': theobject.original_sketch,
                    'originalVersion': theobject.original_version,
                    'originalName': Sketch.get_sketch_name(theobject.original_sketch,theobject.original_version),
                    'appver': theobject.appver,
                    'p_view': 1,
                    'p_edit': bool(permissions['p_edit']),
                    'p_comment': bool(permissions['p_comment']),
                    'p_public': Permissions.check_permissions(theobject.key().id()),
                    'groups': Sketch_Groups.get_groups_for_sketch(theobject.key().id())}
              
          result = {'method':'get_entity_by_versioning',
                      'success':"yes",
                      'id': theobject.key().id(),
                      'created': theobject.created.replace(tzinfo=utc).strftime("%d %b %Y %H:%M:%S"),
                      'modified': theobject.modified.replace(tzinfo=utc).strftime("%d %b %Y %H:%M:%S"), 
                      'data': data
                      }
          if not versionmatch:
            result['success'] = "version"

        else:
          result = {'method':'get_entity_by_versioning',
                        'success':"no",
                        'id': "Forbidden"
                        }
    except (RuntimeError, ValueError):
      result['data'] = ""
      
    return result

  @staticmethod
  def get_entity_by_group(groupId=-1,userid=""):
    utc = UTC()
    result = {'method':'get_entity_by_group',
                  'success':"no",
                  'id': 0,
                  'created': datetime.datetime.now().replace(tzinfo=utc).strftime("%d %b %Y %H:%M:%S"),
                  'modified': datetime.datetime.now().replace(tzinfo=utc).strftime("%d %b %Y %H:%M:%S"),
                  'data': ""
                  }
    group_sketches = Sketch_Groups.get_sketches_for_group(long(groupId))
    entities = []
    count = 0
    en_type = "Welp"
    for g_s in group_sketches:
      en_type = "Sketch"
      sketch_model_id = long(g_s['sketch_model_id'])
      permissions = Permissions.user_access_control(sketch_model_id, userid)
      #if permissions['p_view']:
      en_type = en_type + "h"
      theobject = Sketch.get_by_id(sketch_model_id)
      user_name = User.get_name(theobject.owner)
      data = {'sketchId': theobject.sketchId,
                'version': theobject.version,
                'changeDescription': theobject.changeDescription,
                'fileName': theobject.fileName,
                'owner': user_name,
                'owner_id': theobject.owner,
                'thumbnailData': theobject.thumbnailData,
                'originalSketch': theobject.original_sketch,
                'originalVersion': theobject.original_version,
                'originalName': Sketch.get_sketch_name(theobject.original_sketch,theobject.original_version),
                'appver': theobject.appver,
                'p_view': 1,
                'p_edit': bool(permissions['p_edit']),
                'p_comment': bool(permissions['p_comment']),
                'g_edit': bool(g_s['edit']),
                'g_comment': bool(g_s['comment'])}
                
      entity = {'id': theobject.key().id(),
            'created': theobject.created.replace(tzinfo=utc).strftime("%d %b %Y %H:%M:%S"),
            'modified': theobject.modified.replace(tzinfo=utc).strftime("%d %b %Y %H:%M:%S"), 
            'data': data}
      entities.append(entity)
      count += 1
    result = {'method':'get_entity_by_group',
              'en_type': en_type,
              'count': count,
              'entities': entities}
    return result
    
  @staticmethod
  def check_if_owner(id = 0, user_id = 0):
    is_owner = False
    try:
      object = Sketch.get_by_id(long(id))
      if object:
        if object.owner == long(user_id):
          is_owner = True
    except ValueError:
      is_owner = False
    return is_owner
    
  @staticmethod
  def get_sketch_name(sketchId=-1,version=-1):
    try:
      object = Sketch.all().filter('sketchId =', long(sketchId)).filter('version =', long(version)).get()
      if object:
        return object.fileName
      else:
        return "N/A"
    except:
      return "N/A"
    
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
  def remove(sketch_model_id, user_id):
    #Only the sketch owner or an admin may delete the sketch
    can_delete = False
    is_admin = User.check_if_admin(user_id)
    is_owner = Sketch.check_if_owner(long(sketch_model_id), user_id)
    if is_owner:
      can_delete = True
    elif is_admin:
      can_delete = True
      
    if can_delete:
      entity = Sketch.get_by_id(long(sketch_model_id))
      
      if entity:
        appver = entity.appver
        fileName = entity.fileName
        owner = entity.owner
        check_original = False
        if entity.sketchId == entity.original_sketch:
          if entity.version == entity.original_version:
            check_original = True
            
        entity.delete()
        AppVersionCount.decrement_counter(appver, check_original)
        Comment.delete_by_sketch(long(sketch_model_id))
        Permissions.delete_by_sketch(long(sketch_model_id))
        Sketch_Groups.delete_by_sketch(long(sketch_model_id))
        Like.delete_by_sketch(long(sketch_model_id))
        
        if is_admin and not is_owner:
          
          notify = Notification(user_id = owner,
                                notification_type = "ADMINDELETE",
                                other_user = 0,
                                other_info = fileName,
                                relevant_id = 0)
                                
          notify.put()
          
        
    
        result = {'method':'remove',
                  'id': sketch_model_id,
                  'status': 'success'
                    }
      else:
          result = {'method':'remove',
                    'id': sketch_model_id,
                    'status': 'error'}
          
    else:
      result = {'method':'remove',
                    'id': sketch_model_id,
                    'status': 'error'}
    
    return result

  #data is a dictionary that must be merged with current json data and stored. 
  @staticmethod
  def edit_entity(sketch_model_id, data):
    jsonData = json.loads(data)
    entity = Sketch.get_by_id(long(sketch_model_id))
    
    if jsonData['sketchId']!='':
      entity.sketchId=long(jsonData['sketchId'])
    if jsonData['version']!='':
      entity.version=long(jsonData['version'])
    if jsonData['changeDescription']!='':
      entity.changeDescription=jsonData['changeDescription']
    if jsonData['fileName']!='':
      entity.fileName=jsonData['fileName']
    if jsonData['owner']!='':
      entity.owner=long(jsonData['owner'])
    if jsonData['fileData']!='':
      entity.fileData=jsonData['fileData']
    if jsonData['thumbnail']!='':
      entity.thumbnailData=jsonData['thumbnail']
    if jsonData['originalSketch']!='':
      entity.original_sketch=long(jsonData['originalSketch'])
    if jsonData['originalVersion']!='':
      entity.original_version=long(jsonData['originalVersion'])
    if jsonData['appver']!='':
      entity.appver=float(jsonData['appver'])
    entity.put()
    
    result = {'id': entity.key().id(), 
              'data': json.dumps(jsonData) #this would also check if the json submitted was valid
              }
    return result
    
#Quick retrieval for supported models metadata and count stats
class ModelCount(db.Model):
  en_type = db.StringProperty(required=True,default='Default-entype')
  count = db.IntegerProperty(required=True, default=0)
  
  def to_dict(self):
       d = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       d["id"] = self.key().id()
       return d
  
  @staticmethod
  def get_counter():
    return ModelCount.all().filter('en_type','Sketch').get()
  
  @staticmethod
  def increment_counter():
    modelCount = ModelCount.all().filter('en_type','Sketch').get()
    if modelCount:
      modelCount.count += 1
      modelCount.put()
    else:
      modelCount = ModelCount(en_type='Sketch', count=1)
      modelCount.put()
  
class VersionCount(db.Model):
  sketchId = db.IntegerProperty(required=True, default=0)
  lastVersion = db.IntegerProperty(required=True, default=0)
  
  def to_dict(self):
       d = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       d["id"] = self.key().id()
       return d
  
  @staticmethod
  def get_counter(sketchId = -1):
    return VersionCount.all().filter('sketchId', long(sketchId)).get()
  
  @staticmethod
  def get_and_increment_counter(sketchId = -1):
    versionCount = VersionCount.all().filter('sketchId', long(sketchId)).get()
    if versionCount:
      versionCount.lastVersion += 1
      versionCount.put()
    else:
      versionCount = VersionCount(sketchId=long(sketchId), lastVersion=1)
      versionCount.put()
    return versionCount.lastVersion
  
  
class AppVersionCount(db.Model):
  app_version = db.FloatProperty()
  sketch_count = db.IntegerProperty()
  original_count = db.IntegerProperty()
  

  def to_dict(self):
       d = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       d["id"] = self.key().id()
       return d
  
  @staticmethod  
  def increment_counter(app_version = -1, original = True):
    appVersionCount = AppVersionCount.all().filter('app_version', float(app_version)).get()
    if appVersionCount:
      appVersionCount.sketch_count += 1
      if original:
        appVersionCount.original_count += 1
      appVersionCount.put()
    else:
      if original:
        appVersionCount = AppVersionCount(app_version=float(app_version), sketch_count = 1, original_count = 1)
      else:
        appVersionCount = AppVersionCount(app_version=float(app_version), sketch_count = 1, original_count = 0)
      appVersionCount.put()
      
  
  @staticmethod  
  def decrement_counter(app_version = -1, original = True):
    appVersionCount = AppVersionCount.all().filter('app_version', float(app_version)).get()
    if appVersionCount:
      appVersionCount.sketch_count -= 1
      if original:
        appVersionCount.original_count -= 1
      appVersionCount.put()
  
  @staticmethod
  def retrieve_by_version():
    utc = UTC()
    appver_query = AppVersionCount.all()

    objects = appver_query.run()
    entities = []
    total_user_count = 0
    total_sketch_count = 0
    total_original_count = 0
    for object in objects:

      entity = {'app_version': object.app_version,
            'user_count': 0,
            'sketch_count': object.sketch_count,
            'original_count': object.original_count}
            
      appuser_query = AppUserCount.all().filter('app_version', float(object.app_version)).get()
      if appuser_query:
        entity['user_count'] = int(appuser_query.user_count)
      total_user_count += appuser_query.user_count
      total_sketch_count += object.sketch_count
      total_original_count += object.original_count
      entities.append(entity)    
    
    total = {'app_version': 'Total',
            'user_count': total_user_count,
            'sketch_count': total_sketch_count,
            'original_count': total_original_count}
    
            
    
    result = {'method':'retrieve_by_version',
              'status':'success',
              'entities': entities,
              'total': total}  
    return result
  
class Comment(db.Model):
  sketch_model_id = db.IntegerProperty(required=True)
  user_id = db.IntegerProperty(required=True)
  content = db.StringProperty(required=True)
  reply_to_id = db.IntegerProperty()
  created = db.DateTimeProperty(auto_now_add=True) #The time that the model was created
  
  def to_dict(self):
       d = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       d["id"] = self.key().id()
       return d  
       
  @staticmethod
  def add(data, user_id=-1):
    result = {}
    #try:
    #update ModelCount when adding
    jsonData = json.loads(data)
    
    #For sketch files saved through "Save As"
    if jsonData['sketchModelId'] != '' and user_id != -1:
      #Check Permissions
      permissions = Permissions.user_access_control(long(jsonData['sketchModelId']), long(user_id))
        
      if bool(permissions['p_comment']):
        #Placeholder for reply
      
        contentData = jsonData['content']
        contentData = contentData[:255]
          
        entity = Comment(sketch_model_id=long(jsonData['sketchModelId']),
                        user_id=long(user_id),
                        content=contentData,
                        reply_to_id=long(jsonData['replyToId']))
          
        verify = entity.put()
      else:
        result = {'status': "error",
                'message': "Sorry, but you are not authorized to comment."}
        
    else:
      result = {'status': "error",
                'message': "Error in posting comment. Please try again."}
    #except:
    #  result = {'status': "error",
    #            'message': "Error in posting comment. Please try again."}
    
    return result       
  

  @staticmethod
  def get_entities_by_id(model_id):
    utc = UTC()
    #update ModelCount when adding
    theQuery = Comment.all()
    #if model:
      #theQuery = theQuery.filter('model', model)

    objects = theQuery.run()

    entities = []
    for object in objects:
      if long(model_id) == object.sketch_model_id:
        data = {'sketchModelId': object.sketch_model_id,
                'user_id': object.user_id,
                'user_name': User.get_name(long(object.user_id)),
                'g_hash': User.get_image(long(object.user_id)),
                'content': object.content,
                'reply_to_id': object.reply_to_id}
          
        entity = {'id': object.key().id(),
              'created': object.created.replace(tzinfo=utc).strftime("%d %b %Y %H:%M:%S"), 
              'data': data}
              
        entities.append(entity)
       
    result = {'method':'get_entities_by_id',
              'en_type': 'Comment',
              'count': len(entities),
              'entities': entities}
    return result
    
  @staticmethod  
  def delete_by_sketch(sketch_model_id):
    theQuery = Comment.all()
    theQuery = theQuery.filter('sketch_model_id =', long(sketch_model_id))
    objects = theQuery.run()
    count = 0
    for object in objects:
      object.delete()
      count += 1
    result = {'method':'delete_by_sketch',
              'en_type': 'Comment',
              'sketchModelId': sketch_model_id,
              'count': count}
    return result
      
class Permissions(db.Model):
  sketch_model_id = db.IntegerProperty(required=True)
  view = db.BooleanProperty(required=True)
  edit = db.BooleanProperty(required=True)
  comment = db.BooleanProperty(required=True)
  
  def to_dict(self):
       d = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       d["id"] = self.key().id()
       return d
       
  @staticmethod
  def add(s_id, p_view, p_edit, p_comment):
    p_key = -1
    try:
      entity = Permissions(sketch_model_id = long(s_id),
                          view = bool(p_view),
                          edit = bool(p_edit),
                          comment = bool(p_comment))
      entity.put()
      p_key = entity.key().id()
    except:
      p_key = -1
    return p_key
    
  @staticmethod
  def check_permissions(sketch_id = 0):
    result = {'p_view':False,
              'p_edit':False,
              'p_comment':False}
              
    permissions = Permissions.all().filter('sketch_model_id', sketch_id).get()
    if permissions:
      result = {'p_view':permissions.view,
                'p_edit':permissions.edit,
                'p_comment':permissions.comment}
    return result
    
  @staticmethod
  def user_access_control(sketch_model_id = 0, user_id = 0):
    permissions = {'p_view':False,
                    'p_edit':False,
                    'p_comment':False}
    #Check if Admin - if true, grant FULL access
    if User.check_if_admin(user_id):
      permissions = {'p_view':True,
                    'p_edit':True,
                    'p_comment':True}
    #Check if Owner - if true, grant FULL access
    elif Sketch.check_if_owner(long(sketch_model_id), user_id):
      permissions = {'p_view':True,
                    'p_edit':True,
                    'p_comment':True}
    else:
      #Retrieve public permissions
      permissions = Permissions.check_permissions(long(sketch_model_id))
      
      #Retrieve group permissions
      group_permissions = Sketch_Groups.get_groups_for_sketch(long(sketch_model_id))
      user_groups = UserGroupMgmt.get_memberships(user_id)
      user_group_permissions = []
      for u_g in user_groups:
        group_id = u_g['group_id']
        for g_p in group_permissions:
          if long(group_id) == long(g_p['group_id']):
            user_group_permissions.append(g_p)
      #Apply group permissions
      for u_g_p in user_group_permissions:
        permissions['p_view'] = True
        if not permissions['p_edit']:
          permissions['p_edit'] = u_g_p['edit']
        if not permissions['p_comment']:
          permissions['p_comment'] = u_g_p['comment']
        if permissions['p_edit'] and permissions['p_comment']:
          break
    return permissions
    
  @staticmethod  
  def delete_by_sketch(sketch_model_id):
    theQuery = Permissions.all()
    theQuery = theQuery.filter('sketch_model_id =', long(sketch_model_id))
    theobject = theQuery.get()
    if theobject:
      theobject.delete()
    result = {'method':'delete_by_sketch',
              'en_type': 'Permissions',
              'sketchModelId': sketch_model_id}
    return result 
    
class Sketch_Groups(db.Model):
  sketch_model_id = db.IntegerProperty(required=True)
  group_id = db.IntegerProperty(required=True)
  edit = db.BooleanProperty(required=True)
  comment = db.BooleanProperty(required=True)
  #It is assumed that a sketch that belongs to a group
  #can be viewed by said group - thus, a "view" variable is
  #unnecessary.
  
  def to_dict(self):
       d = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       d["id"] = self.key().id()
       return d
       
  @staticmethod
  def add(s_id, g_id, g_edit, g_comment):
    g_key = -1
    try:
      entity = Sketch_Groups(sketch_model_id = long(s_id),
                          group_id = long(g_id),
                          edit = bool(g_edit),
                          comment = bool(g_comment))
      entity.put()
      g_key = entity.key().id()
    except:
      g_key = -1
    return g_key
  
  @staticmethod
  def get_groups_for_sketch(sketch_model_id=0):
    theQuery = Sketch_Groups.all()
    objects = theQuery.run()
    
    entities = []
    for object in objects:
      if object.sketch_model_id == sketch_model_id:
        data = {'id': object.key().id(),
                'sketch_model_id': object.sketch_model_id,
                'group_id': object.group_id,
                'group_name': Group.get_name(object.group_id),
                'edit': object.edit,
                'comment':object.comment}
        entities.append(data)
    return entities    
  
  @staticmethod
  def get_sketches_for_group(group_id=0):
    theQuery = Sketch_Groups.all()
    objects = theQuery.run()
    
    entities = []
    for object in objects:
      if object.group_id == group_id:
        data = {'id': object.key().id(),
                'sketch_model_id': object.sketch_model_id,
                'group_id': object.group_id,
                'group_name': Group.get_name(object.group_id),
                'edit': object.edit,
                'comment':object.comment}
        entities.append(data)
    return entities
    
  @staticmethod  
  def delete_by_sketch(sketch_model_id):
    theQuery = Sketch_Groups.all()
    theQuery = theQuery.filter('sketch_model_id =', long(sketch_model_id))
    objects = theQuery.run()
    count = 0
    for object in objects:
      object.delete()
      count += 1
    result = {'method':'delete_by_sketch',
              'en_type': 'Sketch_Groups',
              'sketchModelId': sketch_model_id,
              'count': count}
    return result
    
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
    theQuery = Group.all()
    jsonData = json.loads(data)
    result = {'status':'error',
              'message':'There was an error in creating your group.',
              'submessage':'Please try again later.'}    
    if jsonData['group_name'] != '':
      if jsonData['user_id'] != '':
        
        objects = theQuery.run()
        group_exists = False
        for object in objects:
          if jsonData['group_name'] == object.group_name:
            group_exists = True
            break
        if not group_exists:
          entity = Group(group_name=jsonData['group_name'])
        
          entity.put()
          
          usergroupmgmt = UserGroupMgmt(user_id=int(jsonData['user_id']),
                                        group_id=entity.key().id(),
                                        role="Founder")
          usergroupmgmt.put()
        
          result = {'status': 'success',
              'g_name': jsonData['group_name'],
              'u_id': jsonData['user_id'],
              'role': "Founder"}
        else:
          result = {'status': 'error',
                    'message': 'The name you chose is already in use!',
                    'submessage': 'Please choose a different group name!'}
              
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
          
        if object.role == "Pending":
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
        user_name = User.get_name(u_g.user_id)
        u_entity = {'user': user_name,
              'user_id': u_g.user_id,#placeholder
              'role': u_g.role}
        u_groups.append(u_entity)    
    
    result = {'method':'get_entity',
                  'id': model_id,
                  'group_name': theobject.group_name,
                  'u_groups': u_groups
                  }
    return result
    
  @staticmethod
  def check_users(model_id):
    theQuery = User.all()
    objects = theQuery.run()
    groupQuery = UserGroupMgmt.all().filter('group_id',int(model_id))
    groupObjects = groupQuery.run()
    entities = []
    for object in objects:
      include = True
      for groupObject in groupObjects:
        if object.key().id() == groupObject.user_id:
          include = False
      if include:
        data = {'id': object.key().id(),
                'u_name': object.display_name,
                'u_realname': object.real_name}
        entities.append(data)
    return entities
    
class UserGroupMgmt(db.Model):
  user_id = db.IntegerProperty(required=True)
  group_id = db.IntegerProperty(required=True)
  role = db.StringProperty(required=True)
  
  @staticmethod
  def add(data, other_user):
    #update ModelCount when adding
    jsonData = json.loads(data)
    result = {'status':'error',
              'message':'There was an error in sending the invite.',
              'submessage':'Please try again later.'}    
    if jsonData['user_id'] != 0:
      theQuery = UserGroupMgmt.all().filter('group_id', int(jsonData['group_id']))
      objects = theQuery.run()
      user_group_exists = False
      for object in objects:
        if int(jsonData['user_id']) == object.user_id:
          user_group_exists = True
          break
      if not user_group_exists:
        entity = UserGroupMgmt(user_id=int(jsonData['user_id']),
                              group_id=int(jsonData['group_id']),
                              role="Pending")
      
        entity.put()
        
        notify = Notification(user_id = int(jsonData['user_id']),
                              notification_type = "GROUPINVITE",
                              other_user = int(other_user),
                              relevant_id = entity.key().id())
                              
        notify.put()
        
        result = {'status': 'success',
            'user_id': jsonData['user_id'],
            'group_id': jsonData['group_id'],
            'role': "Pending"}
      else:
        result = {'status':'error',
                'message':'You cannot invite an existing or pending member!'}   
        
    else:
      result = {'status':'error',
              'message':'Please select a valid user to invite.'}   
    return result
    
  @staticmethod
  def get_memberships(userid):
    entities = []
    try:
      theQuery = UserGroupMgmt.all().filter('user_id', long(userid))
      objects = theQuery.run()
      for object in objects:
        if object.role != "Pending":
          data = {'user_id': object.user_id,
                  'group_id': object.group_id,
                  'role': object.role}
          entities.append(data)
    except ValueError:
      entities = []
    return entities
    
  @staticmethod
  def accept_reject(data, userid):
    jsonData = json.loads(data)
    result = {'status':'error',
              'message':'There was an error in processing the invitation.',
              'submessage':'Please try again later.'}
    status = str(jsonData['status'])
    u_g = UserGroupMgmt.get_by_id(int(jsonData['u_g']))
    founder = UserGroupMgmt.all().filter('group_id', u_g.group_id).filter('role', 'Founder').get()
    new_notify = Notification(user_id = founder.user_id,
                              notification_type = "",
                              other_user = int(userid),
                              relevant_id = u_g.group_id)
    if status == "accept":
      u_g.role = "Member"
      u_g.put()
      new_notify.notification_type = "GROUPACCEPT"
      
    else:
      u_g.delete()
      new_notify.notification_type = "GROUPREJECT"
    
    old_notify = Notification.get_by_id(int(jsonData['n_id']))
    old_notify.delete()
    new_notify.put()
    result = {'status': 'success',
              'message': 'You have successfully ' + jsonData['status'] + 'ed the group invitation.'}
    return result
      
class Notification(db.Model):
  user_id = db.IntegerProperty(required=True)
  notification_date = db.DateTimeProperty(auto_now_add=True)
  notification_type = db.StringProperty()
  other_user = db.IntegerProperty()
  other_info = db.StringProperty()
  relevant_id = db.IntegerProperty()

  def to_dict(self):
       d = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       d["id"] = self.key().id()
       return d
       
  @staticmethod
  def get_entities(user_id=-1, limit=0):
    #update ModelCount when adding
    u_id = int(user_id)
    theQuery = Notification.all()
    theQuery.order('-notification_date')

    objects = theQuery.run()
    utc = UTC()
    entities = []
    count = 0
    for object in objects:
      if object.user_id == int(user_id):
        n_date = object.notification_date.replace(tzinfo=utc).strftime("%d %b %Y %H:%M:%S")
        o_user = User.get_name(object.other_user)
        
        if object.notification_type == "GROUPINVITE":
          u_g = UserGroupMgmt.get_by_id(object.relevant_id)
          relevant =  Group.get_name(u_g.group_id)
          entity = {'n_date':n_date,
                  'id': object.key().id(),
                  'n_message': o_user + " has invited you to the group " + relevant + ".",
                  'n_type': object.notification_type,
                  'n_relevant': object.relevant_id}
          entities.append(entity)
        elif object.notification_type == "GROUPACCEPT":
          relevant =  Group.get_name(object.relevant_id)
          entity = {'n_date':n_date,
                  'id': object.key().id(),
                  'n_message': o_user + " has accepted your invitation to the group " + relevant + ".",
                  'n_type': object.notification_type,
                  'n_relevant': object.relevant_id}
          entities.append(entity)
        elif object.notification_type == "GROUPREJECT":
          relevant =  Group.get_name(object.relevant_id)
          entity = {'n_date':n_date,
                  'id': object.key().id(),
                  'n_message': o_user + " has rejected your invitation to the group " + relevant + ".",
                  'n_type': object.notification_type,
                  'n_relevant': object.relevant_id}
        elif object.notification_type == "ADMINDELETE":
          entity = {'n_date':n_date,
                  'id': object.key().id(),
                  'n_message': "An administrator has deleted your sketch '" + object.other_info + "'.",
                  'n_type': object.notification_type,
                  'n_relevant': 0}
          entities.append(entity)            
        #Placeholder for other notification types
        count += 1
        #Cutoff if limit was defined
        if limit != 0:
          if count == int(limit):
            break
          
    result = {'method':'get_entities',
              'en_type': 'Notification',
              'entities': entities,
              'retrieved': count}      
    return result
      
class Like(db.Model):
  sketch_model_id = db.IntegerProperty(required=True)
  user_id = db.IntegerProperty(required=True)
  created = db.DateTimeProperty(auto_now_add=True) #The time that the model was 
  
  def to_dict(self):
       d = dict([(p, unicode(getattr(self, p))) for p in self.properties()])
       d["id"] = self.key().id()
       return d
       
  @staticmethod     
  def like_unlike(data, userid):
    result = {}
    try:
      jsonData = json.loads(data)
      sketchModelId = long(jsonData['sketchModelId'])
      permissions = Permissions.user_access_control(sketchModelId, userid)
      
      if bool(permissions['p_view']):
        #Users can only (un)like sketches they can view
        theQuery = Like.all()
        theQuery.filter('sketch_model_id =', sketchModelId).filter('user_id =', userid)
        theobject = theQuery.get()
        data = {'sketchModelId': sketchModelId,
                'userid': userid,
                'action': ""}
        
        if theobject is None:
          #No existing Like by this user for this sketch - new Like
          newobject = Like(sketch_model_id = sketchModelId,
                           user_id = long(userid))
                           
          newobject.put()
          data['action'] = "Like"
        else:
          #Like by this user for this sketch exists - delete Like
          theobject.delete()
          data['action'] = "Dislike"
          
        result = {'status': "success",
                  'data': data}
      else:
        result = {'status': "error"}
    except:
      result = {'status': "error"}
    return result

  @staticmethod
  def check_if_user_likes(sketchModelId = -1, userid = -1):
    try:
      theQuery = Like.all()
      theQuery.filter('sketch_model_id =', long(sketchModelId)).filter('user_id =', long(userid))
      theobject = theQuery.get()
      if theobject:
        return True
      else:
        return False
    except:
      return False
      
  @staticmethod
  def get_entities_by_id(sketchModelId, userid = 0):
    utc = UTC()
    theQuery = Like.all()
    objects = theQuery.run()
    
    entities = []
    for object in objects:
      if object.sketch_model_id == long(sketchModelId):
        data = {'id': object.key().id(),
                'sketch_model_id': object.sketch_model_id,
                'user_id': object.user_id,
                'user_name': User.get_name(object.user_id),
                'created': object.created.replace(tzinfo=utc).strftime("%d %b %Y %H:%M:%S")}
        entities.append(data)
      
    result = {'method':'get_entities_by_id',
              'en_type': 'Like',
              'is_user_like': Like.check_if_user_likes(sketchModelId, userid),
              'count': len(entities),
              'count_other_users': (len(entities) - 1),
              'entities': entities}
    return result
        
  @staticmethod  
  def delete_by_sketch(sketch_model_id):
    theQuery = Like.all()
    theQuery = theQuery.filter('sketch_model_id =', long(sketch_model_id))
    objects = theQuery.run()
    count = 0
    for object in objects:
      object.delete()
      count += 1
    result = {'method':'delete_by_sketch',
              'en_type': 'Like',
              'sketchModelId': sketch_model_id,
              'count': count}
    return result
    
class ActionHandler(webapp2.RequestHandler):
    """Class which handles bootstrap procedure and seeds the necessary
    entities in the datastore.
    """
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

    def add_or_list_sketch(self): #/sketch
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

    def delete_sketch(self, model_id):  #/delete/sketch/<model_id>
        #Check for GET parameter == model to see if this is a get or an edit
        logging.info("**********************")
        logging.info(self.request.method)
        logging.info("**********************")

        auser = self.auth.get_user_by_session()
        userid = 0
        if auser:
          userid = auser['user_id']
        result = Sketch.remove(model_id, userid)
        
        return self.respond(result)
          
    def user_sketch(self, criteria): #/list/sketch/user/<criteria>
        #Check for GET parameter == model to see if this is a get or an edit
        logging.info("**********************")
        logging.info(self.request.method)
        logging.info("**********************")

        auser = self.auth.get_user_by_session()
        userid = 0
        if auser:
          userid = auser['user_id']
          
        result = Sketch.get_entities_by_id(criteria=criteria,userid=userid)
        return self.respond(result)    
          
    def group_sketch(self, criteria): #/list/sketch/group/<criteria>
        #Check for GET parameter == model to see if this is a get or an edit
        logging.info("**********************")
        logging.info(self.request.method)
        logging.info("**********************")

        auser = self.auth.get_user_by_session()
        userid = 0
        if auser:
          userid = auser['user_id']
          
        result = Sketch.get_entity_by_group(criteria,userid=userid)
        return self.respond(result)    
        
    def search_sketch(self, criteria): #/list/sketch/<criteria>
        #Check for GET parameter == model to see if this is a get or an edit
        logging.info("**********************")
        logging.info(self.request.method)
        logging.info("**********************")

        offset = 0
        new_offset = self.request.get("offset")
        if new_offset:
          offset = int(new_offset)

        auser = self.auth.get_user_by_session()
        userid = 0
        if auser:
          userid = auser['user_id']

        result = Sketch.get_entities(criteria=criteria,userid=userid)
        return self.respond(result)
      
    def list_sketch(self): #/list/sketch
        #Check for GET parameter == model to see if this is a get or an edit
        logging.info("**********************")
        logging.info(self.request.method)
        logging.info("**********************")

        offset = 0
        new_offset = self.request.get("offset")
        if new_offset:
          offset = int(new_offset)

        auser = self.auth.get_user_by_session()
        userid = 0
        if auser:
          userid = auser['user_id']
          
        result = Sketch.get_entities(userid=userid)
        return self.respond(result)
      
    def view_sketch(self, sketchId, version): #/get/sketch/view/<sketchId>/<version>
        #Check for GET parameter == model to see if this is a get or an edit
        logging.info("**********************")
        logging.info(self.request.method)
        logging.info("**********************")

        auser = self.auth.get_user_by_session()
        userid = 0
        if auser:
          userid = auser['user_id']
        
        result = Sketch.get_entity_by_versioning(sketchId, version, "View", userid=userid)
        return self.respond(result)     
        
    def edit_sketch(self, sketchId, version): #/get/sketch/edit/<sketchId>/<version>
        #Check for GET parameter == model to see if this is a get or an edit
        logging.info("**********************")
        logging.info(self.request.method)
        logging.info("**********************")

        auser = self.auth.get_user_by_session()
        userid = 0
        if auser:
          userid = auser['user_id']
        
        result = Sketch.get_entity_by_versioning(sketchId, version, "Edit", userid=userid)
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

    def check_user_group(self, model_id):
      result = {'status':'error',
                'message':''}
      entities = Group.check_users(model_id)
      result = {'status':'success',
                'method':'list_user',
                'en_type': 'User',
                'entities': entities}
      return self.respond(result)
        
    def get_versions(self):
        #Check for GET parameter == model to see if this is a get or an edit
        logging.info("**********************")
        logging.info(self.request.method)
        logging.info("**********************")

        offset = 0
        new_offset = self.request.get("offset")
        if new_offset:
          offset = int(new_offset)

        result = AppVersionCount.retrieve_by_version()
        return self.respond(result)
        
    def add_user_group(self):
        #Check for GET paramenter == model to see if this is an add or list. 
        #Call Sketch.add(model, data) or
        #Fetch all models and return a list. 
                
        #Todo - Check for method.
        auser = self.auth.get_user_by_session()
        result = {'status':'error',
              'message':'There was an error in sending the invite.',
              'submessage':'Please try again later.'}    
        if auser:
          userid = auser['user_id']
          result = UserGroupMgmt.add(self.request.body, userid)
        return self.respond(result)
        
    def accept_reject_group(self):
        auser = self.auth.get_user_by_session()
        result = {'status':'error',
              'message':'Not authenticated.'}
        if auser:
          userid = auser['user_id']
          result = UserGroupMgmt.accept_reject(self.request.body, userid)
        return self.respond(result)      
        
    def get_notification(self, limit):
        auser = self.auth.get_user_by_session()
        result = {}
        if auser:
          userid = auser['user_id']
          result = Notification.get_entities(userid, limit)
        return self.respond(result)
        

    def get_all_notification(self):
        auser = self.auth.get_user_by_session()
        result = {}
        if auser:
          userid = auser['user_id']
          result = Notification.get_entities(userid)
        return self.respond(result)        
          
    def add_comment(self):
        logging.info(self.request.method)
        auser = self.auth.get_user_by_session()
        result = {'status':'error',
              'message':'There was an error in adding the comment.',
              'submessage':'Please try again later.'}    
        if auser:
          userid = auser['user_id']
          if self.request.method=="POST":
            logging.info("in POST")
            logging.info(self.request.body)
            result = Comment.add(self.request.body, userid)
      
          else:
            data = self.request.get("obj")
            if data: 
              logging.info("Adding new data: "+data)
              result = Comment.add(data, userid)
        return self.respond(result)        
        
    def get_comment(self, model_id):
        #Check for GET parameter == model to see if this is a get or an edit
        logging.info("**********************")
        logging.info(self.request.method)
        logging.info("**********************")

        result = Comment.get_entities_by_id(model_id)
        return self.respond(result) 
          
    def toggle_like(self):
        logging.info(self.request.method)
        auser = self.auth.get_user_by_session()
        result = {'status':'error',
              'message':'There was an error in liking/unliking the sketch.',
              'submessage':'Please try again later.'}    
        if auser:
          userid = auser['user_id']
          if self.request.method=="POST":
            logging.info("in POST")
            logging.info(self.request.body)
            result = Like.like_unlike(self.request.body, userid)
      
          else:
            data = self.request.get("obj")
            if data: 
              logging.info("Adding new data: "+data)
              result = Like.like_unlike(data, userid)
        return self.respond(result)        
        
    def get_like(self, model_id):
        #Check for GET parameter == model to see if this is a get or an edit
        logging.info("**********************")
        logging.info(self.request.method)
        logging.info("**********************")
        
        auser = self.auth.get_user_by_session()
        if auser:
          userid = auser['user_id']
          result = Like.get_entities_by_id(model_id, userid)
        else:
          result = Like.get_entities_by_id(model_id, 0)
        return self.respond(result)    
   
        
webapp2_config = {}
webapp2_config['webapp2_extras.sessions'] = {
		'secret_key': 'n\xd99\xd4\x01Y\xea5/\xd0\x8e\x1ba\\:\x91\x10\x16\xbcTA\xe0\x87lf\xfb\x0e\xd2\xc4\x15\\\xaf\xb0\x91S\x12_\x86\t\xadZ\xae]\x96\xd0\x11\x80Ds\xd5\x86.\xbb\xd5\xcbb\xac\xc3T\xaf\x9a+\xc5',
	}

application = webapp2.WSGIApplication([
    webapp2.Route('/metadata', handler=ActionHandler, handler_method='metadata'),
    webapp2.Route('/delete/sketch/<model_id>', handler=ActionHandler, handler_method='delete_sketch'), 
    webapp2.Route('/sketch', handler=ActionHandler, handler_method='add_or_list_sketch'), # Add Sketch
    webapp2.Route('/list/sketch', handler=ActionHandler, handler_method='list_sketch'), # List Sketch
    webapp2.Route('/list/sketch/<criteria>', handler=ActionHandler, handler_method='search_sketch'), # List Sketch That Meets <criteria>
    webapp2.Route('/list/sketch/user/<criteria>', handler=ActionHandler, handler_method='user_sketch'), # List Sketch By User
    webapp2.Route('/list/sketch/group/<criteria>', handler=ActionHandler, handler_method='group_sketch'), # List Sketch By Group
    webapp2.Route('/get/sketch/view/<sketchId>/<version>', handler=ActionHandler, handler_method='view_sketch'), # Get Sketch (View)
    webapp2.Route('/get/sketch/edit/<sketchId>/<version>', handler=ActionHandler, handler_method='edit_sketch'), # Get Sketch (Edit)
    webapp2.Route('/group', handler=ActionHandler, handler_method='add_group'), # Add Group
    webapp2.Route('/get/group/<model_id>', handler=ActionHandler, handler_method='get_group'), # Get Group
    webapp2.Route('/list/group/<criteria>', handler=ActionHandler, handler_method='user_group'), # 
    webapp2.Route('/listuser/group/<model_id>', handler=ActionHandler, handler_method='check_user_group'), #
    webapp2.Route('/adduser/group', handler=ActionHandler, handler_method='add_user_group'), # Invite User To Group
    webapp2.Route('/acceptreject/group', handler=ActionHandler, handler_method='accept_reject_group'), # Accept/Reject Group Invite
    webapp2.Route('/get/notification/<limit>', handler=ActionHandler, handler_method='get_notification'), # Get Notifications (Menu)
    webapp2.Route('/get/notification', handler=ActionHandler, handler_method='get_all_notification'), # Get All Notifications
    
    webapp2.Route('/add/comment', handler=ActionHandler, handler_method='add_comment'), # Add Comment
    webapp2.Route('/get/comment/<model_id>', handler=ActionHandler, handler_method='get_comment'), # Get Comment For Sketch
    
    webapp2.Route('/toggle/like', handler=ActionHandler, handler_method='toggle_like'), # Add Comment
    webapp2.Route('/get/like/<model_id>', handler=ActionHandler, handler_method='get_like'), # Get Comment For Sketch
    
    webapp2.Route('/list/version', handler=ActionHandler, handler_method='get_versions') # Get Versions
    ],
    config=webapp2_config,
    debug=True)
