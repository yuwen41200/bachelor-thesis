<?php

require_once __DIR__ . '/vendor/autoload.php';

// destroy these before making the source code public
$secretKey = '3a9c3467214697db53d6ff29a96f52d7';
$accessToken = 'EAARZCIAZCAqZA4BAAZBZBBBQ4ssGXohyK4gltqUIUIs9WGiv3soZCerJZAI2NgYBt'.
               'UZBGMzXTTMDu4Xj5KJNnNnEi5dlcveO1ZCF2KfYwHmopySSXCm1l4unAR43EJDc777'.
               '7JW0SQahjrkF1h5hS2FvappGjbjFu64Et3xmwOV9YZB0k8bWOcSPHGF';

$fb = new Facebook\Facebook([
	'app_id' => '1265675586808222',
	'app_secret' => $secretKey,
	'default_graph_version' => 'v2.7',
]);

$fb->setDefaultAccessToken($accessToken);

try {
	$response = $fb->get('/me?fields=id,name');
	$plainArray = $response->getDecodedBody();
	$userNode = $response->getGraphUser();
}
catch(Facebook\Exceptions\FacebookResponseException $e) {
	die('Graph API Error: ' . $e->getMessage() . PHP_EOL);
}
catch(Facebook\Exceptions\FacebookSDKException $e) {
	die('Facebook SDK Error: ' . $e->getMessage(). PHP_EOL);
}

var_dump($plainArray);
echo $userNode->getId() . ', ' . $userNode->getName() . PHP_EOL;
