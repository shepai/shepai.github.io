var con = new WebSocket("ws://80.5.202.49:4040");

con.onopen = function() {
	con.send("LIST"); //on boot request list
	window.scrollTo(0, document.body.scrollHeight);
};
con.onerror = function(error) {
	console.log("error" + error)
};
list=[];
con.onmessage = function(e) {
	console.log("message:" + e.data);
	var s=e.data.replace(">>>","");
	var vals = s.split(":::");
	vals.pop(vals.length);
	console.log(vals);
  if(vals[0]=="")
	{
		vals[0]="Default";
	}
  list=vals //split down items

	console.log(list);
  populate(list); //populate screen
};


function populate(Array) //popluate the screen with the html format
{
	var a = "<option value='";
  var b = "'>";
	var c = "</option>";
	var string="";
	for (var i=0;i<Array.length;i++)
	{
		string+=a+Array[i]+b+Array[i]+c; //show in correct format
	}
	document.getElementById("mySelect").innerHTML=string;

}
function toPython(usrdata) {
	console.log("uploading" + usrdata);
	$.ajax({
		url: "http://80.5.202.205:4040",
		type: "POST",
		data: {
			information: "From SHEP client",
			userdata: usrdata
		},
		dataType: "json",
		success: function(data) {
			console.log("connected");
			console.log(data);
		}
	})
}
