'use strict';

/* Controller for Saving and Loading of Sketch */

angular.module('app', ['ngResource']);
function SketchController($scope,$resource){
    
	/*
		Sketch
	*/
	//User
	//$scope.name = "Anonymous User"; //Id name - retrieved from Google Login resp.displayName
  //  $scope.etag = ""; //Unique tag identifier - retrieved from Google Login resp.etag
	$scope.User = {"u_name" :"Anonymous User", "u_login": false, "u_email": ""}
    
  //Sketch
  $scope.sketchId = "";  //Placeholder value for sketchId (identifies all sub-versions of the same sketch)
  $scope.version = "";  //Placeholder value for version (identifies version of sketch - starts at "1" unless existing sketch is loaded).
  $scope.fileData = "";  //Placeholder value for fileData (saved data)
  $scope.fileName = "";  //Placeholder value for fileName (name file is saved under)
  $scope.changeDescription = ""; //Placeholder value for changeDescription (change description for file edits)

  //Current Id
  $scope.search = "";
  $scope.test = "";
  
  //Search Query Filter
  $scope.query = function(item) {
      return !!((item.data.fileName.indexOf($scope.search || '') !== -1 || item.data.owner.indexOf($scope.search || '') !== -1));
  };

  $scope.backend_locations = [
    {url : 'k-sketch-test.appspot.com', urlName : 'remote backend' },       
    {url : 'localhost:8080', urlName : 'localhost' } ];

  $scope.showdetails = false;

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
            $scope.User = {"u_name" :"Anonymous User", "u_login": false, "u_email": ""}
          }
          $scope.waiting = "Ready";
    });
  }
  
  $scope.item = {};
	$scope.item.data = {"sketchId":"", "version":"", "original":"", "owner":"", "fileName":"", "fileData":"", "changeDescription":""};    
           	
	$scope.saveAs = function() { //Saving new file
	   	
		$scope.fileData = $scope.fileData.replace(/(\r\n|\n|\r)/gm," ");
		document.getElementById('visibleTextData').value = "";
		
		$scope.item.data = {"sketchId":"", "version":"", "original":"", "owner":"", "fileName":"", "fileData":"", "changeDescription":""};
		$scope.item.data.sketchId = "";			
		
		$scope.item.data.original = $scope.sketchId + ":" + $scope.version;
		
		$scope.item.data.owner = $scope.User.u_name;
		$scope.item.data.fileName = $scope.fileName;
		$scope.item.data.fileData = $scope.fileData;
		$scope.item.data.changeDescription = $scope.changeDescription;
		
	  $scope.setMeta($scope.item.data.sketchId, $scope.item.data.version, $scope.item.data.owner, $scope.item.data.fileName);
		$scope.changeDescription = "" //Clears placeholder before next load.
		
		$scope.add("sketch");
	}
	
	$scope.save = function() { //Save new version of existing file
		$scope.fileData = $scope.fileData.replace(/(\r\n|\n|\r)/gm," ");
		document.getElementById('visibleTextData').value = "";
		
		$scope.item.data = {"sketchId":"", "version":"", "original":"", "owner":"", "fileName":"", "fileData":"", "changeDescription":""};
		$scope.item.data.sketchId = $scope.sketchId;
		$scope.item.data.original = $scope.sketchId + ":" + $scope.version; 
		$scope.item.data.owner = $scope.owner;
		$scope.item.data.fileName = $scope.fileName;
		$scope.item.data.fileData = $scope.fileData;
		$scope.item.data.changeDescription = $scope.changeDescription;
		
	  $scope.setMeta($scope.item.data.sketchId, $scope.item.data.version, $scope.item.data.owner, $scope.item.data.fileName);
		$scope.changeDescription = "" //Clears placeholder before next load.
		
		$scope.add("sketch");		
	}
   
	$scope.setMeta = function(sketchId, version, owner, fileName) {
		$scope.sketchId = sketchId;
		$scope.version = version;
		$scope.owner = owner;
		$scope.fileName = fileName;
	}
	
    
  $scope.setTest = function(test) {
    $scope.test = test;
  }
  
	$scope.setData = function(fileData) {
		$scope.fileData = fileData;
	}
	

/*
	General Add/List (pass "model" to m_type)
*/
  
  $scope.add = function(m_type){
    $scope.SaveResource = $resource('http://:remote_url/:model', 
                  {"remote_url":$scope.remote_url,"model":m_type}, 
                  {'save': { method: 'POST',    params: {} }});
 
    $scope.waiting = "Loading";
    var item = new $scope.SaveResource($scope.item.data);
    item.$save(function(response) { 
            var result = response;
            $scope.sketchId = result.data.sketchId;
            $scope.version = result.data.version;
            $scope.list(m_type);
            $scope.item.data = {"sketchId":"", "version":"", "original":"", "owner":"", "fileName":"", "fileData":"", "changeDescription":""};               
            $scope.waiting = "Ready";
          }); 
  };
  
  //To add key/value pairs when creating new objects
  $scope.add_key_to_item = function(){
    $scope.item.data[$scope.newItemKey] = $scope.newItemValue;
    $scope.newItemKey = "";
    $scope.newItemValue = "";
  };    
  
  $scope.list = function(){
    $scope.SearchResource = $resource('http://:remote_url/list/sketch/:criteria',
    {"remote_url":$scope.remote_url,"criteria":$scope.User.u_name}, 
             {'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
    $scope.waiting = "Updating";   
    $scope.SearchResource.get(function(response) { 
        $scope.items = response;
        $scope.waiting = "Ready";
     });  
  };
  
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
  
  $scope.get_sketch = function(id) {
    $scope.getSketch = $resource('http://:remote_url/get/sketch/:id', 
             {"remote_url":$scope.remote_url,"id":$scope.test}, 
             {'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
    $scope.waiting = "Updating";   
    $scope.getSketch.get(function(response) { 
        var rsketch = response.data;
        $scope.setMeta(rsketch.sketchId, rsketch.version, rsketch.owner, rsketch.fileName);
        $scope.fileData = rsketch.fileData;
        loadKSketchFile($scope.fileData);
        $scope.waiting = "Ready";
      });  
  }
  
  $scope.reload_sketch = function() {
    loadKSketchFile($scope.fileData);
  }
  
  $scope.getuser();
  $scope.list();
}