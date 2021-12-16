var con = new WebSocket("ws://80.5.202.49:4040");

con.onopen = function() {
	window.scrollTo(0, document.body.scrollHeight);
};
con.onerror = function(error) {
	console.log("error" + error)
};



con.onmessage = function(e) {
	console.log("message:" + e.data);
  alert(e.data);
	if(e.data=="Success")
  {

  }
};

function submit()
{
  var name = document.getElementById("name").value;
  var pass = document.getElementById("pass").value;

  if(name!="" && pass!="" && name==name.replace(":::","") && pass==pass.replace(":::","")){
    con.send("ADD"+name+":::"+pass);
  }else{
    alert("Invalid name or password. Make sure you haven't left anything blank and does not contain banned characters")
  }

}
