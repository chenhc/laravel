<?php namespace App;

use Illuminate\Database\Eloquent\Model;

class FoodMaterialCategoryView extends Model {

    // table name
    protected $table = 'fm_category_map_view';

    protected $guarded = array('id');

    // hidden from json
    protected $hidden = ['id', 'classification', 'category', 'material_id'];

}
