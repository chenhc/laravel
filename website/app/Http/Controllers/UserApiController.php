<?php

namespace App\Http\Controllers;

use App\User;
use App\FoodMaterial;
use App\FoodRecipe;
use App\UserLikeMaterial;
use App\UserLikeRecipe;

use App\Http\Requests;
use App\Http\Controllers\Controller;

use Illuminate\Http\Request;

use Auth, Redirect, Input, Session;

class UserApiController extends Controller {


    public function __construct(Request $request)
    {
        $this->session=$request->session();
    }

    private function get_age_bracket($birthday)
    {
        $birthday = new \DateTime($birthday);
        $today = new \DateTime('today');
        $age = $birthday->diff($today)->y;

        if ($age < 1)
            $bracket = '婴儿';
        else if ($age < 3)
            $bracket = '幼儿';
        else if ($age < 6)
            $bracket = '儿童';
        else if ($age < 14)
            $bracket = '少年';
        else if ($age < 45)
            $bracket = '青年';
        else if ($age < 60)
            $bracket = '中年';
        else
            $bracket = '老年';

        return $bracket;
    }

    public function login(Request $request)
    {
        $email = Input::get('email');
        $password = Input::get('password');
        if (Auth::attempt(['email' => $email, 'password' => $password]))
        {

            $user=Auth::user();
            $this->session->put($user->attributesToArray());
            $age_bracket = $this->get_age_bracket($user->birthday);
            Session::put('age_bracket', $age_bracket);
            return response()->json(['result'=> 'login success']);
        }
        else
            return response()->json(['result'=> 'login fail', 'reason'=>'用户名或密码不正确']);

    }

    public function logout()
    {
        $this->session->flush();

        Auth::logout();
        return response()->json('You are logged out');

    }

    public function store(Request $request)
    {
        //
        $this->validate($request, [

                ]);

        $user = new User($request->all());
        $user->save();
    }

    public function destroy(Request $request, $hash)
    {
        //
        $user = Auth::user();
        if (!$user) {
            return response()->json(['reason' => 'didn\'t login']);
        }

        User::destroy($user->id);
        return response()->json(true);
    }

    public function index()
    {
        //
        $user = Auth::user();
        if (!$user) {
            return response()->json(['reason' => 'didn\'t login']);
        }

        return response()->json($user);
    }

    public function update(Request $request)
    {
        //
        $this->validate($request, [

                ]);

        $user = Auth::user();
        if (!$user) {
            return response()->json(['reason' => 'didn\'t login']);
        }

        foreach ($request->all() as $attr => $value) {
            $user->$attr = $value;
        }

        $user->save();
    }

    public function fetch(Request $request, $hash)
    {
        // sql doesn't have 'hash' field. so temporarily using 'ID'
        $user = User::where(['ID' => $hash])->first();
        if (!$user) {
            return response()->json(['reason' => 'user not found']);
        }

        return response()->json($user);

    }

    public function setLikedMaterial(Request $request)
    {
        $user = Auth::user();
        if (!$user)
        {
            return response()->json(['reason' => 'didn\'t login']);
        }
        $user_id = $user->id;
        $material_hash = $request->input('material_hash');
        $material_id = FoodMaterial::where('hash', $material_hash)->first()->id;
//        $user_like = new UserLikeMaterial;
//        $user_like->user_id = $user_id;
//        $user_like->material_id = $material_id;
//        $user_like->save();
        UserLikeMaterial::create(['user_id' => $user_id, 'material_id' => $material_id]);
        return response()->json(['result' => 'success']);
    }
    
    public function setDislikedMaterial(Request $request)
    {
        $user = Auth::user();
        if (!$user)
        {
            return response()->json(['reason' => 'didn\'t login']);
        }
        $user_id = $user->id;
        $material_hash = $request->input('material_hash');
        $material_id = FoodMaterial::where('hash', $material_hash)->first()->id;
        UserLikeMaterial::where('user_id', $user_id)->where('material_id', $material_id)->first()->delete();
        return response()->json(['result' => 'success']);
    }

    public function fetchLikedMaterials(Request $request)
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
        $materials = User::find($user_id)->get_liked_materials->slice($offset, $pagesize);
        return response()->json($materials);
    }

    public function setLikedRecipe(Request $request)
    {
        $user = Auth::user();
        if (!$user)
        {
            return response()->json(['reason' => 'didn\'t login']);
        }
        $user_id = $user->id;
        $recipe_hash = $request->input('recipe_hash');
        $recipe_id = FoodRecipe::where('hash', $recipe_hash)->first()->id;
        UserLikeRecipe::create(['user_id' => $user_id, 'recipe_id' => $recipe_id]);
        return response()->json(['result' => 'success']);
    }        
    
    public function setDislikedRecipe(Request $request)
    {
        $user = Auth::user();
        if (!$user)
        {
            return response()->json(['reason' => 'didn\'t login']);
        }
        $user_id = $user->id;
        $recipe_hash = $request->input('recipe_hash');
        $recipe_id = FoodRecipe::where('hash', $recipe_hash)->first()->id;
        UserLikeRecipe::where('user_id', $user_id)->where('recipe_id', $recipe_id)->first()->delete();
        return response()->json(['result' => 'success']);
    } 
    
    public function fetchLikedRecipes(Request $request)
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
        $recipes = User::find($user_id)->get_liked_recipes->slice($offset, $pagesize);
        return response()->json($recipes);
    }
}
