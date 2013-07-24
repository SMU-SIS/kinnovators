'use strict';

/* Controller for sketch.html */

//angular.module('app', ['ngResource']);
function SketchController($scope,$resource,sharedProperties){

	$scope.User = {"id": 0, "u_name" :"Anonymous User",  "u_realname" :"Anonymous User", "u_login": false, "u_email": "", "g_hash": "", 'u_created': "", 'u_lastlogin': "", 'u_logincount': "", 'u_version': 1.0, 'u_isadmin': false, 'u_isactive': false};

  $scope.backend_locations = [
    {url : sharedProperties.getBackendUrl(), urlName : 'remote backend' },       
    {url : 'localhost:8080', urlName : 'localhost' } ];

  $scope.search = "";
  $scope.showdetails = false;
  
  //Date (Time Zone) Format
  $scope.tzformat = function(utc_date) {
  
    var d = moment(utc_date, "DD MMM YYYY HH:mm:ss");
    return d.format("dddd, Do MMM YYYY, hh:mm:ss");
  };
  //Sketch
  $scope.sketchId = "";  //Placeholder value for sketchId (identifies all sub-versions of the same sketch).
  $scope.version = "";  //Placeholder value for version (identifies version of sketch - starts at "1" unless existing sketch is loaded).
  $scope.fileData = "";  //Placeholder value for fileData (saved data).
  $scope.thumbnailData = ""; //Placeholder value for thumbnail data.
  $scope.fileName = "";  //Placeholder value for fileName (name file is saved under).
  $scope.tempFileName = ""; //Temporary placeholder for fileName during saveAs.
  $scope.changeDescription = ""; //Placeholder value for changeDescription (change description for file edits)


  
  $scope.loaded_id = -1;
  $scope.loaded_version = -1;
  $scope.heading = "";
  $scope.message = "";
  $scope.submessage = "";
  $scope.notify = "You have no new notification(s).";
  
  //Search Query Filter
  $scope.query = function(item) {
      return !!((item.data.fileName.indexOf($scope.search || '') !== -1 || item.data.owner.indexOf($scope.search || '') !== -1));
  };

  //Replace this url with your final URL from the SingPath API path. 
  //$scope.remote_url = "localhost:8080";
  $scope.remote_url = sharedProperties.getBackendUrl();
  $scope.janrain_ref = sharedProperties.getJanrainAccount();
  $scope.waiting = "Ready";
  
  //resource calls are defined here

  $scope.Model = $resource('http://:remote_url/:model_type/:id',
                          {},{'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}
                             }
                      );
                          
  $scope.getuser = function(){
    $scope.UserResource = $resource('http://:remote_url/user/getuser',
                        {'remote_url':$scope.remote_url},
                        {'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}
                           });  
    $scope.waiting = "Loading";          
    $scope.UserResource.get(function(response) {
          var result = response;
          if (result.u_login === "True" || result.u_login === true) {
            $scope.User = result;
            $scope.grouplist();
            $scope.get_notification();            
          } else {
            $scope.User = {"id": 0, "u_name" :"Anonymous User",  "u_realname" :"Anonymous User", "u_login": false, "u_email": "", "g_hash": "",  'u_created': "", 'u_lastlogin': "", 'u_logincount': "", 'u_version': 1.0, 'u_isadmin': false, 'u_isactive': false};
          }
          $scope.waiting = "Ready";
    });
  }
  
  $scope.item = {};
	$scope.item.data = {"sketchId":"", "version":"", "originalSketch":"","originalVersion":"", "owner":"", "owner_id":"", "fileName":"", "fileData":"", "changeDescription":"", "appver":"", "p_view": true, "p_edit": true, "p_comment": true, "group_permissions": []};    
  
	$scope.saveAs = function() { //Saving new file
	   	
		$scope.fileData = $scope.fileData.replace(/(\r\n|\n|\r)/gm," ");
		
		$scope.item.data.sketchId = "";			
		
		$scope.item.data.originalSketch = $scope.sketchId;
		$scope.item.data.originalVersion = $scope.version;
		
		$scope.item.data.owner = $scope.User.u_name;
    $scope.item.data.owner_id = $scope.User.id;
		$scope.item.data.fileName = $scope.tempFileName;
		$scope.item.data.fileData = $scope.fileData;
		$scope.item.data.thumbnailData = $scope.thumbnailData;
		$scope.item.data.changeDescription = $scope.changeDescription;
    $scope.item.data.appver = $scope.User.u_version;
    
    $scope.item.data.p_view = $scope.permissions.p_view;
    $scope.item.data.p_edit = $scope.permissions.p_edit;
    $scope.item.data.p_comment = $scope.permissions.p_comment;
    $scope.item.data.group_permissions = $scope.permissions.group_permissions;
		
	  $scope.setMeta($scope.item.data.sketchId, $scope.item.data.version, $scope.item.data.owner, $scope.item.data.owner_id, $scope.item.data.fileName);
		$scope.changeDescription = "" //Clears placeholder before next load.
		
		$scope.add_sketch();
	}
	
	$scope.save = function() { //Save new version of existing file
		$scope.fileData = $scope.fileData.replace(/(\r\n|\n|\r)/gm," ");
		
		$scope.item.data.sketchId = $scope.sketchId;
		
		$scope.item.data.originalSketch = $scope.sketchId;
		$scope.item.data.originalVersion = $scope.version;
		$scope.item.data.owner = $scope.User.u_name;
    $scope.item.data.owner_id = $scope.User.id;
		$scope.item.data.fileName = $scope.fileName;
		$scope.item.data.fileData = $scope.fileData;
		$scope.item.data.thumbnailData = $scope.thumbnailData;
		$scope.item.data.changeDescription = $scope.changeDescription;
    $scope.item.data.appver = $scope.User.u_version;
    
    $scope.item.data.p_view = $scope.permissions.p_view;
    $scope.item.data.p_edit = $scope.permissions.p_edit;
    $scope.item.data.p_comment = $scope.permissions.p_comment;
    $scope.item.data.group_permissions = $scope.permissions.group_permissions;
		
	  $scope.setMeta($scope.item.data.sketchId, $scope.item.data.version, $scope.item.data.owner, $scope.item.data.owner_id, $scope.item.data.fileName);
		$scope.changeDescription = "" //Clears placeholder before next load.
		
		$scope.add_sketch();		
	}
   
	$scope.setMeta = function(sketchId, version, owner, owner_id, fileName) {
		$scope.sketchId = sketchId;
		$scope.version = version;
		$scope.owner = owner;
    $scope.owner_id = owner_id
		$scope.fileName = fileName;
    $scope.grouplist();
    $scope.waiting = "Ready";
	}

  $scope.permissions = {"p_view": 1, "p_edit": false, "p_comment": false, "group_permissions": []};
  $scope.group_data = {"id":-1,"data":""};
  $scope.group_perm = {"group_id": -1, "group_name": "", "edit": false, "comment": false};
  
  $scope.changePermissions = function(value) {
    if (value = "changePermissions(1)") {
      $scope.permissions.p_edit = false;
      $scope.permissions.p_comment = false;
    }
  };
  $scope.addgroupperm = function() {
    $scope.group_perm.group_id = $scope.group_data.id;
    $scope.group_perm.group_name = $scope.group_data.data.group_name;
    $scope.permissions.group_permissions.push($scope.group_perm);
    $scope.group_data = {"id":-1,"data":""};
    $scope.group_perm = {"group_id": -1, "group_name": "", "edit": false, "comment": false};
  }
	
  $scope.removegroupperm = function(id) {
    var index = $scope.permissions.group_permissions.indexOf(id);
    $scope.permissions.group_permissions.splice(index, 1);
  }
  
  $scope.setPermissions = function(view, edit, comment, group_permissions) {
    $scope.permissions = {"p_view": view, "p_edit": edit, "p_comment": comment, "group_permissions": group_permissions};
  }
    
  $scope.setTest = function(loaded_id) {
    $scope.loaded_id = loaded_id;
  }

    
  $scope.setVersion = function(version) {
    $scope.version = version;
    $scope.loaded_version = version;
  }
  
  
	$scope.setData = function(fileData) {
		$scope.fileData = fileData;
    if (fileData.indexOf("thumbnail data") != -1) {
      var t_index = fileData.indexOf("thumbnail data");
      var t_start = fileData.indexOf("\"", t_index) + 1;
      var t_end = fileData.indexOf("\"", t_start);
      $scope.thumbnailData = fileData.substring(t_start,t_end);
      $scope.thumbnailData = $scope.thumbnailData.replace(/(\r\n|\n|\r)/gm," ");
      var format = new RegExp('&#xA;', 'g');
      $scope.thumbnailData = $scope.thumbnailData.replace(format,"");
    } else {
      $scope.thumbnailData = "";
    }
	}
	

  $scope.grouplist = function() {
    if ($scope.User.id != 0) {
      $scope.GroupListResource = $resource('http://:remote_url/list/group/:criteria',
      {"remote_url":$scope.remote_url,"criteria":$scope.User.id}, 
               {'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
      $scope.waiting = "Loading";   
      $scope.GroupListResource.get(function(response) { 
          $scope.groups = response;
       }); 
    }
  }
  
  $scope.add_sketch = function(){
    $scope.SaveResource = $resource('http://:remote_url/sketch', 
                  {"remote_url":$scope.remote_url}, 
                  {'save': { method: 'POST',    params: {} }});
 
    $scope.waiting = "Saving";
    var item = new $scope.SaveResource($scope.item.data);
    item.$save(function(response) { 
            var result = response;
            if (result.status === "success") {
              $scope.waiting = "Error";
              $scope.heading = "Success!";
              $scope.message = "You have successfully saved '" + $scope.fileName + "' (version " + result.data.version + ").";
              $scope.sketchId = result.data.sketchId;
              $scope.setTest(result.data.sketchId);
              $scope.setVersion(result.data.version);
            } else {
              $scope.waiting = "Error";
              $scope.heading = "Oops...!";
              $scope.message = result.message;
            }
          }); 
  };
  
  //To add key/value pairs when creating new objects
  $scope.add_key_to_item = function(){
    $scope.item.data[$scope.newItemKey] = $scope.newItemValue;
    $scope.newItemKey = "";
    $scope.newItemValue = "";
  };    
  
  $scope.get_sketch = function() {
    $scope.getSketch = $resource('http://:remote_url/get/sketch/edit/:id/:version', 
             {"remote_url":$scope.remote_url,"id":$scope.loaded_id,"version":$scope.version}, 
             {'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
    $scope.waiting = "Loading";      
    $scope.getSketch.get(function(response) {
        var check = response.success
        if (check !== "no") {
          var rsketch = response.data;
          $scope.setMeta(rsketch.sketchId, rsketch.version, rsketch.owner, rsketch.owner_id, rsketch.fileName);
          $scope.setPermissions(rsketch.p_public.p_view, rsketch.p_public.p_edit, rsketch.p_public.p_comment, rsketch.groups);
          $scope.fileData = rsketch.fileData;
          $scope.thumbnailData = rsketch.thumbnailData;
          loadKSketchFile($scope.fileData);
          if (check === "yes") {
            $scope.waiting = "Ready";
          } else if (check === "version"){
            $scope.waiting = "Error";
            $scope.heading = "Hmm...";
            $scope.message = "We couldn't find that version of the sketch you wanted.";
            $scope.submessage = "The latest existing version has been loaded instead.";            
          }
        }
        else {
          if (response.id === "Forbidden") {
            $scope.waiting = "Error";
            $scope.heading = "Access Denied";
            $scope.message = "You have not been granted permission to edit this sketch.";
          } else {
            $scope.waiting = "Error";
            $scope.heading = "Oops...!";
            $scope.message = "We're sorry, but the sketch you wanted does not exist.";
            $scope.submessage = "Perhaps the URL that you entered was broken?";
          }
        }
      });  
  }
  
  $scope.acknowledge = function() {
    if ($scope.heading === "Access Denied") {
      if (navigator.userAgent.match(/MSIE\s(?!9.0)/))
      {
        var referLink = document.createElement("a");
        referLink.href = "index.html";
        document.body.appendChild(referLink);
        referLink.click();
      }
      else { window.location.replace("index.html");} 
    } else {
      $scope.waiting = "Ready";
      $scope.heading = "";
      $scope.message = "";
      $scope.submessage = "";
    }
  }
  
  $scope.reload_sketch = function() {
    if ($scope.waiting === "Ready") {
      var reloadAlert = confirm("Do you wish to abandon your changes and revert to the saved sketch?");
      if (reloadAlert === true) {
        loadKSketchFile($scope.fileData);
      }
    }
  }
  $scope.get_notification = function() {
    $scope.NotificationResource = $resource('http://:remote_url/get/notification/:limit',
    {"remote_url":$scope.remote_url,"limit":3}, 
             {'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
    $scope.waiting = "Loading";   
    $scope.NotificationResource.get(function(response) { 
        $scope.smallnotifications = response;
        if ($scope.smallnotifications.entities.length > 0) {
          $scope.notify = "You have pending notification(s).";
        }
        $scope.waiting = "Ready";
     });  
  };
  
  
  $scope.accept = {};
  $scope.accept.data = {'n_id': -1, 'u_g' : -1, 'status': ''};
  
  $scope.notify_accept = function(n_id, u_g) {
    $scope.accept.data.n_id = n_id;
    $scope.accept.data.u_g = u_g;
    $scope.accept.data.status = 'accept';
    $scope.notify_group_action();
  };
  
  $scope.notify_reject = function(n_id, u_g) {
    $scope.accept.data.n_id = n_id;
    $scope.accept.data.u_g = u_g;
    $scope.accept.data.status = 'reject';
    $scope.notify_group_action();
  };
  
  $scope.notify_group_action = function() {
    $scope.NotifyGroupResource = $resource('http://:remote_url/acceptreject/group', 
                  {"remote_url":$scope.remote_url}, 
                  {'save': { method: 'POST',    params: {} }});
 
    $scope.waiting = "Loading";   
    var notify_group = new $scope.NotifyGroupResource($scope.accept.data);
    notify_group.$save(function(response) { 
            var result = response;
            $scope.accept.data = {'u_g' : -1, 'status': 'accept'}; 
            if (result.status === 'success') {
              $scope.waiting = "Error";
              $scope.heading = "Success!";
              $scope.message = result.message;
            } else {
              $scope.waiting = "Error";
              $scope.heading = "Oops...!"
              $scope.message = result.message;
              $scope.submessage = result.submessage;
            }                 
            $scope.get_notification();
          }); 
  };
  
  $scope.simpleSearch = function() {
    if ($scope.search.replace(/^\s+|\s+$/g,'') !== "") {
      //var searchAlert = confirm("Warning - Navigating away from this page will remove all your unsaved progress.\n\nDo you wish to continue?");
      //if (searchAlert === true) {
        var searchUrl = "search.html?query=" + $scope.search.replace(/^\s+|\s+$/g,'');
        window.location.href=searchUrl;
      } else {
        $scope.search = "";
      }
    //}
  }
  
  $scope.getStatus = function() {
    if ($scope.waiting == "Ready") {
      if ($scope.thumbnailData != "") {
        return true;
      } else {
        return false;
      }
    } else {
      return false;
    }
  }
  
  $scope.getuser();
}