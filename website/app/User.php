<?php

namespace App;

use Illuminate\Auth\Authenticatable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Auth\Passwords\CanResetPassword;
use Illuminate\Contracts\Auth\Authenticatable as AuthenticatableContract;
use Illuminate\Contracts\Auth\CanResetPassword as CanResetPasswordContract;

class User extends Model implements AuthenticatableContract, CanResetPasswordContract
{
    use Authenticatable, CanResetPassword;

    /**
     * The database table used by the model.
     *
     * @var string
     */
    protected $table = 'user';

    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = ['username', 'email', 'password'];

    /**
     * The attributes excluded from the model's JSON form.
     *
     * @var array
     */
    protected $hidden = ['id', 'password', 'remember_token', 'created_at', 'updated_at'];

    protected $guarded = array('id');

    public function get_liked_materials() 
    {
        return $this->belongsToMany('App\FoodMaterial', 'user_like_material', 'user_id', 'material_id');
    }

    public function get_liked_recipes()
    {
        return $this->belongsToMany('App\FoodRecipe', 'user_like_recipe', 'user_id', 'recipe_id');
    }
}
