<?php

/**
 * FileName:   route.php
 * Author:     Chen Yanfei
 * @contact:   fasionchan@gmail.com
 * @version:   $Id$
 *
 * Description:
 *
 * Changelog:
 *
 **/

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
