<?php
$mysqli = new mysqli("", "", "", "");

if ($mysqli->connect_error) {
    die("Falha na conexão: " . $mysqli->connect_error);
}

echo "Conectado com sucesso!";
?>
