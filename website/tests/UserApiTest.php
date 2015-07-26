<?php

/**
 * FileName:   UserApiTest.php
 * Author:     Chen Yanfei
 * @contact:   fasionchan@gmail.com
 * @version:   $Id$
 *
 * Description:
 *
 * Changelog:
 *
 **/

use App\User;


class UserApiTest extends TestCase
{
    //use Illuminate\Foundation\Testing\WithoutMiddleware;

    private $test_user;


    public function setUp()
    {
        parent::setUp();

        $this->test_user = factory(User::class)->create();
    }


    // 测试新增（注册）用户
    public function testStore()
    {
        $user = factory(User::class)->make();

        $this->postJsonWithCsrf('/api/user', [
                'username' => $user->username,
                'password' => $user->password,
            ])
            ->seeJson([
                'status' => true,
            ])
            ->seeInDatabase('user', [
                    'username' => $user->username,
                ]
            );

        User::where('username', $user->username)->first()->delete();
    }


    // 测试注销用户
    public function testDestroy()
    {
        $user = factory(User::class)->create();

        $this->actingAs($user)
            ->deleteJsonWithCsrf('/api/user/' . $user->hash)
            ->seeJson([
                'status' => true,
            ])
            ->notSeeInDatabase('user', [
                'username' => $user->username,
            ]);
    }


    // 测试更改用户信息
    public function testUpdate()
    {
        $user = factory(User::class)->make();

        $this->actingAs($this->test_user)
            ->putJsonWithCsrf('/api/user/' . $this->test_user->hash, [
                'email' => $user->email,
            ])
            ->seeJson([
                'status' => true,
            ])
            ->seeInDatabase('user', [
                'email' => $user->email,
            ]);
    }


    // 测试获取用户信息
    public function testFetch()
    {
        $this->actingAs($this->test_user)
            ->get('/api/user/' . $this->test_user->hash)
            ->seeJson([
                'username' => $this->test_user->username,
            ]);
    }


    // 测试用户名登陆
    public function testLoginWithUserName()
    {
        $this->postJsonWithCsrf('/api/user/login', [
                'account' => $this->test_user->username,
                'password' => '12345678',
            ])->seeJson([
                'status' => true,
            ]);
    }


    // 测试用户名登陆失败情况
    public function testLoginWithUserNameFailed()
    {
        $this->postJsonWithCsrf('/api/user/login', [
                'account' => $this->test_user->username,
                'password' => '87654321',
            ])->seeJson([
                'status' => false,
            ]);
    }

    // 测试邮箱登陆
    public function testLoginWithEmail()
    {
        $this->postJsonWithCsrf('/api/user/login', [
                'account' => $this->test_user->email,
                'password' => '12345678',
            ])->seeJson([
                'status' => true,
            ]);
    }


    // 测试邮箱登陆失败情况
    public function testLoginWithEmailFailed()
    {
        $this->postJsonWithCsrf('/api/user/login', [
                'account' => $this->test_user->email,
                'password' => '87654321',
            ])->seeJson([
                'status' => false,
            ]);
    }


    public function tearDown()
    {
        User::destroy($this->test_user->id);

        parent::tearDown();
    }
}
