<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class MaterialLike extends Model {

    // table name
    protected $table = 'user_like_material';

    protected $fillable = ['user_id', 'material_id'];

    protected $hidden = ['id', 'created_at', 'updated_at'];


}
