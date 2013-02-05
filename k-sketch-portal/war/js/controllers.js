'use strict';

/* Controllers */

angular.module('app', ['ngResource']);
function FirstController($scope,$resource){
    $scope.name = "Anonymous User"; //Id name - retrieved from Google Login resp.displayName
    $scope.etag = ""; //Unique tag identifier - retrieved from Google Login resp.etag
	
  	$scope.fileData = "?";  
   	$scope.fileName = "";
	$scope.files = [];
	$scope.filenames = [];
	
	$scope.filearray = [];
	   
	$scope.save = function() {
	   	
		$scope.fileData = $scope.fileData.replace(/(\r\n|\n|\r)/gm," ");
		$scope.filearray.push({id: $scope.filearray.length + 1, name: $scope.fileName, owner: $scope.name, data: $scope.fileData});
		document.getElementById('visibleTextData').value = "";
		
		$scope.item.data.id = "0";
		$scope.item.data.owner = $scope.name;
		$scope.item.data.fileName = $scope.fileName;
		$scope.item.data.fileData = $scope.fileData;
		
	   	$scope.fileName = "";
		$scope.fileData = "";
		
		$scope.add("sketch");
	}
   
	$scope.setData = function(f) {
		$scope.fileData = f;
	}
	
	$scope.setName = function(l) {
		$scope.name = l.displayName;
		$scope.etag = l.etag;
	}




  $scope.backend_locations = [
    {url : 'saitohikari89.appspot.com', urlName : 'remote backend' },       
    {url : 'localhost:8080', urlName : 'localhost' } ];

  $scope.showdetails = false;
  $scope.apikey = "DESU";
  
  //Replace this url with your final URL from the SingPath API path. 
  //$scope.remote_url = "localhost:8080";
  $scope.remote_url = "saitohikari89.appspot.com";
  $scope.model = "sketch";
  $scope.waiting = "Ready";
  
  $scope.item = {};
  $scope.item.data = {"id":"", "owner":"", "fileName":"", "fileData":"Hi Chris"};
  
  //resource calls are defined here

  $scope.Model = $resource('http://:remote_url/:apikey/:model_type/:id',
                          {},{'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}
                             }
                      );

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

  $scope.list("sketch");         
}