'use strict';

/* Controller for search.html */

//angular.module('app', ['ngResource']);
function SearchController($scope,$resource){
    
	/*
		Sketch
	*/
	//User
	$scope.User = {"id": 0, "u_name" :"Anonymous User", "u_login": false, "u_email": ""}
  $scope.backend_locations = [
    {url : 'k-sketch-test.appspot.com', urlName : 'remote backend' },       
    {url : 'localhost:8080', urlName : 'localhost' } ];

  $scope.showdetails = false;
  
  $scope.search = "";
  $scope.predicate_users = '-data.fileName';
  
  //Replace this url with your final URL from the SingPath API path. 
  //$scope.remote_url = "localhost:8080";
  $scope.remote_url = "k-sketch-test.appspot.com";
  $scope.waiting = "Ready";
  
  //resource calls are defined here

  $scope.Model = $resource('http://:remote_url/:model_type/:id',
                          {},{'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}
                             }
                      );
                          
  $scope.getuser = function(){
    $scope.UserResource = $resource('http://:remote_url/getuser',
                        {'remote_url':$scope.remote_url},
                        {'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}
                           });  
    $scope.waiting = "Updating";       
    $scope.UserResource.get(function(response) {
          var result = response;
          $scope.iiii = result.u_login;
          if (result.u_login === "True" || result.u_login === true) {
            $scope.User = result;            
          } else {
            $scope.User = {"id": 0, "u_name" :"Anonymous User", "u_login": false, "u_email": ""}
          }
          $scope.waiting = "Ready";
    });
  }


  
  $scope.searchlist = function(){
    $scope.SearchResource = $resource('http://:remote_url/list/sketch/:criteria',
    {"remote_url":$scope.remote_url,"criteria":$scope.search}, 
             {'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
    $scope.waiting = "Updating";   
    $scope.SearchResource.get(function(response) { 
        $scope.searchitems = response;
        $scope.waiting = "Ready";
    });
  };
  
  $scope.getuser();
}