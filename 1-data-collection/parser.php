<?php

$targetList = array();

$fp = fopen('facebook_pages_stats_socialbakers_total_taiwan_society_politics.txt', 'r');
while (fgets($fp)) {
	$targetList[] = trim(fgets($fp));
	fgets($fp);
}
fclose($fp);

$fp = fopen('facebook_pages_stats_socialbakers_total_taiwan_community_political.txt', 'r');
while (fgets($fp)) {
	$targetList[] = trim(fgets($fp));
	fgets($fp);
}
fclose($fp);

$fp = fopen('facebook_pages_stats_socialbakers_local_taiwan_society_politics.txt', 'r');
while (fgets($fp)) {
	$targetList[] = trim(fgets($fp));
	fgets($fp);
	fgets($fp);
}
fclose($fp);

$fp = fopen('facebook_pages_stats_socialbakers_local_taiwan_community_political.txt', 'r');
while (fgets($fp)) {
	$targetList[] = trim(fgets($fp));
	fgets($fp);
	fgets($fp);
}
fclose($fp);

$fp = fopen('facebook_pages_stats_likeboy_combined.txt', 'r');
while ($line = fgets($fp)) {
	$targetList[] = trim($line);
	fgets($fp);
	fgets($fp);
	fgets($fp);
}
fclose($fp);

$fp = fopen('facebook_pages_stats_custom.txt', 'r');
while ($line = fgets($fp)) {
	$targetList[] = trim($line);
	fgets($fp);
}
fclose($fp);

$uniqueTargetList = array_unique($targetList);
print_r($uniqueTargetList);

$serialized = serialize($uniqueTargetList);
$fp = fopen('target_list_serialized.dat', 'w');
fwrite($fp, $serialized);
fclose($fp);
