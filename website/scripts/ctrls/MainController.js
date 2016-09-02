"use strict";

import { parse_resp, clipboard } from "../utils";

import { BACKEND } from "../constants";

main_app.controller('MainController', ($scope, $http)=>{
    $scope.searching = false;
    $scope.search_finish = false;
    $scope.search_error = '';
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
    $scope.search_error = '';

    let url = `${BACKEND}/query`;
    $http.get(url, {
        params: {
            "content": keyword
        }
    }).then(parse_resp)
    .then((data)=>{
        if(data.failed){
            console.error(data.result);
            $scope.searching = false;
            $scope.search_finish = true;
            $scope.search_error = data.result;
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
}
