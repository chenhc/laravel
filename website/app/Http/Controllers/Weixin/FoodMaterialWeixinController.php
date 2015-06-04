<?php

/**
 * FileName:   FoodMaterialWeixinController.php
 * Author:     Chen Yanfei
 * @contact:   fasionchan@gmail.com
 * @version:   $Id$
 *
 * Description:
 *
 * Changelog:
 *
 **/

namespace App\Http\Controllers\Weixin;

use App\FoodMaterial;

use App\Http\Requests;
use App\Http\Controllers\Controller;

use Illuminate\Http\Request;

class FoodMaterialWeixinController extends Controller {

    public function display(Request $request, $hash)
    {
        //
        $material = FoodMaterial::where(['hash' => $hash])->first();
        if (!$material) {
            return response()->json(['reason' => 'item not found']);
        }

        return view('weixin/food_material', $material);
        return response()->json($material);
    }
}
