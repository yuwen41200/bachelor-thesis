<?php

require_once __DIR__ . '/vendor/autoload.php';
require_once 'safe_facebook.php';

$secretKey = '3a9c3467214697db53d6ff29a96f52d7';
$accessToken = 'EAARZCIAZCAqZA4BACZCqbD1Na3bpcCzMOSbRABs6ciq1cbawtJoRIQ0fyOA7Nqb'.
               'rsGXMZA1Y7do5ZBRtDC883fFcaIQiohYIoQPz4sarN601ZCv1lgtu6naTRz097ZB'.
               'tQHzmCvOEiTBZAiZBqLoZCZCxYIUEUe6zdI8xglQQkf5tgXaD01cZAokHTPCkCq1'.
               'k6YT18daZAOtdrA1y8iCeUyNAU81JIM';

$fb = new SafeFacebook\SafeFacebook([
	'app_id' => '1265675586808222',
	'app_secret' => $secretKey,
	'default_graph_version' => 'v2.7',
]);
$fb->setDefaultAccessToken($accessToken);

$input = readline();
try {
	$response = $fb->get('/' . $input . '?fields=name');
	$output = $response->getGraphNode()->asArray();
	print($output['name'] . PHP_EOL);
}
catch (Facebook\Exceptions\FacebookResponseException $e) {
	print('Graph API Error: ' . $e->getMessage() . PHP_EOL);
	exit(1);
}
catch (Facebook\Exceptions\FacebookSDKException $e) {
	print('Facebook SDK Error: ' . $e->getMessage() . PHP_EOL);
	exit(1);
}
