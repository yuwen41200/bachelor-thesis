<?php

namespace SafeFacebook;

use Facebook\Facebook;

class SafeFacebook extends Facebook {

	private $call_count = 0;

	public function get($endpoint, $accessToken = null, $eTag = null, $graphVersion = null) {
		sleep((int) ($this->call_count * 0.04));
		$this->call_count++;
		return parent::get($endpoint, $accessToken, $eTag, $graphVersion);
	}

	public function getCallCount() {
		return $this->call_count;
	}

}
