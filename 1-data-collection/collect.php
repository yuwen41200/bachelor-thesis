<?php

require_once __DIR__ . '/vendor/autoload.php';
require_once 'safe_facebook.php';

$fp = fopen('dat/target_list_serialized_final.dat', 'r');
$unserialized = fread($fp, filesize('dat/target_list_serialized_final.dat'));
fclose($fp);
$targetList = unserialize($unserialized);

// we are just doing a prototype now
array_splice($targetList, 1);

// destroy these before making the source code public
/* @noinspection SpellCheckingInspection */
$secretKey = '3a9c3467214697db53d6ff29a96f52d7';
/* @noinspection SpellCheckingInspection */
$accessToken = 'EAARZCIAZCAqZA4BABDTI5qilZCP1oYdgH7bagRBLnD7ImeQVPnNUT1FgfCYwZC1dsjb8zbxZCM'.
               'dAInCImRvjtg0wKnkOEQHkD6wHHwGgaCFDfZBlSGvU0FZBuZCan0QtYbFmwZBCIZA1Qs5R8GJEy'.
               'PE7LrvTB7Jcykkl5ZAwHdYJS72jQs90kpo9RfED09c9QfgHLuXXaZAaVPZByI9gZDZD';

$fb = new SafeFacebook\SafeFacebook([
	'app_id' => '1265675586808222',
	'app_secret' => $secretKey,
	'default_graph_version' => 'v2.7',
]);
$fb->setDefaultAccessToken($accessToken);

foreach ($targetList as $target) {
	try {
		$fp = fopen('json/archive_' . $target['id'] . '.json', 'w');
		fwrite($fp, '[');
		$str = '/' . $target['id'] . '/posts?'.
		       'fields=message,story,link,created_time,id&'.
		       'limit=100&since=2015-10-17&until=2016-01-17';
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
