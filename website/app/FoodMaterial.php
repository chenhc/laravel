<?php namespace App;

use Illuminate\Database\Eloquent\Model;

class FoodMaterial extends Model {

    // table name
    protected $table = 'food_material';

    protected $guarded = array('id');

    // hidden from json
    protected $hidden = ['created_at', 'updated_at'];

}
