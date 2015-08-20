angular.module('iLifeApp', ['ngRoute','ngCookies'])

.config(function($routeProvider, $locationProvider) {
    $routeProvider

    // 用户注册
    .when('/user/register', {
        templateUrl: 'view/register.html',
        controller: 'RegisterController',
    })

    // 用户登录
    .when('/user/login', {
        templateUrl: 'view/login.html',
        controller: 'LoginController',
    })

    // 用户信息
    .when('/user', {
        templateUrl: 'view/user_info.html',
        controller: 'UserController',
    })

    // 食材详情
    .when('/food_material_detail/:hash', {
        templateUrl: 'view/food_material_detail.html',
        controller: 'FoodMaterialDetailController',
    })

    //主页面
    .when('/', {
        templateUrl: 'view/index.html',
        controller: 'IndexController',
    })

    .when('/user/healthCenter', {
        templateUrl: 'view/healthCenter.html',
        controller: 'HealthController',
    })

    .when('/food_material', {
        templateUrl: 'view/food_material.html',
        controller: 'FoodMaterialController',
    })

    .when('/food_material/:classification/:category', {
        templateUrl: 'view/food_material.html',
        controller: 'FoodMaterialController',
    })

    .when('/user/like/:item', {
        templateUrl: 'view/user_like.html',
        controller: 'UserLikeController',
    })

    .otherwise({redirectTo: '/'})
});
