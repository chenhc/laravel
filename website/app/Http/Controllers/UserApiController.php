<?php namespace App\Http\Controllers;

use App\User;

use App\Http\Requests;
use App\Http\Controllers\Controller;

use Illuminate\Http\Request;

use Auth, Redirect, Input, Session;

class UserApiController extends Controller {


    public function __construct(Request $request)
    {
        $this->session=$request->session();
    }

    private function birth2Group($birth)
    {
        list($by, $bm, $bd) = explode('-', $birth);
        $cm = date('n');
        $cd = date('j');
        $age = date('Y')-$by-1;
        if ($cm > $bm || $cm == $bm && $cd > $bd) 
            $age++;
        if ($age < 1)
            $group = '婴儿';
        else if ($age < 3)
            $group = '幼儿';
        else if ($age < 6)
            $group = '儿童';
        else if ($age < 14)
            $group = '少年';
        else if ($age < 45)
            $group = '青年';
        else if ($age < 60)
            $group = '中年';
        else 
            $group = '老年';
        return $group;
    }

    public function login(Request $request)
    {
        $email = Input::get('email');
        $password = Input::get('password');
        if (Auth::attempt(['email' => $email, 'password' => $password]))
        {

            $user=Auth::user();
            $this->session->put($user->attributesToArray());
            $group = $this->birth2Group($user->birthday);
            Session::put('group', $group);	
            return response()->json(['result'=> 'login success']);
        }
        else
            return response()->json(['result'=> 'login fail', 'reason'=>'用户名或密码不正确']);

    }

    public function logout()
    {
        $this->session->flush();

        Auth::logout();
        return json_encode('You are logged out');

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

}
