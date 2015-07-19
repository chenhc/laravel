<?php

/**
 * FileName:   AddressApiController.php
 * Author:     Chen Yanfei
 * @contact:   fasionchan@gmail.com
 * @version:   $Id$
 *
 * Description:
 *
 * Changelog:
 *
 **/

namespace App\Http\Controllers;

use App\Http\Requests;
use App\Http\Controllers\Controller;

use Illuminate\Http\Request;


class AddressApiController extends Controller
{
    public function country(Request $request, $country_code)
    {

    }

    public function district(Request $request, $country_code, $province_code,
            $city_code, $district_code)
    {

    }
}
