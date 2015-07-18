<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;

class HelperServiceProvider extends ServiceProvider
{

    protected $namespace = 'App\Http\Controllers';

    public function register()
    {
        foreach (glob(app_path().'/Helpers/*.php') as $filename) {
            require_once($filename);
        }
    }
}
