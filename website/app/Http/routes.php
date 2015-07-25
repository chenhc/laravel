<?php

/*
|--------------------------------------------------------------------------
| Application Routes
|--------------------------------------------------------------------------
|
| Here is where you can register all of the routes for an application.
| It's a breeze. Simply tell Laravel the URIs it should respond to
| and give it the controller to call when that URI is requested.
|
*/

Route::get('/api/address/country/{code}', 'AddressApiController@country');
Route::get('/api/address/country/{country_code}/province/{province_code}/city/{city_code}/district/{district_code}', 'AddressApiController@district');

api_route('api/food_material', 'FoodMaterialApiController');
api_route('api/food_recipe', 'FoodRecipeApiController');
api_route('api/user', 'UserApiController');

Route::post('/api/user/login', 'UserApiController@login');
Route::get('/api/user/logout', 'UserApiController@logout');

Route::group(['prefix' => '/api/user/like/food_material'], function(){
    Route::post('/', 'UserApiController@setLikedMaterial');
    Route::delete('/', 'UserApiController@setDislikedMaterial');
    Route::get('/', 'UserApiController@fetchLikedMaterials');
    
});

Route::group(['prefix' => '/api/user/like/food_recipe'], function(){
    Route::post('/', 'UserApiController@setLikedRecipe');
    Route::delete('/', 'UserApiController@setDislikedRecipe');
    Route::get('/', 'UserApiController@fetchLikedRecipes');
});

weixin_route('food_material', 'FoodMaterialWeixinController');


Route::controllers([
	'auth' => 'Auth\AuthController',
	'password' => 'Auth\PasswordController',
]);
