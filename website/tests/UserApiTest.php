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

    private $user;
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

        $this->withSession([])->postJsonCsrf('/api/user', [
                'username' => $user->username,
                'password' => $user->password,
            ])
            ->seeJson([
                'status' => true,
            ]);

        User::where('username', $user->username)->first()->delete();
    }


    public function testDestroy()
    {
    }


    public function testFetch()
    {

    }


    // 测试用户名登陆
    public function testLoginWithUserName()
    {
        $this->withSession([])->postJsonCsrf('/api/user/login', [
                'account' => $this->test_user->username,
                'password' => '12345678',
            ])->seeJson([
                'status' => true,
            ]);
    }


    // 测试用户名登陆失败情况
    public function testLoginWithUserNameFailed()
    {
        $this->withSession([])->postJsonCsrf('/api/user/login', [
                'account' => $this->test_user->username,
                'password' => '87654321',
            ])->seeJson([
                'status' => false,
            ]);
    }

    // 测试邮箱登陆
    public function testLoginWithEmail()
    {
        $this->withSession([])->postJsonCsrf('/api/user/login', [
                'account' => $this->test_user->email,
                'password' => '12345678',
            ])->seeJson([
                'status' => true,
            ]);
    }


    // 测试邮箱登陆失败情况
    public function testLoginWithEmailFailed()
    {
        $this->withSession([])->postJsonCsrf('/api/user/login', [
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
