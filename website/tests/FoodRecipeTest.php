<?php

/**
 * FileName:   FoodRecipeTest.php
 * Author:     Chen Yanfei
 * @contact:   fasionchan@gmail.com
 * @version:   $Id$
 *
 * Description:
 *
 * Changelog:
 *
 **/

use App\FoodRecipe;

class FoodRecipeTest extends TestCase
{

    private $test_recipe;

    public function setUp()
    {
        parent::setUp();
        $this->test_recipe = factory(FoodRecipe::class)->create();
    }

    // 测试新增食材
    public function testStore()
    {
        $hash = str_random(16);
        $this->postJsonWithCsrf('/api/food_recipe', [
            "tags" => "热菜,幼儿,家常菜",
            "taste" => "咸鲜味",
            "accessories" => "胡萝卜,鸡蛋,食盐,葱,姜,料酒",
            "setup_time" => "30分钟",
            "difficulty" => "初中水平",
            "cook_time" => "<5分钟",
            "name" => "蒸鱼丸",
            "amount" => "2人份",
            "primaries" => "草鱼",
            "method" => "蒸",
            "procedure" => "草鱼段洗净片去鱼骨
            http://images.meishij.net/p/20140226/3e368bf98b975390cbc1e8aa220b69ca.jpg
            去鱼皮切成几小片
            http://images.meishij.net/p/20140226/bb25dd997a5da5d6dd8696b4b6e606e2.jpg
            将鱼肉放入搅拌机搅打成鱼蓉
            http://images.meishij.net/p/20140226/b2b9d75e7b5186cd73773e2e16c1ef30.jpg
            鱼蓉放入容器，加入盐、料酒、葱姜末
            http://images.meishij.net/p/20140226/4a79452aa67d4213a4dd21276936b7c4.jpg
            鸡蛋只取蛋清，加入鱼蓉，顺同一方向将鱼蓉搅拌上劲腌制15分钟
            http://images.meishij.net/p/20140226/70dfcce7289b29137dea7de45cbeed67.jpg
            腌制好的鱼蓉搓成等量的小丸子
            http://images.meishij.net/p/20140226/730fea1d3b8f4b1f2e2441a11589101f.jpg
            胡萝卜洗净去皮切成薄片放置盘内，将鱼丸放在胡萝卜片上，放入烧开水的蒸锅内
            http://images.meishij.net/p/20140226/cd9ae90c177cc8bea58b0510b4a78d36.jpg
            大火蒸3分钟至鱼丸熟透即可
            http://images.meishij.net/p/20140226/5a4567d1437f3294b3634f0e0b540c99.jpg
            http://images.meishij.net/p/20140226/553babea39175063b9ae5911abd1d38f.jpg
            http://images.meishij.net/p/20140226/17ca3352a7ea2be7bfa3ee2dab4a8d93.jpg
            1、鱼肉营养丰富，含维生素A、铁、钙、磷等，具有滋补健胃、利水消肿、通乳、清热解毒、止嗽下气的功效；
            2、鱼丸的大小直接关系到蒸制时间，做给小宝宝吃的鱼丸不宜过大；
            3、鱼类所含的DHA，它们在人体内主要是存在脑部、视网膜和神经中。DHA可维持视网膜正常功能，婴儿尤其需要此种养份，促进视力健全发展；DHA也对人脑发育及智能发展有极大的助益，亦是神经系统成长不可或缺的养份。",
            'hash' => $hash,
        ])
        ->seeJson([
            'status' => true,
        ])
        ->seeInDatabase('food_recipe', [
            "name" => "蒸鱼丸",
        ]);
        FoodRecipe::where('hash', $hash)->first()->delete();
    }

    public function testFetch()
    {
        $this->get('/api/food_recipe/' . $this->test_recipe->hash)
            ->seeJson([
                'status' => true,
            ]);
    }

    public function testFetchWithFailed()
    {
        $this->get('/api/food_recipe/zhangfan')
            ->seeJson([
                'status' => false,
            ]);
    }

    public function testDestroy()
    {
        $recipe = factory(FoodRecipe::class)->create();

        $this->deleteJsonWithCsrf('/api/food_recipe/' . $recipe->hash)
        ->seeJson([
            'status' => true,
        ])
        ->notSeeInDatabase('food_recipe', [
            'name' => $recipe->name,
        ]);

    }

    public function testUpdate()
    {
        $recipe = factory(FoodRecipe::class)->create();

        $this->putJsonWithCsrf('/api/food_recipe/' . $recipe->hash, [
            'difficulty' => $recipe->difficulty,
        ])->seeJson([
            'status' => true,
        ]);

        FoodRecipe::destroy($recipe->id);
    }

    public function testIndex()
    {
        $this->get('/api/food_recipe?page=1')
            ->seeJson([
                'status' => true,
            ]);
    }

    public function tearDown()
    {
        FoodRecipe::destroy($this->test_recipe->id);

        parent::tearDown();
    }
}
