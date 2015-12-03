<?php
    require ('steamauth/steamauth.php');  
    
	# You would uncomment the line beneath to make it refresh the data every time the page is loaded
	// $_SESSION['steam_uptodate'] = false;
?>
<html>
<head>
    <title>Key Cellar</title>
</head>
<body>
<?php
if(!isset($_SESSION['steamid'])) {

    echo "welcome guest! please login \n \n";
    echo steamlogin(); //login button
    
}  else {
    include ('steamauth/userInfo.php');

    //Protected content
    echo "<form method=\"post\" action=\"login?action=update\">"; 
    echo "<input type=\"hidden\" name=\"up_steam\" value=\"".$steamprofile['steamid']."\">";
    echo "Successfully logged in! Please click below to update your list.<br>";
    echo "Enter current password: <input type=\"password\" name=\"password\"><br>";
    echo "<input type=\"submit\" value=\"Update\">";
    echo "</form>";
 
    logoutbutton();
}    
?>  
</body>
</html>
