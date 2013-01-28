'use strict';

/* Controllers */


function FirstController($scope) {
   $scope.name = "Prof. Richard";
}

function AnnimationController($scope, $resource) {
   $scope.name = $resource('/animation').get();
}
