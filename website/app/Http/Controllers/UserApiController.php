<?php namespace App\Http\Controllers;

use App\User;

use App\Http\Requests;
use App\Http\Controllers\Controller;

use Illuminate\Http\Request;

use Auth, Redirect, Input;

class UserApiController extends Controller {

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