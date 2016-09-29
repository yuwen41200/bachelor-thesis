<?php

$fp = fopen('target_list_serialized.dat', 'r');
$unserialized = fread($fp, filesize('target_list_serialized.dat'));
fclose($fp);
$targetList = unserialize($unserialized);

$fp = fopen('target_list_serialized_ng.dat', 'r');
$unserialized = fread($fp, filesize('target_list_serialized_ng.dat'));
fclose($fp);
$targetListNg = unserialize($unserialized);

foreach ($targetListNg as $key => $value)
	$targetListNg[$key] = $value['name'];

// manually verify the target list
$diffList = array_diff($targetList, $targetListNg);
print_r($diffList);
$diffList = array_diff($targetListNg, $targetList);
print_r($diffList);
echo sizeof($targetList) . ', ' . sizeof($targetListNg) . PHP_EOL;

// manually correct the target list
$targetListNg = unserialize($unserialized);
unset($targetListNg[145]);
unset($targetListNg[141]);
unset($targetListNg[127]);
unset($targetListNg[104]);
$targetListNg[] = [
	'name' => '宋楚瑜',
	'fan_count' => 577128,
	'id' => 'love4tw'
];
$targetListNg[] = [
	'name' => '民間司法改革基金會',
	'fan_count' => 28473,
	'id' => 'jrf.tw'
];

usort($targetListNg, 'compareTarget');
array_splice($targetListNg, 135);
print_r($targetListNg);

$serialized = serialize($targetListNg);
$fp = fopen('target_list_serialized_final.dat', 'w');
fwrite($fp, $serialized);
fclose($fp);

function compareTarget($a, $b) {
	return $b['fan_count'] - $a['fan_count'];
}
