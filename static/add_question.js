'use strict';   

var app = angular.module('add_question', ['ngRoute']);

app.config(function($routeProvider) {
  $routeProvider

  .when('/add_question', {
    templateUrl : '/static/partials/add_question.html',
    controller  : 'AddQuestion'
  })


  .otherwise({redirectTo: 'add_question.html'});
});

app.controller('AddQuestion', function($scope) {
  $scope.message = 'Hello from HomeController';
});
