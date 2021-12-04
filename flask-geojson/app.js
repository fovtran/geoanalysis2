var app = angular.module('myApp', ['ngAnimate']);


app.controller('AnimateController', ['$scope', '$timeout', function($scope, $timeout){
    $scope.title = 'First Step at Angular Animations!';

    $scope.addToList = function(){
      $scope.list.push({title: $scope.listElement});
    };

    $timeout(function(){
      $scope.list = [
        {title: 'hello World'},
        {title: 'hello World'},
        {title: 'hello World'},
        {title: 'hello World'}
      ];
    }, 1000);

  }]);
