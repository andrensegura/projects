<script>
function show_content(el_id) {
    if (el_id == "first") {
        document.getElementById("sel1").style.backgroundColor = "silver";

        document.getElementById("second").className = "tab-content-hidden";
        document.getElementById("sel2").style.backgroundColor = "transparent";
        document.getElementById("third").className = "tab-content-hidden";
        document.getElementById("sel3").style.backgroundColor = "transparent";
    } else if (el_id == "second") {
        document.getElementById("sel2").style.backgroundColor = "silver";

        document.getElementById("first").className = "tab-content-hidden";
        document.getElementById("sel1").style.backgroundColor = "transparent";
        document.getElementById("third").className = "tab-content-hidden";
        document.getElementById("sel3").style.backgroundColor = "transparent";
    } else if (el_id == "third") {
        document.getElementById("sel3").style.backgroundColor = "silver";

        document.getElementById("second").className = "tab-content-hidden";
        document.getElementById("sel2").style.backgroundColor = "transparent";
        document.getElementById("first").className = "tab-content-hidden";
        document.getElementById("sel1").style.backgroundColor = "transparent";
    }
    element = document.getElementById(el_id);
    element.className = "tab-content";
}
</script>
