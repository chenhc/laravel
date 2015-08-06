$(".dropdown-toggle").dropdown();

angular.module('iLifeApp', ['ngRoute'])

// 食材控制器
.controller('FoodMaterialController', function($scope, $routeParams, $http) {

    $scope.fetchMaterial = function(hash, callback) {
        $http.get('/api/food_material/' + hash).success(callback);
    }

    $scope.renderMaterial = function (data) {
        var suit_ctcms = ( data.suit_ctcms == null ? null : data.suit_ctcms.split(','));
        var avoid_ctcms = ( data.avoid_ctcms == null ? null : data.avoid_ctcms.split(','));
        var nutrient = ( data.nutrient == null ? null : data.nutrient.split("\n"));
        var efficacy = ( data.efficacy == null ? null : data.efficacy.split("\n"));
        var taboos = ( data.taboos == null ? null: data.taboos.split("\n"));
        var suit_mix = ( data.suit_mix == null ? null : data.suit_mix.split(","));
        var avoid_mix = ( data.avoid_mix == null ? null : data.avoid_mix.split(","));
        var tips = ( data.tips == null ? null : data.tips.split("\n"));

        data.suit_ctcms = suit_ctcms;
        data.avoid_ctcms = avoid_ctcms;
        data.nutrient = nutrient;
        data.efficacy = efficacy;
        data.taboos = taboos;
        data.suit_mix = suit_mix;
        data.avoid_mix = avoid_mix;
        data.tips = tips;
        //data solve end

        //data check
        for(item in data){
            if(data[item] == null || data[item] == ""){
                data[item] = '无';
                $('.hxy-'+item).hide();
            }
        }

        if(data.suit_ctcms == '无'){
            $('.hxy-suit_ctcms').hide();
        }else{
            $('.hxy-suit_ctcms').show();
        }

        if(data.avoid_ctcms == '无'){
            $('.hxy-avoid_ctcms').hide();
        }else{
            $('.hxy-avoid_ctcms').show();
        }

        $scope.material = data.data;
    }

    $scope.fetchMaterial($routeParams.hash, $scope.renderMaterial);
})

.controller('UserController', function($scope, $http) {

    $scope.renderBirthday = function() {
        $('.form_datetime').datetimepicker({
            weekStart: 1,
            todayBtn:  1,
            autoclose: 1,
            todayHighlight: 1,
            startView: 2,
            forceParse: 0,
            showMeridian: 1,
            format: "yyyy-mm-dd",
            minView: 2,
            endDate: $scope.user.birthday
        });
    }

    $scope.fetchSelf = function() {
        $http.get('/api/user')
        .success(function(data, status, headers, config) {
            if (data.status) {
                $scope.user = data.data;
                $scope.renderBirthday();
            }
        })
    }


    // 个性签名
    $scope.STATUS_LEN_LIMIT = 150;  // 长度限制150
    $scope.$watch('textarea', function(newStatus, oldStatus) {
        if(newStatus && (newStatus != oldStatus)) {
            if (newStatus.length >= $scope.limitation) {
                $scope.textarea = newStatus.substr(0, $scope.limitation);   // 截短
            }
        }
    });

    // 请求获取个人信息
    $scope.fetchSelf();
})

// 登录控制器
.controller('LoginController', function($scope, $http, $location) {

    $scope.submit = function(form) {
        console.log(form.account);
        if(form.account.$valid && form.password.$valid) {
            $http.post('/api/user/login', {
                'account':$scope.account,
                'password':$scope.password
            }).success(function(data, status, headers, config) {
                if (data.status) {
                     $location.path('/user');
                }
            }).error(function(data, status, headers, config) {
                console.log('post error');
            });
        }
    }
})

// 注册控制器
.controller('RegisterController', function($scope, $http, $location) {

    // 重置功能
    $scope.reset = function(form) {
        if(form) {
            form.$setPristine();
            form.$setUntouched();
        }

        $scope.name = '';
        $scope.email = '';
        $scope.password = '';
        $scope.ensured = '';
    }

    // 提交注册功能
    $scope.submit = function(form) {
        // 判断可以提交
        if (form.name.$valid &&
            form.email.$valid &&
            form.password.$valid &&
            form.ensured.$valid &&
            $scope.password == $scope.ensured
        ) {
            $http.post('/api/user', {
                'username': $scope.name,
                'email': $scope.email,
                'password': $scope.password
            }).success(function(data, status, headers, config) {
                if (data.status) {
                    $location.path('/user');
                }
            }).error(function(data, status, headers, config) {
                console.log(data);
                console.log('post error');
            });
        }
    }
})

.config(function($routeProvider, $locationProvider) {
    $routeProvider

    // 用户注册
    .when('/user/register', {
        templateUrl: 'view/register.html',
        controller: 'RegisterController'
    })

    // 用户登录
    .when('/user/login', {
        templateUrl: 'view/login.html',
        controller: 'LoginController'
    })

    // 用户信息
    .when('/user', {
        templateUrl: 'view/user_info.html',
        controller: 'UserController',
    })

    // 食材详情
    .when('/food_material_detail/:hash', {
        templateUrl: 'view/food_material_detail.html',
        controller: 'FoodMaterialController'
    })

    .otherwise({redirectTo: '/'})
})
