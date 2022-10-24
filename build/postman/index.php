<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Raleway:wght@300&display=swap" rel="stylesheet">
    <title>Postman</title>
    <style>
        .center {
            margin: 0;
            position: absolute;
            text-align: center;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-family: 'Raleway', sans-serif;
        }

    </style>
</head>
<body>
    <div class="center">
    <img src="https://i.imgur.com/TJMQvDl.png" width=500px>
    <br>
    <?php
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        echo "ACSI{n1c3_y0u_1342n7_480u7_h77p_23qu3575}";
    }
    if ($_SERVER['REQUEST_METHOD'] === 'GET') {
        echo "<br><h1>bruh maybe you want to help this poor postman?</h1>";
    }  
    ?>
    </div>
</body>
</html>
