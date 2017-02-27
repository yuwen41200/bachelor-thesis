<?php

$fp = fopen('dat/target_list_serialized_final.dat', 'r');
$unserialized = fread($fp, filesize('dat/target_list_serialized_final.dat'));
fclose($fp);
$targetList = unserialize($unserialized);

$convertedList = array();
foreach ($targetList as $item)
	$convertedList[$item['id']] = $item['name'];

$encoded = json_encode($convertedList, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT);
$fp = fopen('dat/uid_to_name_map.dat', 'w');
fwrite($fp, $encoded);
fclose($fp);
