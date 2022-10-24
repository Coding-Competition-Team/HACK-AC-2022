
<?php
    ini_set('display_errors', FALSE);
    include 'lib.php';
    $password = "RSnake33ncxYMsiIgw";
    if ($_GET["pass"] == $password){
        echo "Sorry, that's the right password. But you'll have to find a way to bypass this check.";
    }
    elseif (hash("sha1", $password) == hash("sha1", $_GET["pass"])){
        echo $flag;
    }
    else {
        echo "You got this! This should be a fun and easy web challenge!";
    }
    show_source(__FILE__);
?>
