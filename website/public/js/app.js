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

        $scope.material = data;
    }

    $scope.fetchMaterial($routeParams.hash, $scope.renderMaterial);
})

.config(function($routeProvider, $locationProvider) {
    $routeProvider
    .when('/food_material_detail/:hash', {
        templateUrl: 'view/food_material_detail.html',
        controller: 'FoodMaterialController'
    })
})
