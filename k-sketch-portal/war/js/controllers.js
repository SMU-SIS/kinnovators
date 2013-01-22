'use strict';

/* Controllers */

//angular.module("myApp", []);
function FirstController($scope) {
    $scope.name = "Prof. Richard";
	
  	$scope.fileData = "?";  
   	$scope.fileName = "";
	$scope.files = [];
	$scope.filenames = [];
	   
	$scope.save = function() {
	   	
		
		$scope.filenames.push($scope.fileName);
		$scope.files.push($scope.fileData);
	   		
	}
   
	$scope.setData = function(f) {
		$scope.fileData = f;
	}

}
