<?php

/**
 * FileName:   FoodMaterialTest.php
 * Author:     Chen Yanfei
 * @contact:   fasionchan@gmail.com
 * @version:   $Id$
 *
 * Description:
 *
 * Changelog:
 *
 **/

use App\FoodMaterial;

class FoodMaterialTest extends TestCase
{

    private $test_material;

    public function setUp()
    {
        parent::setUp();
        $this->test_material = factory(FoodMaterial::class)->create();
    }

    // 测试新增食材
    public function testStore()
    {
        $material = factory(FoodMaterial::class)->make();

        $this->postJsonWithCsrf('/api/food_material', [
            'name' => $material->name,
            'hash' => $material->hash,
            'classification' => $material->classification,
            'category' => $material->category,
            'alias' => $material->alias,
            'tags' => $material->tags,
            'image_hash' => $material->image_hash,
        ])
        ->seeJson([
            'status' => true,
        ])
        ->seeInDatabase('food_material', [
            'name' => $material->name,
        ]);

        FoodMaterial::where('hash', $material->hash)->first()->delete();
    }

    public function testFetch()
    {
        $this->get('/api/food_material/' . $this->test_material->hash)
            ->seeJson([
                'status' => true,
            ]);
    }

    public function testFetchWithFailed()
    {
        $this->get('/api/food_material/zhangfan')
            ->seeJson([
                'status' => false,
            ]);
    }

    public function testDestroy()
    {
        $material = factory(FoodMaterial::class)->create();

        $this->deleteJsonWithCsrf('/api/food_material/' . $material->hash)
        ->seeJson([
            'status' => true,
        ])
        ->notSeeInDatabase('food_material', [
            'name' => $material->name,
        ]);

    }

    public function testUpdate()
    {
        $material = factory(FoodMaterial::class)->create();

        $this->putJsonWithCsrf('/api/food_material/' . $material->hash, [
            'image_hash' => $material->image_hash,
        ])->seeJson([
            'status' => true,
        ]);

        FoodMaterial::destroy($material->id);
    }

    public function testIndex()
    {
        $this->get('/api/food_material?category=鱼类&&page=1')
            ->seeJson([
                'status' => true,
            ]);
    }

    public function tearDown()
    {
        FoodMaterial::destroy($this->test_material->id);

        parent::tearDown();
    }
}
