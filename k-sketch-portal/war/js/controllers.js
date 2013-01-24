'use strict';

/* Controllers */

//angular.module("myApp", []);
function FirstController($scope) {
    $scope.name = "Prof. Richard";
	
  	$scope.fileData = "?";  
   	$scope.fileName = "";
	$scope.files = [];
	$scope.filenames = [];
	
	$scope.filearray = [];
	   
	$scope.save = function() {
	   	
		$scope.fileData = $scope.fileData.replace(/(\r\n|\n|\r)/gm," ");
		$scope.filearray.push({id: $scope.filearray.length + 1, name: $scope.fileName, data: $scope.fileData})
	   	$scope.fileData = "";

	}
   
	$scope.setData = function(f) {
		$scope.fileData = f;
	}
}