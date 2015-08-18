<?php namespace App\Http\Controllers;

use App\Http\Requests;
use App\Http\Controllers\Controller;

use Illuminate\Http\Request;

use Redis;

class CategoryApiController extends Controller {

    public function fetchFmCategory(Request $request)
    {
        $classifications = Redis::command('smembers', ['material_classifications']);
        $value = [];
        foreach ($classifications as $classification)
        {
            $categories = Redis::command('hmget', ['fm_classification2category', $classification]);
            $categories = json_decode($categories[0]);
            $value = array_add($value, $classification, $categories);
        }
        return response()->json([
            'status' => true,
            'data' => $value,
        ]);
    }

    public function fetchFrCategory(Request $request)
    {
        $classifications = Redis::command('smembers', ['recipe_classifications']);
        $value = [];
        foreach ($classifications as $classification)
        {
            $categories = Redis::command('hmget', ['fr_classification2category', $classification]);
            $categories = json_decode($categories[0]);
            $value = array_add($value, $classification, $categories);
        }
        return response()->json([
            'status' => true,
            'data' => $value,
        ]);
    }
}
