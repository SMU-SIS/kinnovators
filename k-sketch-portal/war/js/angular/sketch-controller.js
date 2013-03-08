'use strict';

/* Controller for Saving and Loading of Sketch */

angular.module('app', ['ngResource']);
function SketchController($scope,$resource){
    
	/*
		Sketch
	*/
	//User
	$scope.name = "Anonymous User"; //Id name - retrieved from Google Login resp.displayName
    $scope.etag = ""; //Unique tag identifier - retrieved from Google Login resp.etag
	
    
    //Sketch
    $scope.sketchId = "";  //Placeholder value for sketchId (identifies all sub-versions of the same sketch)
    $scope.version = "";  //Placeholder value for version (identifies version of sketch - starts at "1" unless existing sketch is loaded).
  	$scope.fileData = "";  //Placeholder value for fileData (saved data)
   	$scope.fileName = "";  //Placeholder value for fileName (name file is saved under)
   	$scope.changeDescription = ""; //Placeholder value for changeDescription (change description for file edits)
	
   	//Current Id
   	$scope.search = "";
   	
   	//Search Query Filter
   	$scope.query = function(item) {
   			return !!((item.data.fileName.indexOf($scope.search || '') !== -1 || item.data.owner.indexOf($scope.search || '') !== -1));
   	};

    $scope.backend_locations = [
      {url : 'saitohikari89.appspot.com', urlName : 'remote backend' },       
      {url : 'localhost:8080', urlName : 'localhost' } ];

    $scope.showdetails = false;

    //Replace this url with your final URL from the SingPath API path. 
    //$scope.remote_url = "localhost:8080";
    $scope.remote_url = "saitohikari89.appspot.com";
    $scope.waiting = "Ready";
    
    //resource calls are defined here

    $scope.Model = $resource('http://:remote_url/:model_type/:id',
                            {},{'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}
                               }
                        );
 	
    $scope.item = {};
	$scope.item.data = {"sketchId":"", "version":"", "original":"", "owner":"", "fileName":"", "fileData":"", "changeDescription":""};    
           	
	$scope.saveAs = function() { //Saving new file
	   	
		$scope.fileData = $scope.fileData.replace(/(\r\n|\n|\r)/gm," ");
		document.getElementById('visibleTextData').value = "";
		
		$scope.item.data = {"sketchId":"", "version":"", "original":"", "owner":"", "fileName":"", "fileData":"", "changeDescription":""};
		$scope.item.data.sketchId = "";			
		
		$scope.item.data.original = $scope.sketchId + ":" + $scope.version;
		
		$scope.item.data.owner = $scope.name;
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
	
	$scope.setData = function(fileData) {
		$scope.fileData = fileData;
	}
	
	$scope.setName = function(l) {
		$scope.name = l.displayName;
		$scope.etag = l.result;
	}
		
	$scope.logout = function() {
		$scope.name = "Anonymous User";
		$scope.etag = ""
		
		var authorizeButton = document.getElementById('authorize-button');
		authorizeButton.style.visibility = '';		
		
		var hm = document.getElementById('hm');
		var sc = document.getElementById('sc');
		var cs = document.getElementById('cs');
		var vs = document.getElementById('vs');	
		
		var hm2 = document.getElementById('Home');
		var sc2 = document.getElementById('Sketchbook');
		var cs2 = document.getElementById('CreateSketch');
		var vs2 = document.getElementById('ViewSketch');
		
		sc.className = sc.className.replace
					( /(?:^|\s)active(?!\S)/g , '' );
		sc2.className = sc2.className.replace
		( /(?:^|\s)active(?!\S)/g , '' );	
		cs.className = cs.className.replace
			      ( /(?:^|\s)active(?!\S)/g , '' );
		cs2.className = cs2.className.replace
	      ( /(?:^|\s)active(?!\S)/g , '' );	      		
		vs.className = vs.className.replace
			      ( /(?:^|\s)active(?!\S)/g , '' )
		vs2.className = vs2.className.replace
		      ( /(?:^|\s)active(?!\S)/g , '' )
		if (hm.className.search("active") == -1) {		      
			hm.className += "active";				  
		}
		if (hm2.className.search(" active") == -1) {
			hm2.className += " active";
		}
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
            $scope.sketchId = result.sketchId;
            $scope.version = result.version;
            $scope.list(m_type);
            alert(result.version);
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
  
  $scope.list = function(m_type){
    var data = {
  		  'remote_url':$scope.remote_url,
			  'model_type':m_type,
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