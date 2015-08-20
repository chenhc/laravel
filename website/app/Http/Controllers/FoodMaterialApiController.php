<?php namespace App\Http\Controllers;

use App\FoodMaterial;

use App\Http\Requests;
use App\Http\Controllers\Controller;

use Illuminate\Http\Request;

use Redis;

class FoodMaterialApiController extends Controller {

    protected function create(array $data)
    {
        FoodMaterial::create([
            'name' => $data['name'],
            'hash' => $data['hash'],
            'category' => $data['category'],
        ]);
    }
    public function store(Request $request)
    {
        //
        $this->validate($request, [
        ]);

        $material = $this->create($request->json()->all());
        return response()->json([
            'status' => true,
        ]);
    }

    public function destroy(Request $request, $hash)
    {
        //
        $material = FoodMaterial::where(['hash' => $hash])->first();
        if (!$material) {
            return response()->json([
                'status' => false,
                'reason' => 'item not exists'
            ]);
        }

        FoodMaterial::destroy($material->id);
        return response()->json([
            'status' => true
        ]);
    }

    public function fetch(Request $request, $hash)
    {
        //
        $material = FoodMaterial::where(['hash' => $hash])->first();
        if (!$material) {
            return response()->json([
                'status' => false,
                'reason' => 'item not exists'
            ]);
        }

        return response()->json([
            'status' => true,
            'data' => $material
        ]);
    }

    public function update(Request $request, $hash)
    {
        //
        $this->validate($request, [
        ]);

        $material = FoodMaterial::where(['hash' => $hash])->first();
        if (!$material) {
            return response()->json([
                'status' => false,
                'reason' => 'item not exists'
            ]);
        }

        foreach ($request->json()->all() as $attr => $value) {
            $material->$attr = $value;
        }

        $material->save();

        return response()->json([
            'status' => true,
        ]);
    }

    public function index(Request $request)
    {
        $classification = $request->input('classification');
        $category = $request->input('category');
        $pagesize = $request->input('pagesize', 8);
        $page = $request->input('page', 1);
        $offset = $pagesize * ($page - 1);
        if ($classification)
        {
            $materials = FoodMaterial::where('classification', $classification);
            if ($category)
            {
                $materials = $materials->where('category', $category);
            }
            $totalMaterials = $materials->count();
            $materials = $materials->skip($offset)->take($pagesize)->get();
        }
        else
        {
            $totalMaterials = FoodMaterial::all()->count();
            $materials = FoodMaterial::skip($offset)->take($pagesize)->get();
        }
        $totalPage = getTotalPage($totalMaterials, $pagesize);
        return response()->json([
            'status' => true,
            'data' => $materials,
            'totalPage' => $totalPage,
        ]);
    }
}
