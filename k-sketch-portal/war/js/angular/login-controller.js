'use strict';

/* Controller for Handing Logins. Currently not working. */

angular.module('app', ['ngResource']);
function LoginController($scope,$resource){
    $scope.name = "Anonymous User"; //Id name - retrieved from Google Login resp.displayName
    $scope.etag = ""; //Unique tag identifier - retrieved from Google Login resp.etag
	
	   


  $scope.backend_locations = [
    {url : 'saitohikari89.appspot.com', urlName : 'remote backend' },       
    {url : 'localhost:8080', urlName : 'localhost' } ];

  $scope.showdetails = false;
  $scope.apikey = "DESU";
  
  //Replace this url with your final URL from the SingPath API path. 
  //$scope.remote_url = "localhost:8080";
  $scope.remote_url = "saitohikari89.appspot.com";
  $scope.model = "login";
  $scope.waiting = "Ready";
  
  $scope.item = {};
  $scope.item.data = {"currentid":""};
  
  //resource calls are defined here

  $scope.Model = $resource('http://:remote_url/:apikey/:model_type/:id',
                          {},{'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}
                             }
                      );

/*  //Code to generate id to identify all versions of a particular sketch.
  $scope.generateSketchId = function(m_type) {
	  var data = {'remote_url':$scope.remote_url,
              'model_type':m_type,
              'apikey':$scope.apikey,
              'id': 61003
            }
      $scope.Model.get(data, 
          function(response){   
              $scope.item = response;
              $scope.item_data = $scope.item.data;
          }); 
	  alert($scope.item.data.currentId);
  }
  
  //Code to update currentId counter.
  $scope.updateSketchId = function(m_type){
    $scope.UpdateResource = $resource('http://:remote_url/:apikey/:model', 
                  {"remote_url":$scope.remote_url,"apikey":$scope.apikey,"model":m_type, "id":61003}, 
                  {'update': { method: 'PUT',    params: {} }});
    
 
    $scope.item.currentId = parseInt($scope.item.currentId, 10) + 1;
    var item = new $scope.UpdateResource($scope.item.currentId);
    item.$update(function(response) { 
            $scope.item = response;
          });
  };
    */
  
  //Generic model resource calls. Pass model-type.
  
  $scope.add = function(m_type){
    $scope.SaveResource = $resource('http://:remote_url/:apikey/:model', 
                  {"remote_url":$scope.remote_url,"apikey":$scope.apikey,"model":m_type}, 
                  {'save': { method: 'POST',    params: {} }});
 
    $scope.waiting = "Loading";
    var item = new $scope.SaveResource($scope.item.data);
    $scope.item = item.$save(function(response) { 
            $scope.item = response;
            $scope.list(m_type);
            $scope.waiting = "Ready";
          }); 
  };
  
  //To add key/value pairs when creating new objects
  $scope.add_key_to_item = function(){
    $scope.item.data[$scope.newItemKey] = $scope.newItemValue;
    $scope.newItemKey = "";
    $scope.newItemValue = "";
  };    
  
  $scope.list = function(m_type){
    var data = {
  		  'remote_url':$scope.remote_url,
			  'model_type':m_type,
            'apikey':$scope.apikey
           }
    $scope.waiting = "Updating";       
    $scope.Model.get(data,
          function(response) { 
            $scope.items = response;
            $scope.waiting = "Ready";
          });  
  };

  $scope.list("login");         
}