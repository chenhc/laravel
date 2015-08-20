<?php

namespace App\Http\Controllers\Weixin;

use App\FoodRecipe;

use App\Http\Requests;
use App\Http\Controllers\Controller;

use Illuminate\Http\Request;

class FoodRecipeWeixinController extends Controller {

    public function display(Request $request, $hash)
    {
        //
        $recipe = FoodRecipe::where(['hash' => $hash])->first();
        if (!$recipe) {
            return response()->json(['reason' => 'item not found']);
        }

        return view('weixin/food_recipe', $recipe);
        return response()->json($recipe);
    }
}
