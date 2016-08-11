<?php

echo '{"current":"';
echo date('YmdH');
echo '","all":[';

$first = true;

$todayDay = date('Ymd');

for ($i = 0; $i < 24; $i++) {
	if ($first == true) {
		$first = false;
	} else {
		echo ",";
	}
	echo '"' . $todayDay;
	if ($i < 10) {
		echo '0';
	}
	echo $i;
	echo '"';
}

$tomorrowDay = date("Ymd", time()+86400);

for ($i = 0; $i < 24; $i++) {
	echo ',"' . $tomorrowDay;
	if ($i < 10) {
		echo '0';
	}
	echo $i;
	echo '"';
}
echo ']}';
?>
