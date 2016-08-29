"use strict";

import { parse_resp, clipboard } from "../utils";

let SERVER = 'http://10.0.2.76:16000';

main_app.controller('MainController', ($scope, $http)=>{
    $scope.searching = false;
    $scope.search_finish = false;
    $scope.copy_code_success = false;
    $scope.copy_code_failed = false;
    $scope.result_length = 0;

    // $scope.keyword = 'https://cr.deepin.io/#/c/15255';
    $scope.keyword = '';

    $scope.tab_click = (value)=>{
        $scope.current_tab_val = value;
        $scope.copy_code_success = false;
        $scope.copy_code_failed = false;
    }

    $scope.is_active = (value)=>{
        if($scope.current_tab_val === value){
            console.log('active');
            return true;
        }
        return false;
    }

    $scope.search_click = (keyword)=>{
        search_click(keyword, $scope, $http);
    }

    $scope.copy_code = (code)=>{
        if(clipboard(code)){
            $scope.copy_code_success = true;
        }
        else{
            $scope.copy_code_failed = true;
        }
    }
});


function search_click(keyword, $scope, $http){
    if(!keyword){
        return;
    }

    $scope.searching = true;
    $scope.search_finish = false;

    let url = `${SERVER}/query`;
    $http.get(url, {
        params: {
            "content": keyword
        }
    }).then(parse_resp)
    .then((data)=>{
        console.log(data);
        if(data.failed){
            console.err(data.result);
        }
        else{
            $scope.result = data.result;
            set_default_package_tab($scope);
            count_result_length($scope);
            $scope.searching = false;
            $scope.search_finish = true;
        }
    });
}

function set_default_package_tab($scope){
    if($scope.result.packages.length){
        $scope.current_tab_val = $scope.result.packages[0];
    }
}

function count_result_length($scope){
    $scope.result_length = 0;
    let len = 0;

    if($scope.result.bugzilla_url){
        len += 1;
    }

    if($scope.result.tower_url){
        len += 1;
    }

    if($scope.result.packages.length){
        len += 1;
    }

    $scope.result_length = len;
    console.log($scope.result_length);
    //$scope.$apply();
}
