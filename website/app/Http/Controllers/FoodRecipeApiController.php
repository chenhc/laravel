<?php namespace App\Http\Controllers;

use App\FoodRecipe;

use App\Http\Requests;
use App\Http\Controllers\Controller;

use Illuminate\Http\Request;

use Redis;

class FoodRecipeApiController extends Controller {

    public function store(Request $request)
    {
        //
        $this->validate($request, [
        ]);

        $Recipe = new FoodRecipe($request->json()->all());
        $Recipe->save();
        return response()->json([
            'status' => true,
        ]);
    }

    public function destroy(Request $request, $hash)
    {
        //
        $Recipe = FoodRecipe::where(['hash' => $hash])->first();
        if (!$Recipe) {
            return response()->json([
                'status' => false,
                'reason' =>'item not exists'
            ]);
        }

        FoodRecipe::destroy($Recipe->id);
        return response()->json([
            'status' => true,
        ]);
    }

    public function fetch(Request $request, $hash)
    {
        //
        $Recipe = FoodRecipe::where(['hash' => $hash])->first();
        if (!$Recipe) {
            return response()->json([
                'status' => false,
                'reason' =>'item not exists'
            ]);
            return response()->json(['reason' => 'item not found']);
        }

        return response()->json([
            'status' => true,
            'data' => $Recipe,
        ]);
    }

    public function update(Request $request, $hash)
    {
        //
        $this->validate($request, [
        ]);

        $Recipe = FoodRecipe::where(['hash' => $hash])->first();
        if (!$Recipe) {
            return response()->json([
                'status' => false,
                'reason' =>'item not exists'
            ]);
        }

        foreach ($request->json()->all() as $attr => $value) {
            $Recipe->$attr = $value;
        }

        $Recipe->save();
        return response()->json([
            'status' => true,
        ]);
    }

    public function index(Request $request) {
        $pagesize = $request->input('pagesize', 10);
        $page = $request->input('page', 1);
        $offset = $pagesize * ($page - 1);
        $totalPage = FoodRecipe::count();
        $recipes = FoodRecipe::skip($offset)->take($pagesize)->get();
        $remian = $totalPage % $pagesize;
        $totalPage = floor($totalPage / $pagesize);
        if ($remian)
            $totalPage += 1;
        return response()->json([
            'status' => true,
            'data' => $recipes,
            'totalPage' => $totalPage,
        ]);
    }
}
