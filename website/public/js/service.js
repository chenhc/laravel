angular.module('iLifeApp')

.factory('HttpService', ['$http', '$q',
    function($http, $q) {

        var service = {};

        service.callApi = function(_method, _url, _params, _data) {
            var deferred = $q.defer();
            $http({
                    method: _method,
                    url: _url,
                    params: _params,
                    data: _data
                })
                .success(function(data, status, headers, config) {
                    deferred.resolve(data);
                })
                .error(function(data, status, headers, config) {
                    deferred.reject('There was an error: ' + status);
                });
            return deferred.promise;
        };

        return service;
    }
])

.factory('FoodMaterialService', ['HttpService',
    function(HttpService) {

        var service = {};
        var api_url = '/api/food_material';

        service.fetch = function(hash) {
            return HttpService.callApi('GET', api_url + '/' + hash, null, null);
        };

        service.index = function(params) {
            return HttpService.callApi('GET', api_url, params, null);
        };

        return service;
    }
])

.factory('FoodRecipeService', ['HttpService',

    function(HttpService) {

        var service = {};
        var api_url = '/api/food_recipe';

        service.fetch = function(hash) {
            return HttpService.callApi('GET', api_url + '/' + hash, null, null);
        };

        service.index = function(params) {
            return HttpService.callApi('GET', api_url, params, null);
        };

        return service;
    }
])

.factory('CategoryService', ['HttpService',
    function(HttpService) {

       var service = {};
       var api_url = '/api/category';

       service.fetch = function(name) {
           return HttpService.callApi('GET', api_url + '/' + name, null, null);
       };

       return service;
    }
])

.factory('UserService', ['HttpService',
    function(HttpService) {

        var service = {};
        var api_url = '/api/user';

        // 获取用户信息，不加参数默认取当前用户信息
        service.getUser = function() {
            if (arguments[0])
                return HttpService.callApi('GET', api_url + '/' + arguments[0],
                                            null, null);
            else
                return HttpService.callApi('GET', api_url, null, null);
        };

        service.valid = function(data) {
            return HttpService.callApi('POST', api_url + '/validity',
                                    null, data);
        };

        service.register = function(name, email, password) {
            var data = {
                'username': name,
                'email': email,
                'password': password
            };
            return  HttpService.callApi('POST', api_url, null, data);
        };

        service.destory = function(hash) {
            return HttpService.callApi('DELETE', api_url + '/' + hash,
                                        null, null);
        };

        service.login = function(account, password) {
            var data = {
                'account': account,
                'password': password
            };
            return HttpService.callApi('POST', api_url + '/login', null, data);
        };

        service.logout = function() {
            return HttpService.callApi('GET', api_url + '/logout', null, null);
        };

        service.update = function(hash, data) {
            return HttpService.callApi('PUT', api_url + '/' + hash,
                                        null, data);
        };

        service.setLikedMaterial = function(hash) {
            data = {
                'material_hash': hash
            };
            return HttpService.callApi('POST', api_url + '/like/food_material',
                                        null, data);
        };

        service.setDislikedMaterial = function(hash) {
            data = {
                'material_hash': hash
            };
            return HttpService.callApi('Delete',
                                        api_url + '/like/food_material',
                                        null, data);
        };

        service.fetchLikedMaterials = function() {
            return HttpService.callApi('GET', api_url + '/like/food_material',
                                        null, null);
        };

        service.setLikedRecipe = function(hash) {
            data = {
                'recipe_hash': hash
            };
            return HttpService.callApi('POST', api_url + '/like/food_recipe',
                                        null, data);
        };

        service.setDislikedRecipe = function(hash) {
            data = {
                'recipe_hash': hash
            };
            return HttpService.callApi('POST', api_url + '/like/food_recipe',
                                        null, data);
        };

        service.fetchLikedRecipes = function() {
            return HttpService.callApi('GET', api_url + '/like/food_recipe',
                                        null, null);
        };

        return service;

    }
])

.factory('HotService', ['HttpService',
    function(HttpService) {

        var service = {};
        var api_url = 'api/hot';

        service.personal = function() {
            return HttpService.callApi('GET', api_url + '/personal', null, null);
        };

        service.food_material = function() {
            return HttpService.callApi('GET', api_url + '/food_material', null, null);
        };

        service.sports = function() {
            return HttpService.callApi('GET', api_url + '/sports', null, null);
        };

        service.tips = function() {
            return HttpService.callApi('GET', api_url + '/health_tips', null, null);
        };

        return service;
    }
]);
