<?php


class TestCase extends Illuminate\Foundation\Testing\TestCase
{
    use Illuminate\Foundation\Testing\DatabaseMigrations;

    /**
     * The base URL to use while testing the application.
     *
     * @var string
     */
    protected $baseUrl = 'http://localhost';


    /**
     * Creates the application.
     *
     * @return \Illuminate\Foundation\Application
     */
    public function createApplication()
    {
        $app = require __DIR__.'/../bootstrap/app.php';

        $app->make(Illuminate\Contracts\Console\Kernel::class)->bootstrap();

        return $app;
    }


    public function requestJson($method, $uri, array $data = [],
            array $headers = [], $with_csrf_token = false)
    {
        // 初始化会话，不然CSRF检查会失败
        $this->withSession([]);

        // 初始化请求头、数据和参数
        $headers['Content-Type'] = 'application/json';
        $server = $this->transformHeadersToServerVars($headers);
        $json = json_encode($data);
        $data = $with_csrf_token ? ['_token' => csrf_token()] : [];

        $this->call($method, $uri, $data, [], [], $server, $json);

        return $this;
    }


    // POST请求
    public function postJson($uri, array $data = [], array $headers = [],
            $with_csrf_token = false)
    {
        return $this->requestJson('POST', $uri, $data, $headers,
                    $with_csrf_token);
    }


    public function postJsonWithCsrf($uri, array $data = [], array $headers = [])
    {
        return $this->postJson($uri, $data, $headers, true);
    }


    // DELETE请求
    public function deleteJson($uri, array $data = [], array $headers = [],
            $with_csrf_token = false)
    {
        return $this->requestJson('DELETE', $uri, $data, $headers,
                    $with_csrf_token);
    }


    public function deleteJsonWithCsrf($uri, array $data = [], array $headers = [])
    {
        return $this->deleteJson($uri, $data, $headers, true);
    }


    // PUT请求
    public function putJson($uri, array $data = [], array $headers = [],
            $with_csrf_token = false)
    {
        return $this->requestJson('PUT', $uri, $data, $headers,
                    $with_csrf_token);
    }


    public function putJsonWithCsrf($uri, array $data = [], array $headers = [])
    {
        return $this->putJson($uri, $data, $headers, true);
    }
}
