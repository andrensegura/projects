<?php
    require ('steamauth/steamauth.php');  
    include 'html/header.html';
    echo "<hr><a href=\"/\">Home</a><hr>";
    
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

    echo "Login to Steam to auto-add tradeable games to your collection:";
    echo steamlogin(); //login button
    echo "<i><a href=\"http://store.steampowered.com/\">Proudly powered by Steam!</a></i>";
    
}  else {
    include ('steamauth/userInfo.php');

    //Protected content
    echo "<form method=\"post\" action=\"login?action=update\">"; 
    echo "<input type=\"hidden\" name=\"up_steam\" value=\"".$steamprofile['steamid']."\">";
    echo "Successfully logged into Steam! Please click below to update your list.<br>";
    echo "Enter current password: <input type=\"password\" name=\"password\"><br>";
    echo "<input type=\"submit\" value=\"Update\">";
    echo "</form>";
 
    logoutbutton();
    echo "<i><a href=\"http://store.steampowered.com/\">Proudly powered by Steam!</a></i>";
}    
?>  
</body>
</html>
