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
}

api_route('api/food_material', 'FoodMaterialApiController');
api_route('api/food_recipe', 'FoodRecipeApiController');


Route::group(['prefix' => 'api/user', 'middleware' => 'auth'], function() {
    Route::get('/', 'UserApiController@index');
    Route::put('/', 'UserApiController@update');
    Route::delete('/', 'UserApiController@destroy');

});

Route::post('/api/user', 'UserApiController@store');
Route::get('/api/user/{hash}', 'UserApiController@fetch');

Route::get('/', 'DietController@index');

Route::controllers([
	'auth' => 'Auth\AuthController',
	'password' => 'Auth\PasswordController',
]);
