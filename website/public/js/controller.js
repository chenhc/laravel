angular.module('iLifeApp')

//父类控制器
.controller('ParentController', ['$scope',
    function($scope) {
        $scope.$on('intermediary', function(e, newStatus) {
            $scope.$broadcast('loginStatus', newStatus);
        });
    }
])
// 食材控制器
.controller('FoodMaterialDetailController', ['$scope', '$routeParams',
        'FoodMaterialService',
    function($scope, $routeParams, FoodMaterialService) {

        $scope.material = {};

        renderMaterial = function(response) {
            var data = response.data;
            for (attr in data) {
                var value = data[attr];
                if (['suit_ctcms', 'avoid_ctcms', 'suit_mix', 'avoid_mix']
                    .indexOf(attr) >= 0)
                    value = value ? value.split(',') : "无";
                else if (['nutrient', 'efficacy', 'taboos'].indexOf(attr) >= 0)
                    value = value ? value.split('\n'): "无";
                $scope.material[attr] = value;
            }
        };

        FoodMaterialService.fetch($routeParams.hash)
            .then(function(response) {
                renderMaterial(response);
            });
    }
])

// 食材列表控制器
.controller('FoodMaterialController', ['$scope',
        '$routeParams', 'FoodMaterialService', 'CategoryService',
    function($scope, $routeParams, FoodMaterialService, CategoryService) {

        $scope.category = $routeParams.category;
        $scope.classification = $routeParams.classification;

        $scope.renderCAC = function(response) {
            $scope.classificationAll = {};

            for(item in response.data) {
                $scope.classificationAll[item] = item;
            }

            $scope.categoryAll = response.data;
        }
        // 对获取的数据进行分析重构
        $scope.getData = function(data) {

            $scope.itemsUp = {};
            $scope.itemsDown = {};

            for(i = 0; i < 4; i++) {
                if(data[i]) {
                    $scope.itemsUp[i] = data[i];
                }
            }

            for(i = 4; i < 8; i++) {
                if(data[i]) {
                    $scope.itemsDown[i] = data[i];
                }
            }
        };

        // 获取classification和category
        CategoryService.fetch('food_material')
            .then(function(response) {
                $scope.renderCAC(response);
            });

        // 获取初始化首页数据
        $scope.refresh = function(classification, category, page, pagesize) {
            params = {
                'classification': classification ? classification : '',
                'category': category ? category : '',
                'page': page ? page : 1,
                'pagesize': pagesize ? pagesize : 8,
            }
            FoodMaterialService.index(params)
                            .then(function(response) {
                $scope.getData(response.data);
                $scope.totalPage = response.totalPage;
            });
        };

        $scope.initial = function() {
            $scope.refresh($scope.classification, $scope.category, 1, 8);
            $scope.page = 3;
            $scope.activePage = 1;
        };

        // 换classification函数
        $scope.changeClassification = function(element) {
            $scope.classification = element;
            $scope.category = null;
            $scope.initial();
        }

        // 换category函数
        $scope.changeCategory = function(element) {

            $scope.category = element;
            $scope.initial();
        }

        // 转页函数
        $scope.turnPage = function(element) {

            if($scope.activePage == element || element > $scope.totalPage) {
                return;
            }

            $scope.activePage = element;

            if(element == 1 || element == 2 || element == 3) {
                $scope.page = 3;
            }
            else {
                if(element == $scope.totalPage
                    || element == $scope.totalPage - 1
                    || element == $scope.totalPage - 2) {
                    $scope.page = $scope.totalPage - 2;
                }
                else {
                    $scope.page = $scope.activePage;
                }
            }

            $scope.refresh($scope.classification, $scope.category, element, 8);

         }

        $scope.initial();

    }
])


//账户中心控制器
.controller('UserController', ['$scope', 'UserService',
    function($scope, UserService) {

        $scope.fetchSelf = function() {
            UserService.getUser()
                .then(function(response) {
                    $scope.isLogin = true;
                    $scope.user = response.data;
                });
        }

        // 个性签名
        $scope.STATUS_LEN_LIMIT = 150;  // 长度限制150
        $scope.$watch('textarea', function(newStatus, oldStatus) {
            if(newStatus && (newStatus != oldStatus)) {
                if (newStatus.length >= $scope.STATUS_LEN_LIMIT) {
                    $scope.textarea = newStatus.substr(0, $scope.STATUS_LEN_LIMIT);   // 截短
                }
            }
        });

        // 请求获取个人信息
        $scope.fetchSelf();
    }
])

// 登录控制器
.controller('LoginController', ['$scope', '$location', '$window',
        'UserService',
    function($scope, $location, $window, UserService) {

        // 登录提交表单函数
        $scope.submit = function(form) {
            if(form.account.$valid && form.password.$valid) {

                UserService.login($scope.account, $scope.password)
                    .then(function(response) {
                        if(response.status) {
                            $location.path('/');
                        }
                        else {
                            $window.alert('账号或密码错误');
                        }
                    });

            }
        };
    }
])

