var con = new WebSocket("ws://80.5.202.49:50007");
var lastMessage = "";
var lastAnswer = "";
var subs = "";
var username=""; //username
function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';');
  for(let i = 0; i <ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

con.onopen = function() {
  username=getCookie("username");
	console.log("username",username);
	con.send(username+"-+-+"+"hi" + "---" + "");
	window.scrollTo(0, document.body.scrollHeight);
};
con.onerror = function(error) {
	console.log("error" + error)
};
con.onmessage = function(e) {
	console.log("message:" + e.data);
	var vals = e.data.split("---");
	var output = vals[0];
	subs = vals[1];
	var string = "";
	output = output.replace(/([\[(])(.+?)([\])])/g, "");
	var add2;
	output = output.split("$");
	if(num > 0) {
		var tempID = document.getElementById(num - 1).innerHTML;
		tempID = tempID.replace("?", ".");
		tempID = tempID.replace("!", ".");
		tempID = tempID.replace(/'/g, '\'');
		tempID = tempID.split(".")
	}
	for(i = 0; i < output.length; i++) {
		if(output[i] != "") {
			add2 = '<br id="' + num + "bR" + '"><div id="' + num + '" class="shepMessage">' + output[i] + '</div><div id="' + num + '" class="msgBrk"></div>';
			if(output[i].includes("This is something similar I found which may answer your question")) {
				var temp = output[i].replace("This is something similar I found which may answer your question ", "");
				temp = temp.replace(/'/g, "");
				add2 = '<br id="' + num + "bR" + '"><div id="' + num + '" class="shepMessage">' + output[i] + '<a onClick="feedback(' + "'" + tempID[i] + "'" + ',' + "'" + temp + "'" + ')"><p style="cursor: pointer;"><u> Did this answer your question? </u></p></a>' + '</div><div id="' + num + '" class="msgBrk"></div>'
			}
			num = num + 1;
			document.getElementById("mainContent").innerHTML += add2;
		}
	}
  window.scrollTo(0,document.body.scrollHeight);
};
var startNum = 0;
var num = 0;
var modal = document.getElementById("myModal");
function enterMessage() {
	console.log("test");
	var text = document.getElementById("messageFAQ").value;
	var add = '<br id="' + num + "bR" + '"><div id="' + num + '" class="userMessage">' + text + '</div><div id="' + num + '" class="msgBrk"></div>';
	num = num + 1;
	text = text.toLowerCase();
	text = text.replace("---", "");
	text = text.replace("FEEDBACKN", "");
	text = text.replace("FEEDBACKP", "");
	text = text.replace(":::", "");
	text = text.replace("[", "(");
	text = text.replace("]", ")");
	text = text.replace("-+-+", "");
	if(text.length < 500) {
		con.send(username+"-+-+"+text + "---" + subs);
		lastMessage = text;
		document.getElementById("mainContent").innerHTML += add;
		document.getElementById("messageFAQ").value = "";
		removeTop()
	} else {
		alert("Please decrease the size of your message")
	}
}

function removeTop() {
	if(num + startNum > 10) {
		document.getElementById(startNum.toString() + "bR").remove();
		document.getElementById((startNum + 1).toString() + "bR").remove();
		document.getElementById(startNum.toString()).remove();
		document.getElementById((startNum + 1).toString()).remove();
		document.getElementById(startNum.toString()).remove();
		document.getElementById((startNum + 1).toString()).remove();
		startNum += 2
	}
}

function report() {
	var text = prompt("Please enter the question you would like fixed:", "");
	text = text.replace("---", "");
	text = text.replace("FEEDBACKN", "");
	text = text.replace("FEEDBACKP", "");
	text = text.replace(":::", "");
	text = text.replace("-+-+", "");
	text = text.toLowerCase();
	if(text.length < 500) {
		if(text != null && text != "") {
			con.send(username+"-+-+"+"REPORT" + text)
		} else {
			alert("Invalid input")
		}
	}
}

function feedback(id, answer) {
	modal.style.display = "block";
	lastMessage = id;
	lastAnswer = answer
}

function posFeedback() {
	modal.style.display = "none";
	con.send(username+"-+-+"+"FEEDBACKP" + lastMessage + "---" + lastAnswer)
}

function negFeedback() {
	console.log("negative");
	con.send(username+"-+-+"+"FEEDBACKN" + lastMessage);
	modal.style.display = "none"
}

function toPython(usrdata) {
	console.log("uploading" + usrdata);
	$.ajax({
		url: "http://80.5.202.205:50007",
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
document.getElementById("messageFAQ").addEventListener("keyup", function(event) {
	if(event.keyCode === 13) {
		enterMessage();
    window.scrollTo(0,document.body.scrollHeight);
	}
});
