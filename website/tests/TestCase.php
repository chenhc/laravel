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


    public function postJson($uri, array $data = [], array $headers = [],
            $with_csrf_token = false)
    {
        $headers['Content-Type'] = 'application/json';
        $server = $this->transformHeadersToServerVars($headers);
        $json = json_encode($data);
        $data = $with_csrf_token ? ['_token' => csrf_token()] : [];

        $this->call('POST', $uri, $data, [], [], $server, $json);

        return $this;
    }


    public function postJsonCsrf($uri, array $data = [], array $headers = [])
    {
        return $this->postJson($uri, $data, $headers, true);
    }
}
