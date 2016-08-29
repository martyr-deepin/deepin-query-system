"use strict";

import ngSanitize from "angular-sanitize";

import Cookies from "js-cookie";

window.main_app = angular.module("MainApp", ["ngRoute", "ngSanitize"]);
main_app.config(["$routeProvider", $routeProvider => {

    $routeProvider
        .when("/", {
            "templateUrl": "partials/main.html",
            "controller": "MainController",
            "title": "查询系统"
        })
        .otherwise({
            "templateUrl": "partials/main.html",
            "controller": "MainController",
            "title": "查询系统"
        });
}]);

/*
 * set page default title to route title attr
 */
main_app.run(($location, $rootScope)=>{
    $rootScope.$on('$routeChangeSuccess', (event, current, previous)=>{
        if(current.hasOwnProperty('$$route')){
            document.title = current.$$route.title;
        }
    });
});

console.log("init main.js");
