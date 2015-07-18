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

class FoodMaterialTest extends TestCase
{
    public function testGet()
    {
        $this->get('/api/food_material/57a799ee774bd4389153dc3012ae6fa0')
            ->seeJson([
                'name' => '大黄米',
            ]);
    }
}
