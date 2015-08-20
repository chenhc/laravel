<?php namespace App\Http\Controllers;

use App\Http\Requests;
use App\Http\Controllers\Controller;

use Illuminate\Http\Request;
use Redis;

class HotApiController extends Controller {

    // 获取热门食谱
    public function fetchHotRecipes(Request $request) {
        $value = Redis::get('hot_recipes');
        $value = json_decode($value, true);
        return response()->json([
            'status' => true,
            'data' => $value['data'],
            'update_time' => $value['updatetime'],
        ]);
    }

    // 获取热门食材
    public function fetchHotMaterials(Request $request) {
        $value = Redis::get('hot_materials');
        $value = json_decode($value, true);
        return response()->json([
            'status' => true,
            'data' => $value['data'],
            'update_time' => $value['updatetime'],
        ]);
    }

    // 获取热门运动
    public function fetchHotSports(Request $request) {
        $value = Redis::get('hot_sports');
        $value = json_decode($value, true);
        return response()->json([
            'status' => true,
            'data' => $value['data'],
            'update_time' => $value['updatetime'],
        ]);
    }

    // 获取健康Tips（生活百科）
    public function fetchHealthTips(Request $request) {
        $value = Redis::get('health_tips');
        $value = json_decode($value, true);
        return response()->json([
            'status' => true,
            'data' => $value['data'],
            'update_time' => $value['updatetime'],
        ]);
    }

    // 获取一天量的食谱
    public function fetchOneDayRecipes(Request $request) {
        $value = Redis::get('one_day_recipes');
        $value = json_decode($value, true);
        return response()->json([
            'status' => true,
            'data' => $value,
        ]);
    }

    // 获取当前季节（时令）易发的疾病
    public function fetchSeasonalDiseases(Request $request) {
        $value = Redis::get('seasonal_diseases');
        $value = json_decode($value, true);
        return response()->json([
            'status' => true,
            'season' => $value['season'],
            'data' => $value['data'],
        ]);
    }
}

