'use strict';

/* Controller for sketch.html */

//angular.module('app', ['ngResource']);
function ViewController($scope,$resource,sharedProperties){

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
  $scope.sketchId = "";  //Placeholder value for sketchId (identifies all sub-versions of the same sketch)
  $scope.version = "";  //Placeholder value for version (identifies version of sketch - starts at "1" unless existing sketch is loaded).
  $scope.fileData = "";  //Placeholder value for fileData (saved data)
  $scope.fileName = "";  //Placeholder value for fileName (name file is saved under)
  $scope.changeDescription = ""; //Placeholder value for changeDescription (change description for file edits)
  $scope.test = -1;
  $scope.version = -1;
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
          $scope.iiii = result.u_login;
          if (result.u_login === "True" || result.u_login === true) {
            $scope.User = result;
            $scope.get_notification();            
          } else {
            $scope.User = {"id": 0, "u_name" :"Anonymous User",  "u_realname" :"Anonymous User", "u_login": false, "u_email": "", "g_hash": "",  'u_created': "", 'u_lastlogin': "", 'u_logincount': "", 'u_version': 1.0, 'u_isadmin': false, 'u_isactive': false};
          }
          $scope.waiting = "Ready";
    });
  }
  
  $scope.item = {};
	$scope.item.data = {"sketchId":"", "version":"", "original":"", "owner":"", "owner_id":"", "fileName":"", "fileData":"", "changeDescription":"", "appver":"", "p_view": true, "p_edit": true, "p_comment": true}; 
          
    
  $scope.setTest = function(test) {
    $scope.test = test;
  }

    
  $scope.setVersion = function(version) {
    $scope.version = version;
  }
  
  
	$scope.setData = function(fileData) {
		$scope.fileData = fileData;
	}
	

/*
	General Add/List (pass "model" to m_type)
*/
  
  
  $scope.get_sketch = function() {
    $scope.getSketch = $resource('http://:remote_url/get/sketch/view/:id/:version', 
             {"remote_url":$scope.remote_url,"id":$scope.test,"version":$scope.version}, 
             {'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
    $scope.waiting = "Loading";      
    $scope.getSketch.get(function(response) {
        var check = response.success
        if (check !== "no") {
          $scope.item = response;
          $scope.fileData = $scope.item.data.fileData;
          $scope.sketchId = $scope.item.id;
          loadKSketchFile($scope.fileData);
          if (check === "yes") {
            $scope.getComments();
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
            $scope.message = "You have not been granted permission to view this sketch.";
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

  $scope.comment = {};
	$scope.comment.data = {"sketchId":$scope.sketchId, "content":"", "replyToId":-1};    
  
  $scope.addComment = function() {
    $scope.comment.data.sketchId = $scope.sketchId;
    if ($scope.comment.data.content.length > 0) {
      $scope.AddCommentResource = $resource('http://:remote_url/add/comment', 
                    {"remote_url":$scope.remote_url}, 
                    {'save': { method: 'POST',    params: {} }});
      $scope.waiting = "Loading";   
      var add_comment = new $scope.AddCommentResource($scope.comment.data);
      add_comment.$save(function(response) { 
              var result = response;
              $scope.comment.data = {"sketchId":$scope.sketchId, "content":"", "replyToId":-1};    
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
              $scope.getComments();
            });      
    }
  }
  
  $scope.getComments = function() {
     $scope.GetCommentResource = $resource('http://:remote_url/get/comment/:model_id', 
             {"remote_url":$scope.remote_url,"model_id":$scope.sketchId}, 
             {'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
    $scope.waiting = "Loading";   
    $scope.GetCommentResource.get(function(response) { 
        $scope.comments = response;           
        $scope.waiting = "Ready";
     });               
  } 
  
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
  
  $scope.getuser();
}