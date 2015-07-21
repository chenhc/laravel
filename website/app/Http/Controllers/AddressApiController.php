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
use DB;

class AddressApiController extends Controller 
{
    public function country(Request $request, $country_code)
    {
         $country = DB::table('country')->where('id','=',$country_code)->get();
         if(count($country) == 0)
         	return response()->json( ['ret_code'=>1 , 'ret_msg'=>'country code incorrect'] );

         $provinces = DB::table('province')->where('country_id','=',$country[0]->id)->get();  
         foreach ($provinces as $province) 
         {
             $cities = DB::table('city')->where('province_id','=',$province->id)->get();
             foreach ($cities as $city) 
             {
                 $districts = DB::table('district')->where('city_id','=',$city->id)->get();
                 $city->districts = $districts;
             }
             $province->cities = $cities;
         }
         $country[0]->provinces = $provinces;
         return response()->json( ['ret_code'=>0 , 'ret_msg'=>'success' , 'country'=>$country[0] ] );
    }

    public function district(Request $request, $country_code, $province_code,
            $city_code, $district_code)
    {
        $streets = DB::table('street')->where('district_id','=',$district_code)->get();
        if(count($streets) == 0)
        	return response()->json( ['ret_code'=>1 , 'ret_msg'=>'district code incorrect'] );
        else
        	return response()->json( ['ret_code'=>0 , 'ret_msg'=>'success' , 'streets'=>$streets] );
    }

}