$.get( "http://localhost:8080/api/getDashboard", function( data ) {
    console.log( typeof data ); // string
    console.log( data ); // HTML content of the jQuery.ajax page
    document.getElementById("lastVictims").innerHTML = data["lastVics"];
    document.getElementById("latency").innerHTML = data["avgLatency"];
    document.getElementById("tasks").innerHTML = data["taskNbr"];
    document.getElementById("intServ").innerHTML = data["intServ"];

  });