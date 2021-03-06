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

function api_route($path, $controller) {
    Route::post($path, $controller . '@store');
    Route::delete($path . '/{hash}', $controller . '@destroy');
    Route::get($path . "/{hash}", $controller . '@fetch');
    Route::put($path . '/{hash}', $controller . '@update');
    Route::get($path, $controller . '@index');
}

function weixin_route($path, $controller) {
    Route::get('/wx/' . $path . '/{hash}', 'Weixin\\' . $controller . '@display');
}

api_route('api/food_material', 'FoodMaterialApiController');
api_route('api/food_recipe', 'FoodRecipeApiController');
api_route('api/user', 'UserApiController');

Route::post('/api/login', 'UserApiController@login');
Route::get('/api/logout', 'UserApiController@logout');

weixin_route('food_material', 'FoodMaterialWeixinController');

Route::get('/', 'DietController@index');
Route::get('/diet', 'DietController@index');


Route::controllers([
	'auth' => 'Auth\AuthController',
	'password' => 'Auth\PasswordController',
]);
