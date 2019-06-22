function loadQR() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("qrcode").innerHTML =
      "<img class=\"img-responsive\" src=\"data:image/png;base64," + this.responseText + "\">"
    }
    else {
      document.getElementById("qrcode").innerHTML = this.responseText;
    }
  }
  xhttp.open("GET", "/generate", true)
  xhttp.send();
}
