<?php

require_once __DIR__ . '/vendor/autoload.php';
require_once 'safe_facebook.php';

$fp = fopen('target_list_serialized.dat', 'r');
$unserialized = fread($fp, filesize('target_list_serialized.dat'));
fclose($fp);
$targetList = unserialize($unserialized);

// destroy these before making the source code public
$secretKey = '3a9c3467214697db53d6ff29a96f52d7';
$accessToken = 'EAARZCIAZCAqZA4BAKqTcW8RUkJOgaEIrOrS22UMzXiqZCM95OLTa1mrmxhzPd2ZCTwfWBD'.
               'D4fYPgbFJZBZCl37iLxDtjjWZBbTxS61mxsL5VGrZAwRG1fMQZCES3mQi3uyhcsQwFUIs3w'.
               'jZBdxbCm5CDsVIahpFfzreIgPNhWdTsaWludJuKsg0j1eMNNrGdD3e2uYZD';

$fb = new SafeFacebook\SafeFacebook([
	'app_id' => '1265675586808222',
	'app_secret' => $secretKey,
	'default_graph_version' => 'v2.7',
]);

// $oauth = $fb->getOAuth2Client();
// $accessToken = $oauth->getLongLivedAccessToken($accessToken);
// print_r($accessToken);
$fb->setDefaultAccessToken($accessToken);

$fullTargetList = array();
foreach ($targetList as $item) {
	try {
		$response = $fb->get('/search?q=' . rawurlencode($item) . '&type=page');
		$targetId = ($response->getGraphEdge()->asArray())[0]['id'];
		if ($targetId) {
			$response = $fb->get('/' . $targetId . '?fields=name,fan_count');
			$target = $response->getGraphNode()->asArray();
			$fullTargetList[] = $target;
			print_r($target);
		}
		else
			echo '"' . $item . '" not found' . PHP_EOL;
	}
	catch (Facebook\Exceptions\FacebookResponseException $e) {
		echo 'Graph API Error: ' . $e->getMessage() . PHP_EOL;
	}
	catch (Facebook\Exceptions\FacebookSDKException $e) {
		echo 'Facebook SDK Error: ' . $e->getMessage() . PHP_EOL;
	}
}

usort($fullTargetList, 'compareTarget');
print_r($fullTargetList);

$serialized = serialize($fullTargetList);
$fp = fopen('target_list_serialized_ng.dat', 'w');
fwrite($fp, $serialized);
fclose($fp);

function compareTarget($a, $b) {
	return $a['fan_count'] - $b['fan_count'];
}
