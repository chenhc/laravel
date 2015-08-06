<?php

/*
|--------------------------------------------------------------------------
| Model Factories
|--------------------------------------------------------------------------
|
| Here you may define all of your model factories. Model factories give
| you a convenient way to create models for testing and seeding your
| database. Just tell the factory how a default model should look.
|
*/

$factory->define(App\User::class, function (Faker\Generator $faker) {
    return [
        'username' => $faker->name,
        'hash' => str_random(16),
        'email' => $faker->email,
        'password' => bcrypt('12345678'),
        'remember_token' => str_random(10),
    ];
});

$factory->define(App\FoodMaterial::class, function (Faker\Generator $faker)
{
    return [
        'name' => $faker->name,
        'hash' => str_random(16),
        'classification' => '速食食品',
        'category' => '方便食品类',
        'alias' => $faker->name,
        'tags' => $faker->name,
        'image_hash' => str_random(16),
    ];
});

$factory->define(App\FoodRecipe::class, function (Faker\Generator $faker)
{
    return [
        "tags" => "汤粥,美容",
        "taste" => "甜味",
        "accessories" => "冰糖,纯净水",
        "setup_time" => "数小时",
        "difficulty" => "初级入门",
        "cook_time" => "<60分钟",
        "name" => $faker->name,
        "amount" => "2人份",
        "primaries" => "燕窝",
        "method" => "炖",
        "procedure" => "",
        'hash' => str_random(16),
    ];
});
