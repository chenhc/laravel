<?php namespace App\Http\Controllers;

use App\FoodMaterial;

use App\Http\Requests;
use App\Http\Controllers\Controller;

use Illuminate\Http\Request;

class FoodMaterialApiController extends Controller {

    public function store(Request $request)
    {
        //
        $this->validate($request, [
            'name' => 'required|unique|max:255',
            'hash' => 'required|unique|max:32',
            'category' => 'required|max:255',
        ]);

        $material = new FoodMaterial($request->all());
        $material->save();
    }

    public function destroy(Request $request, $hash)
    {
        //
        $material = FoodMaterial::where(['hash' => $hash])->first();
        if (!$material) {
            return response()->json(['reason' => 'item not found']);
        }

        FoodMaterial::destroy($material->id);
        return response()->json(true);
    }

    public function fetch(Request $request, $hash)
    {
        //
        $material = FoodMaterial::where(['hash' => $hash])->first();
        if (!$material) {
            return response()->json(['reason' => 'item not found']);
        }

        return response()->json($material);
    }

    public function update(Request $request, $hash)
    {
        //
        $this->validate($request, [
            'name' => 'required|unique|max:255',
            'hash' => 'required|unique|max:32',
            'category' => 'required|max:255',
        ]);

        $material = FoodMaterial::where(['hash' => $hash])->first();
        if (!$material) {
            return response()->json(['reason' => 'item not found']);
        }

        foreach ($request->all() as $attr => $value) {
            $material->$attr = $value;
        }

        $material->save();
    }

}
