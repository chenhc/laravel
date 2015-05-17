<?php namespace App;

use Illuminate\Database\Eloquent\Model;

class FoodRecipe extends Model {

    // table_name
	protected $table = 'food_recipe';


    protected $guarded = array('id');

    // hidden from json
    protected $hidden = ['created_at', 'updated_at'];
}
