<?php namespace App\Http\Controllers;

use App\MaterialLike;
use App\User;
use App\FoodMaterial;

use App\Http\Requestes;
use App\Http\Controllers\Controller;

use Illuminate\Http\Request;

use Auth;

class MaterialLikeApiController extends Controller
{
    
    public function like(Request $request)
    {
        $user = Auth::user();
        if (!$user)
        {
            return response()->json(['reason' => 'didn\'t login']);
        }
        $material_hash = $request->input('material_hash');
        $material_id = FoodMaterial::where('hash', $material_hash)->first()->id;
        $user_id = $user->id;
        $user_like = new MaterialLike;
        $user_like->user_id = $user_id;
        $user_like->material_id = $material_id;
        $user_like->save();
        return response()->json(['result' => 'success']);
    }
    
    public function dislike(Request $request)
    {
        $user = Auth::user();
        if (!$user)
        {
            return response()->json(['reason' => 'didn\'t login']);
        }
        $material_hash = $request->input('material_hash');
        $material_id = FoodMaterial::where('hash', $material_hash)->first()->id;
        $user_id = $user->id;
        MaterialLike::where('user_id', $user_id)->where('material_id', $material_id)->first()->delete();
        return response()->json(['result' => 'success']);
    }

    public function index(Request $request)
    {
        $user = Auth::user();
        if (!$user)
        {
            return response()->json(['reason' => 'didn\'t login']);
        }
        $user_id = $user->id;
        $pagesize = $request->input('pagesize', 10);
        $page = $request->input('page', 1);
        $offset = $pagesize * ($page - 1);
        $materials = User::find($user_id)->material_likes->slice($offset, $pagesize);
        return response()->json($materials);
    }

}
