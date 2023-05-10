<?php
$command = $_GET['direction'];
switch ($command) {
    case "avant":
        exec("python3 class_moteur_robot.py avant");
        break;
    case "arriere":
        exec("python3 class_moteur_robot.py arriere");
        break;
    case "gauche":
        exec("python3 class_moteur_robot.py gauche");            
        break;
    case "droite":
        exec("python3 class_moteur_robot.py droite");            
        break;
    case "reco_facial7":
        exec("python3 reco_facial7.py");
        break;
    case "haut_cam":
        exec("python3 class_moteur_robot.py haut_cam");
        break;
    case "bas_cam":
        exec("python3 class_moteur_robot.py bas_cam");
        break;
    case "gauche_cam":
        exec("python3 class_moteur_robot.py gauche_cam");
        break;
    case "droite_cam":
        exec("python3 class_moteur_robot.py droite_cam");
        break;
    case "cam_initial":
        exec("python3 class_moteur_robot.py cam_initial");
        break;
    }

?>
