'use strict';

/* Controller for generating current Sketch Id. Currently not working. */

angular.module('app', ['ngResource']);
function CurrentIdController($scope,$resource){
	
  $scope.currentId = "0";

/*  $scope.showdetails = false;
  $scope.apikey = "DESU";
  
  //Replace this url with your final URL from the SingPath API path. 
  //$scope.remote_url = "localhost:8080";
  $scope.remote_url = "saitohikari89.appspot.com";
  $scope.model = "currentId";
  $scope.waiting = "Ready";
  
  $scope.currentId = {};
  $scope.currentId.data = {"currentId":""};
  
  //resource calls are defined here

  $scope.Model = $resource('http://:remote_url/:apikey/:model_type/:id',
                          {},{'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}
                             }
                      );

//Code to generate id to identify all versions of a particular sketch.
  $scope.generateSketchId = function(m_type) {
	  var data = {'remote_url':$scope.remote_url,
              'model_type':m_type,
              'apikey':$scope.apikey,
              'id': 61003
            }
      $scope.Model.get(data, 
          function(response){   
              $scope.currentId = response;
              $scope.currentId_data = $scope.currentId.data;
          }); 
	  alert($scope.currentId.data.currentId);
  }
  
  //Code to update currentId counter.
  $scope.updateSketchId = function(m_type, id){
    $scope.UpdateResource = $resource('http://:remote_url/:apikey/:model', 
                  {"remote_url":$scope.remote_url,"apikey":$scope.apikey,"model":m_type, "id":61003}, 
                  {'update': { method: 'PUT',    params: {} }});
    
 
    $scope.currentId.data.currentId = parseInt($scope.item.currentId, 10) + 1;
    var item = new $scope.UpdateResource($scope.item.currentId);
    item.$update(function(response) { 
            $scope.item = response;
          });
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

  $scope.list("currentId");      */   
}