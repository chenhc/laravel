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

use Auth, Redirect, Input;

class UserApiController extends Controller {

    private $json_no_login = [
        'status' => false,
        'reason' => 'no login',
        'hint' => '请先登录',
    ];

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


    protected function create(array $data)
    {
        return User::create([
            'username' => $data['username'],
            'email' => $data['email'],
            'hash' => md5($data['username'] . env('HASH_SALT')),
            'password' => bcrypt($data['password']),
        ]);
    }

    protected function attempt(array $data)
    {
        if (Auth::attempt($data))
        {
            return true;
        }
        else
            return false;
    }

    public function login(Request $request)
    {
        $account = $request->json()->get('account');
        $password = $request->json()->get('password');

        // 用户名登录
        if ($this->attempt(['username' => $account, 'password' => $password]) ||
            // 邮箱登陆
            $this->attempt(['email' => $account, 'password' => $password]))
        {
            $user=Auth::user();
            $request->session()->put($user->attributesToArray());
            $age_bracket = $this->get_age_bracket($user->birthday);
            $request->session()->push('age_bracket', $age_bracket);

            return response()->json([
                'status'=> true
            ]);
            // ->withCookie(cookie('user', $user->name, 69));
        }
        return response()->json([
            'status' => false,
            'reason' => '用户名或密码不正确',
            'account' => $account,
            'password' => $password,
        ]);
    }

    public function logout(Request $request)
    {
        $request->session()->flush();

        Auth::logout();
        return response()->json([
            'status' => true,
        ]);
    }


    // 增
    // 注册用户
    public function store(Request $request)
    {
        // 字段验证
        $this->validate($request, [
        ]);

        // 创建用户并保存到数据库
        $user_data = $request->json()->all();
        $user = $this->create($user_data);
        // $user->save();

        $this->attempt(['username' => $user_data['username'],
            'password' => $user_data['password']]);

        return response()->json([
            'status' => true,
        ]);
    }


    // 删
    // 注销用户
    public function destroy(Request $request, $hash)
    {
        // 用户认证
        $user = Auth::user();
        if (!$user)
        {
            return response()->json($this->json_no_login);
        }

        // 删除用户记录
        User::destroy($user->id);

        return response()->json([
            'status' => true
        ]);
    }


    // 改
    // 修改用户信息
    public function update(Request $request, $hash)
    {
        // 字段验证
        $this->validate($request, [
        ]);

        // 用户认证
        $user = Auth::user();
        if (!$user)
        {
            return response()->json($this->json_no_login);
        }

        // 遍历并更新属性
        foreach ($request->json()->all() as $attr => $value) {
            $user->$attr = $value;
        }

        // 保存更新到数据库
        $user->save();

        return response()->json([
            'status' => true,
            'user' => $user,
        ]);
    }


    // 查
    // 获取用户信息
    public function fetch(Request $request, $hash)
    {
        // 获取本人信息
        $user = Auth::user();
        if ($user && $user->hash == $hash)
        {
            return response()->json($user);
        }

        // 获取其他用户信息
        $user = User::where(['hash' => $hash])->first();
        if ($user)
        {
            return response()->json([
                'username' => $user['username'],
            ]);
        }

        return response()->json([
            'status' => false,
            'reason' => 'user not exists',
            'hint' => '用户不存在',
        ]);
    }


    // 列
    // 搜索用户
    public function index()
    {
        //
        $user = Auth::user();
        if (!$user) {
            return response()->json($this->json_no_login);
        }

        return response()->json([
            'status' => true,
            'data' => $user
            ]);
    }

    public function setLikedMaterial(Request $request)
    {
        $user = Auth::user();
        if (!$user)
        {
            return response()->json($this->json_no_login);
        }
        $user_id = $user->id;
        $material_hash = $request->json()->get('material_hash');
        $material_id = FoodMaterial::where('hash', $material_hash)->first()->id;
        UserLikeMaterial::create(['user_id' => $user_id, 'material_id' => $material_id]);
        return response()->json(['status' => true]);
    }

    public function setDislikedMaterial(Request $request)
    {
        $user = Auth::user();
        if (!$user)
        {
            return response()->json($this->json_no_login);
        }
        $user_id = $user->id;
        $material_hash = $request->json()->get('material_hash');
        $material_id = FoodMaterial::where('hash', $material_hash)->first()->id;
        UserLikeMaterial::where('user_id', $user_id)->where('material_id', $material_id)->first()->delete();
        return response()->json(['status' => true]);
    }

    public function fetchLikedMaterials(Request $request)
    {
        $user = Auth::user();
        if (!$user)
        {
            return response()->json($this->json_no_login);
        }
        $user_id = $user->id;
        $pagesize = $request->input('pagesize', 10);
        $page = $request->input('page', 1);
        $offset = $pagesize * ($page - 1);
        $materials = User::find($user_id)->get_liked_materials;
        $totalPage = getTotalPage($materials->count(), $pagesize);
        $materials = $materials->slice($offset, $pagesize);
        return response()->json([
            'status' => true,
            'data' => $materials,
            'totalPage' => $totalPage,
        ]);
    }

    public function setLikedRecipe(Request $request)
    {
        $user = Auth::user();
        if (!$user)
        {
            return response()->json($this->json_no_login);
        }
        $user_id = $user->id;
        $recipe_hash = $request->json()->get('recipe_hash');
        $recipe_id = FoodRecipe::where('hash', $recipe_hash)->first()->id;
        UserLikeRecipe::create(['user_id' => $user_id, 'recipe_id' => $recipe_id]);
        return response()->json(['status' => true]);
    }

    public function setDislikedRecipe(Request $request)
    {
        $user = Auth::user();
        if (!$user)
        {
            return response()->json($this->json_no_login);
        }
        $user_id = $user->id;
        $recipe_hash = $request->json()->get('recipe_hash');
        $recipe_id = FoodRecipe::where('hash', $recipe_hash)->first()->id;
        UserLikeRecipe::where('user_id', $user_id)->where('recipe_id', $recipe_id)->first()->delete();
        return response()->json(['status' => true]);
    }

    public function fetchLikedRecipes(Request $request)
    {
        $user = Auth::user();
        if (!$user)
        {
            return response()->json($this->json_no_login);
        }
        $user_id = $user->id;
        $pagesize = $request->input('pagesize', 10);
        $page = $request->input('page', 1);
        $offset = $pagesize * ($page - 1);
        $recipes = User::find($user_id)->get_liked_recipes;
        $totalPage = getTotalPage($recipes->count(), $pagesize);
        $recipes = $recipes->slice($offset, $pagesize);
        return response()->json([
            'status' => true,
            'data' => $recipes,
            'total' => $totalPage,
        ]);
    }

    public function validity(Request $request)
    {
        $data = $request->json();
        if ($data->has('username'))
        {
            $name = $data->get('username');
            $user = User::where('username', $name)->first();
            if ($user)
            {
                return response()->json([
                    'status' => false,
                    'reason' => '该用户名已经存在'
                ]);
            }
        }
        if ($data->has('email'))
        {
            $email = $data->get('email');
            $user = User::where('email', $email)->first();
            if ($user)
            {
                return response()->json([
                    'status' => false,
                    'reason' => '该邮箱已经被使用'
                ]);
            }
        }

        return response()->json([
            'status' => true,
        ]);
    }
}
