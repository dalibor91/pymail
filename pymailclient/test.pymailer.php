<?php 

require('PyMailer.php');


$pm = new PyMailer('test@gmail.com');

$ok = $pm->setSubject("Test From PHP")
->setBody("Some text ")
->addTo('test1@gmail.com')
->attach('/tmp/file1')
->attach('/tmp/file2')
->send('localhost', '8888', 'login:pass')
;
