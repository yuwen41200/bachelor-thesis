<?php

require_once __DIR__ . '/vendor/autoload.php';
require_once 'safe_facebook.php';

$fp = fopen('target_list_serialized_final.dat', 'r');
$unserialized = fread($fp, filesize('target_list_serialized_final.dat'));
fclose($fp);
$targetList = unserialize($unserialized);

// we are just doing a prototype now
array_splice($targetList, 1);

// destroy these before making the source code public
/* @noinspection SpellCheckingInspection */
$secretKey = '3a9c3467214697db53d6ff29a96f52d7';
/* @noinspection SpellCheckingInspection */
$accessToken = 'EAARZCIAZCAqZA4BAPRkdzg5Pr4oCqHVoMFJYdZBqOzGCQ4sAckcGxgw87ne5F3PPRL0ZAs'.
               'BfFYtoZA4kfZAPLomYHpVCXfNFqdgZCZBHbOdAKJ6HaAWv9EAnRK87KWpqMepkGIkIZAhAV'.
               'lE3dP4uwUeXYRip2GPY2ZBvD87nzFwoezFgD2NP94eRrcywF1ATbLaCiMZD';

$fb = new SafeFacebook\SafeFacebook([
	'app_id' => '1265675586808222',
	'app_secret' => $secretKey,
	'default_graph_version' => 'v2.7',
]);
$fb->setDefaultAccessToken($accessToken);

foreach ($targetList as $target) {
	try {
		$fp = fopen('archive_' . $target['id'] . '.json', 'w');
		fwrite($fp, '[');
		$str = '/' . $target['id'] . '/posts?limit=100&since=2015-10-17&until=2016-01-17';
		$postEdge = $fb->get($str)->getGraphEdge();
		do {
			foreach ($postEdge as $post)
				fwrite($fp, $post->asJson(JSON_UNESCAPED_UNICODE) . ',' . PHP_EOL);
		} while ($postEdge = $fb->next($postEdge));
		fseek($fp, -2, SEEK_CUR);
		fwrite($fp, ']');
		fclose($fp);
		echo '"' . $target['name'] . '" collected' . PHP_EOL;
	}
	catch (Facebook\Exceptions\FacebookResponseException $e) {
		echo 'Graph API Error: ' . $e->getMessage() . PHP_EOL;
	}
	catch (Facebook\Exceptions\FacebookSDKException $e) {
		echo 'Facebook SDK Error: ' . $e->getMessage() . PHP_EOL;
	}
}
