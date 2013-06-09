'use strict';

/* Controller for groups.html */

//angular.module('app', ['ngResource']);
function GroupsController($scope,$resource,sharedProperties){
    
	$scope.User = {"id": 0, "u_name" :"Anonymous User",  "u_realname" :"Anonymous User", "u_login": false, "u_email": "", "g_hash": "",  'u_created': "", 'u_lastlogin': "", 'u_logincount': "", 'u_version': 1.0, 'u_isadmin': false, 'u_isactive': false};
    
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
  $scope.predicate_users = '-data.fileName';  
  $scope.derp = "derp";
  $scope.test = "-";
  $scope.belong = false;
  $scope.founder = false;
  
  $scope.group_name = "-";
  $scope.u_groups = [];
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
    $scope.waiting = "Updating";       
    $scope.UserResource.get(function(response) {
          var result = response;
          $scope.iiii = result.u_login;
          if (result.u_login === "True" || result.u_login === true) {
            $scope.User = result;
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
          $scope.waiting = "Ready";
    });
  }	
    
  $scope.setTest = function(test) {
    $scope.test = test;
  }
  
  $scope.get_group = function() {
    $scope.getGroup = $resource('http://:remote_url/get/group/:id', 
             {"remote_url":$scope.remote_url,"id":$scope.test}, 
             {'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
    $scope.waiting = "Updating";   
    $scope.getGroup.get(function(response) { 
        var thisgroup = response;
        $scope.setGroup(thisgroup.group_name, thisgroup.u_groups);
        for (var i = 0; i < thisgroup.u_groups.length; i++) {
          var u_g = thisgroup.u_groups[i]
          if (u_g.user_id === $scope.User.id) {
            $scope.belong = true;
            if (u_g.role === "Founder") {
              $scope.founder = true;
            }
          }
        }
        $scope.waiting = "Ready";
      });  
  }
  
	$scope.setGroup = function(group_name, u_groups) {
    $scope.group_name = group_name;
    $scope.u_groups = u_groups;
	}
  

  $scope.groupuserlist = function() {
    $scope.GroupUserListResource = $resource('http://:remote_url/listuser/group/:id',
    {"remote_url":$scope.remote_url,"id":$scope.test}, 
             {'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
    $scope.waiting = "Updating";
    $scope.GroupUserListResource.get(function(response) { 
        var result = response;
        if (result.status === "success") {
          $scope.usersfound = result;
        }
        $scope.waiting = "Ready";
     });  
  }  

  $scope.usertoadd = {};
  $scope.usertoadd.data = {"user_id": 0, "group_id":$scope.test};
  
  $scope.addmember = function() {
    $scope.usertoadd.data.group_id = $scope.test;
    $scope.AddMemberResource = $resource('http://:remote_url/adduser/group', 
                  {"remote_url":$scope.remote_url}, 
                  {'save': { method: 'POST',    params: {} }});
 
    $scope.waiting = "Saving";
    var addgroup = new $scope.AddMemberResource($scope.usertoadd.data);
    addgroup.$save(function(response) { 
            var result = response;
            $scope.usertoadd.data = {"user_id": 0, "group_id":$scope.test};
            $scope.get_group();
            if (result.status === 'success') {
              $scope.waiting = "Error";
              $scope.heading = "Success!";
              $scope.message = "You have sent out the invite.";
            } else {
              $scope.waiting = "Error";
              $scope.heading = "Oops...!"
              $scope.message = result.message;
              $scope.submessage = result.submessage;
            }
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
    $scope.waiting = "Updating";
    $scope.NotificationResource.get(function(response) { 
        $scope.smallnotifications = response;
        if ($scope.smallnotifications.entities.length > 0) {
          $scope.notify = "You have " + $scope.smallnotifications.entities.length + " new notification(s).";
        }
        $scope.waiting = "Ready";
     });  
  };  
  

  
  $scope.accept = {};
  $scope.accept.data = {'u_g' : 0, 'n_id': 0, 'status': 'accept'};
  $scope.notify_accept_group = function(n_a) {
    $scope.accept.data = n_a;
    $scope.AcceptResource = $resource('http://:remote_url/acceptreject/group', 
                  {"remote_url":$scope.remote_url}, 
                  {'save': { method: 'POST',    params: {} }});
 
    $scope.waiting = "Updating";
    var acceptgroup = new $scope.AcceptResource($scope.accept.data);
    acceptgroup.$save(function(response) { 
            var result = response;
            $scope.accept.data = {'u_g' : 0, 'n_id': 0, 'status': 'accept'};            
            $scope.get_notification();
          }); 
  };
  
  $scope.simpleSearch = function() {
    if ($scope.search.replace(/^\s+|\s+$/g,'') !== "") {
      var searchUrl = "search.html?query=" + $scope.search.replace(/^\s+|\s+$/g,'');
      window.location.href=searchUrl;
    }
  }
  
  $scope.getuser();
}