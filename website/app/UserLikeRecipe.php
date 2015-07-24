<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class UserLikeRecipe extends Model {

    protected $table = 'user_like_recipe';

    protected $fillable = ['user_id', 'recipe_id'];

    protected $hidden = ['id', 'created_at', 'updated_at'];

}
