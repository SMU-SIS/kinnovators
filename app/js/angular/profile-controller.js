'use strict';

/* Controller for profile.html */

//angular.module('app', ['ngResource']);
function ProfileController($scope,$resource,sharedProperties, sharedFunctions){
    
	$scope.User = {"id": 0, "u_name" :"Anonymous User",  "u_realname" :"Anonymous User", "u_login": false, "u_email": "", "g_hash": "", 'u_created': "", 'u_lastlogin': "", 'u_logincount': "", 'u_version': 1.0, 'u_isadmin': false, 'u_isactive': false};
  
  $scope.profile_user = {"id": 0, "u_name" :"Anonymous User",  "u_realname" :"Anonymous User", "g_hash": "", 'u_isadmin': false, 'u_isactive': false};
    
  $scope.backend_locations = [
    {url : sharedProperties.getBackendUrl(), urlName : 'remote backend' },       
    {url : 'localhost:8080', urlName : 'localhost' } ];

  $scope.showdetails = false;
  
  //Date (Time Zone) Format
  $scope.tzformat = function(utc_date) {
  
    var d = moment(utc_date, "DD MMM YYYY HH:mm:ss");
    return d.format("dddd, Do MMM YYYY, hh:mm:ss");
  };
  
  $scope.search = "";
  $scope.selected_search = "Name";
  
  $scope.derp = "derp";
  $scope.newgroup = {};
  $scope.newgroup.data = {"group_name":"", "user_id":""};
  $scope.test = "-";
  $scope.heading = "";
  $scope.message = "";
  $scope.submessage = "";
  $scope.notify = "You have no new notification(s).";
  
  
  //Search Query Filter
  $scope.query = function(item) {
      return !!((item.data.fileName.indexOf($scope.search || '') !== -1 || item.data.owner.indexOf($scope.search || '') !== -1));
  };

  $scope.predicate_users = '-data.fileName';
  

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
  
  /*$scope.edituser = function() {
    $scope.EditUserResource = $resource('http://:remote_url/user/edituser',
                              {'remote_url':$scope.remote_url}, 
                              {'update': { method: 'PUT', params: {} }});
    var edit_user = new $scope.EditUserResource($scope.User);
    $scope.waiting = "Loading";
    edit_user.$update(function(response) {
          $scope.User = response;
          
        });
  };*/
  
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
            $scope.User.u_created = $scope.tzformat($scope.User.u_created);
            
            if ($scope.User.u_lastlogin !== "") {
              $scope.User.u_lastlogin = $scope.tzformat($scope.User.u_lastlogin);
            }
            $scope.get_notification();
          } else {
            $scope.User = {"id": 0, "u_name" :"Anonymous User",  "u_realname" :"Anonymous User", "u_login": false, "u_email": "", "g_hash": "",  'u_created': "", 'u_lastlogin': "", 'u_logincount': "", 'u_version': 1.0, 'u_isadmin': false, 'u_isactive': false};
            if (navigator.userAgent.match(/MSIE\s(?!9.0)/))
            {
              var referLink = document.createElement("a");
              referLink.href = "index.html";
              document.body.appendChild(referLink);
              referLink.click();
            }
            else { window.location.replace("index.html");}
          }
    });
  };	
  
  $scope.setTest = function(test) {
    $scope.test = test;
  }
  
  $scope.get_profile = function() {
    if ($scope.test === "-") {
      $scope.profile_user = $scope.User;
      $scope.grouplist();
      $scope.list();
      $scope.belong = true;
    } else if (parseInt($scope.test, 10) === parseInt($scope.User.id, 10)) {
      $scope.profile_user = $scope.User;
      $scope.grouplist();
      $scope.list();
      $scope.belong = true;
    
    } else {
      $scope.belong = false;
      $scope.ProfileUserResource = $resource('http://:remote_url/user/profileuser/:id',
                          {'remote_url':$scope.remote_url, 'id':$scope.test},
                          {'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}
                             });  
      $scope.waiting = "Loading";       
      $scope.ProfileUserResource.get(function(response) {
            var result = response;
            if (result.status === "success") {
              $scope.profile_user = result;
              $scope.list();
              $scope.grouplist();
            } else {
              if (navigator.userAgent.match(/MSIE\s(?!9.0)/))
              {
                var referLink = document.createElement("a");
                referLink.href = "index.html";
                document.body.appendChild(referLink);
                referLink.click();
              }
              else { window.location.replace("index.html");}
            }            
            $scope.waiting = "Ready";
      });
    }
  }
  
  $scope.addgroup = function(){
    $scope.newgroup.data.user_id = $scope.User.id;
    $scope.GroupResource = $resource('http://:remote_url/group', 
                  {"remote_url":$scope.remote_url}, 
                  {'save': { method: 'POST',    params: {} }});
 
    $scope.waiting = "Saving";
    var newgroup = new $scope.GroupResource($scope.newgroup.data);
    newgroup.$save(function(response) { 
            var result = response;
            $scope.newgroup.data = {"group_name":"", "user_id":""};
            $scope.grouplist();
            if (result.status === 'success') {
              $scope.waiting = "Error";
              $scope.heading = "Success!";
              $scope.message = "You have successfully founded the group '" + result.g_name + "'!";
            } else {
              $scope.waiting = "Error";
              $scope.heading = "Oops...!"
              $scope.message = result.message;
              $scope.submessage = result.submessage;
            }
          }); 
  };
  
  //To add key/value pairs when creating new objects
  $scope.add_key_to_item = function(){
    $scope.item.data[$scope.newItemKey] = $scope.newItemValue;
    $scope.newItemKey = "";
    $scope.newItemValue = "";
  };    
  
  $scope.grouplist = function() {
    $scope.GroupListResource = $resource('http://:remote_url/list/group/:criteria',
    {"remote_url":$scope.remote_url,"criteria":$scope.profile_user.id}, 
             {'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
    $scope.waiting = "Saving";
    $scope.GroupListResource.get(function(response) { 
        $scope.groups = response;
     });  
  }

  $scope.acknowledge = function() {
    $scope.waiting = "Ready";
    $scope.heading = "";
    $scope.message = "";
    $scope.submessage = "";
  }
  
  $scope.get_notification = function() {
    $scope.NotificationResource = $resource('http://:remote_url/get/notification/:limit',
    {"remote_url":$scope.remote_url,"limit":3}, 
             {'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
    $scope.waiting = "Loading";
    $scope.NotificationResource.get(function(response) { 
        $scope.smallnotifications = response;
        if ($scope.smallnotifications.entities !== undefined) {
          if ($scope.smallnotifications.entities.length > 0) {
            $scope.notify = "You have pending notification(s).";
          }
        }
        $scope.waiting = "Ready";
     });  
  };
  
  $scope.list = function(){
    $scope.ListResource = $resource('http://:remote_url/list/sketch/user/:criteria',
    {"remote_url":$scope.remote_url,"criteria":$scope.profile_user.id}, 
             {'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
    $scope.waiting = "Loading";
    $scope.ListResource.get(function(response) { 
        $scope.items = response;
        $scope.waiting = "Ready";
    });  
  };
  
  $scope.delete_sketch = function(id) {
    var confirm_delete = confirm('Are you sure you want to delete this sketch?');
    if (confirm_delete == true){
      $scope.DeleteSketchResource = $resource('http://:remote_url/delete/sketch/:model_id',
      {"remote_url":$scope.remote_url,"model_id":id}, 
             {'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
      $scope.waiting = "Deleting";
      $scope.DeleteSketchResource.remove(function(response) { 
        var check = response.status
        $scope.list();
        if (check === 'error') {
            $scope.waiting = "Error";
            $scope.heading = "Oops!";
            $scope.message = "Error in deleting sketch.";
            $scope.submessage = "Please try again later.";         
        } else {
            $scope.waiting = "Error";
            $scope.heading = "Sketch Deleted";
            $scope.message = "You have successfully deleted the sketch.";     
        }
      });  
    }
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
            $scope.get_profile();
          }); 
  };
  
  $scope.simpleSearch = function() {
    sharedFunctions.simpleSearch($scope.search);
  }
  
  $scope.getuser();
}