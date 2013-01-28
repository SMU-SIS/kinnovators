'use strict';

/* Controllers */

//angular.module("myApp", []);
function FirstController($scope) {
    $scope.name = "Anonymous User";
	
  	$scope.fileData = "?";  
   	$scope.fileName = "";
	$scope.files = [];
	$scope.filenames = [];
	
	$scope.filearray = [];
	   
	$scope.save = function() {
	   	
		$scope.fileData = $scope.fileData.replace(/(\r\n|\n|\r)/gm," ");
		$scope.filearray.push({id: $scope.filearray.length + 1, name: $scope.fileName, owner: $scope.name, data: $scope.fileData})
	   	$scope.fileName = "";
		$scope.fileData = "";
		document.getElementById('visibleTextData').value = "";

	}
   
	$scope.setData = function(f) {
		$scope.fileData = f;
	}
	
	$scope.setName = function(l) {
		$scope.name = l;
	}
}