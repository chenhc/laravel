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

       service.getUser = function() {
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

        service.update = function() {

        };

        return service;

    }
])

.factory('HotService', ['HttpService',
    function(HttpService) {

        var service = {};
        var api_url = 'api/hot';

        service.personal = function() {
            return HttpService.callApi('GET', api_url + '/personal', null);
        };

        service.food_material = function() {
            return HttpService.callApi('GET', api_url + '/food_material', null);
        };

        service.sports = function() {
            return HttpService.callApi('GET', api_url + '/sports', null);
        };

        service.tips = function() {
            return HttpService.callApi('GET', api_url + '/health_tips', null);
        };

        return service;
    }
]);
