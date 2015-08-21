<?php namespace App;

use Illuminate\Database\Eloquent\Model;

class FoodRecipeCategoryView extends Model {

    // table name
    protected $table = 'fr_category_map_view';

    protected $guarded = array('id');

    // hidden from json
    protected $hidden = ['id', 'classification', 'category', 'recipe_id'];

}
