<?php namespace App\Http\Controllers;

use App\FoodRecipe;

use App\Http\Requests;
use App\Http\Controllers\Controller;

use Illuminate\Http\Request;

class FoodRecipeApiController extends Controller {

    public function store(Request $request)
    {
        //
        $this->validate($request, [
            'name' => 'required|unique|max:255',
            'hash' => 'required|unique|max:32',
            'method' => 'required|max:255',
            'difficulty' => 'required|max:255',
            'amount' => 'required|numeric',
            'taste' => 'required|max:255',
            'primaries' => 'required',
            'accessories' => 'required',
            'procedure' => 'required',
        ]);

        $Recipe = new FoodRecipe($request->all());
        $Recipe->save();
    }

    public function destroy(Request $request, $hash)
    {
        //
        $Recipe = FoodRecipe::where(['hash' => $hash])->first();
        if (!$Recipe) {
            return response()->json(['reason' => 'item not found']);
        }

        FoodRecipe::destroy($Recipe->id);
        return response()->json(true);
    }

    public function fetch(Request $request, $hash)
    {
        //
        $Recipe = FoodRecipe::where(['hash' => $hash])->first();
        if (!$Recipe) {
            return response()->json(['reason' => 'item not found']);
        }

        return response()->json($Recipe);
    }

    public function update(Request $request, $hash)
    {
        //
        $this->validate($request, [
            'name' => 'required|unique|max:255',
            'hash' => 'required|unique|max:32',
            'method' => 'required|max:255',
            'difficulty' => 'required|max:255',
            'amount' => 'required|numeric',
            'taste' => 'required|max:255',
            'primaries' => 'required',
            'accessories' => 'required',
            'procedure' => 'required',
        ]);

        $Recipe = FoodRecipe::where(['hash' => $hash])->first();
        if (!$Recipe) {
            return response()->json(['reason' => 'item not found']);
        }

        foreach ($request->all() as $attr => $value) {
            $Recipe->$attr = $value;
        }

        $Recipe->save();
    }

    public function index(Request $request) {
        $category = $request->input('category');
        $pagesize = $request->input('pagesize', 10);
        $page = $request->input('page', 1);
        $offset = $pagesize * ($page - 1);
        $recipes = FoodRecipe::where(['category' => $category])
            ->skip($offset)->take($pagesize)->get();
        return response()->json($recipes);
    }

}