// 注册控制器
.controller('RegisterController', ['$scope', '$location',
        'UserService',
    function($scope, $location, UserService) {

        $scope.valid = function(response, change) {
            if(response.status) {
                change = false;
            }
            else {
                change = true;
            }
        };

        // name valid?
        $scope.nameIsSame = false;

        $scope.isSameName = function() {
            var params = {
                'username': $scope.name
            };
            UserService.valid(params)
                .then(function(response) {
                    if(response.status) {
                        $scope.nameIsSame = false;
                    }
                    else {
                        $scope.nameIsSame = true;
                    }
                });
        };

        // email valid?
        $scope.emailIsSame = false;

        $scope.isSameEmail = function() {
            var params = {
                'email': $scope.email
            }
            UserService.valid(params)
                .then(function(response) {
                    if(response.status) {
                        $scope.emailIsSame = false;
                    }
                    else {
                        $scope.emailIsSame = true;
                    }
                });
        };

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
            $scope.emailIsSame = false;
            $scope.nameIsSame = false;
        };

        // 提交注册功能
        $scope.submit = function(form) {
            // 判断可以提交
            if (form.name.$valid &&
                form.email.$valid &&
                form.password.$valid &&
                form.ensured.$valid &&
                $scope.password == $scope.ensured &&
                $scope.nameIsSame == false &&
                $scope.emailIsSame ==false
            ) {
                UserService.register($scope.name, $scope.email, $scope.password)
                    .then(function(response) {
                        $location.path('/user');
                    });
            }
        };
    }
])

//主页控制器
.controller('IndexController', function($scope, $http, $cookies, $location) {

    //监听是否登出
    $scope.$on('loginStatus', function(e,newStatus) {
        $scope.isLogin = newStatus;
        if(newStatus) {
            //get personal
            $http.get('/api/hot/personal')
                .success(function(data,status, headers, config) {
                    $scope.personal = data.data;
                });
        }
    });

    //get ppt
    $http.get('/api/hot/food_material')
        .success(function(data, status, headers, config) {
            $scope.ppt = data.data;
            $scope.show = $scope.ppt[0].image_hash;//使ppt刚开始显示第一张图片
        });

    //get food
    $http.get('/api/hot/food_material')
        .success(function(data, status, headers, config) {
            $scope.food = data.data;
        });

    //get sport
    $http.get('/api/hot/sports')
        .success(function(data, status, headers, config) {
            $scope.sport = data.data;
        });

    //get tips
    $http.get('/api/hot/health_tips')
        .success(function(data, status, headers, config) {
            $scope.tip = data.data;
        });

    angular.element(window).bind('load', function() {

        var fixed_first = '.img_' + $scope.ppt[0].image_hash;
        var first = angular.element(document.querySelector(fixed_first));

        //使得图片居中
        first.css('marginTop',(-1*first[0].clientHeight/2) + 'px');
    });

    //幻灯片的按钮跳转
    $scope.slider = function(element) {

        $scope.show = element;
        var fixed = '.img_'+element;
        var it = angular.element(document.querySelector(fixed));

        //使得图片居中
        it.css('marginTop',(-1*it[0].clientHeight/2) + 'px');
    }

})

//健康中心控制器
.controller('HealthController', function($scope, $http, $cookies, $location) {
   /* $scope.questions = [
        {question:'您舌头的颜色',choice1:,choice2:,choice3:,choice4:},
        {question:'您舌体的形态',choice1:,choice2:,choice3:,choice4:},
        {question:'您舌苔的颜色',choice1:,choice2:,choice3:,choice4:},
        {question:'您舌苔的厚度',choice1:,choice2:,choice3:,choice4:},
        {question:'您排泄物的形状',choice1:,choice2:,choice3:,choice4:},
        {question:'您排泄物的粘稠度',choice1:,choice2:,choice3:,choice4:},
        {question:'您口腔的气味',choice1:,choice2:,choice3:,choice4:},
        {question:'您的生活习惯',choice1:,choice2:,choice3:,choice4:},
        {question:'您的饮食嗜好 ',choice1:,choice2:,choice3:,choice4:},
        {question:'您一分钟脉搏跳动的次数 ',choice1:,choice2:,choice3:,choice4:}
    ];*/
    $scope.click = function() {
        console.log($scope.color);
    }
})

// 导航栏控制器
.controller('NavigationBarController',['$scope', '$location',
        'UserService',
    function($scope, $location, UserService) {

        $scope.loginOrNot = function(response) {
            if(response.status) {

                if($location.url() == '/user/login'
                    || $location.url == '/user/register') {
                    $location.path('/');
                }

                if($location.url() == '/user/healthCenter') {
                    $scope.healthCenterActive = true;
                }
                else {
                    $scope.healthCenterActive = false;
                }

                $scope.isLogin = true;
                $scope.user = response.data;

                $scope.$emit('intermediary', $scope.isLogin);

                $scope.logout = function() {
                    UserService.logout()
                        .then(function(response) {
                            $scope.isLogin = false;
                            $scope.$emit('intermediary', $scope.isLogin);
                            $location.path('/');
                        });
                };

            }
            else {

                if($location.url() == '/user') {
                    $location.path('/user/login');
                }

                $scope.isLogin = false;

                $scope.$emit('intermediary', $scope.isLogin);

            }
        }
        // 对页面url的判断跳转，以及用户状态的设定
        UserService.getUser()
            .then(function(response) {
                $scope.loginOrNot(response);
            });
    }
]);
