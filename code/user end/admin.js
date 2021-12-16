class Stack {
    constructor() {
        this.size = 10;
        this.items = [];
    }
    push(element) {
        if (this.items.length <= this.size) {
            this.items.push(element);
        } else {
            this.items.shift();
            this.items.push(element);
        }
    }
    pop(element) {
        if (this.items.length == 0) {
            return "overflow";
        } else {
            return this.items.pop();
        }
    }
    isEmpty() {
        if (this.items.length == 0) {
            return true;
        } else {
            return false;
        }
    }
}

var con,
    loadedQs = [],
    stack = new Stack(),
    startNumA = 0,
    numA = 0,
    us = "",
    ps = "",
    typeOfDisplay = "",
    letIn = !1;

var username="";
function connect() {
    ((con = new WebSocket("ws://80.5.202.49:8080")).onopen = function () {
        con.send(username+"-+-+"+"Connect");
    }),
        (con.onerror = function (e) {
            alert("Error");
        }),
        (con.onclose = function () {
            alert("Server closed, please refresh"), location.reload();
        }),
        (con.onmessage = function (e) {
            console.log("message:" + e.data);
            var t = e.data;
            if ("signInRequestGranted" == t) (letIn = !0), (document.getElementById("signIn").style.display = "none");
            else if ("ERROR" == t) alert("there was a problem doing what you just did");
            else {
                (loadedQs = t.split(":::")), (document.getElementById("View").innerHTML = '<a onClick="undo()"><p style="cursor: pointer;"><u> Undo Deletion </u></p></a>');
                for (var n, o = 0; o < loadedQs.length; o++) {
                    "" != loadedQs[0] &&
                        (console.log(typeOfDisplay),
                        (n =
                            "V" == typeOfDisplay
                                ? '<br id="' +
                                  numA +
                                  '"><button oncontextmenu="Delete(\'' +
                                  numA +
                                  "')\" onClick=\"addQ('" +
                                  numA +
                                  '\')" id="' +
                                  numA +
                                  '" class="userMessage">' +
                                  loadedQs[o] +
                                  '</button><div id="' +
                                  numA +
                                  '" class="msgBrk"></div>'
                                : "R" == typeOfDisplay
                                ? '<br id="' +
                                  numA +
                                  '"><button oncontextmenu="DeleteR(\'' +
                                  numA +
                                  "')\" onClick=\"addR('" +
                                  numA +
                                  '\')" id="' +
                                  numA +
                                  '" class="userMessage">' +
                                  loadedQs[o] +
                                  '</button><div id="' +
                                  numA +
                                  '" class="msgBrk"></div>'
                                : '<br id="' + numA + '"><button oncontextmenu="DeleteF(\'' + numA + '\')" id="' + numA + '" class="userMessage">' + loadedQs[o] + '</button><div id="' + numA + '" class="msgBrk"></div>'),
                        (numA += 1),
                        (document.getElementById("View").innerHTML += n + "<br><br><br>"));
                }
                removeTopA();
            }
        });
}
function viewReport() {
    (stack = new Stack()),
        1 == letIn
            ? ((typeOfDisplay = "R"),
              (document.getElementById("View").innerHTML = ""),
              (document.getElementById("View").style.display = "block"),
              (document.getElementById("alertAdd").style.display = "none"),
              (document.getElementById("alertDelete").style.display = "none"),
              con.send(username+"-+-+"+"REPORT"))
            : alert("Sign in to do this");
}
function viewAll() {

    (stack = new Stack()),
        console.log("view"),
        1 == letIn
            ? ((numA = startNumA = 0),
              (typeOfDisplay = "V"),
              (document.getElementById("View").innerHTML = ""),
              (document.getElementById("View").style.display = "block"),
              (document.getElementById("alertAdd").style.display = "none"),
              (document.getElementById("alertDelete").style.display = "none"),
              con.send(username+"-+-+"+"VIEWDATA"))
            : alert("Sign in to do this");
}
function signIn() {
    var e = document.getElementById("uname").value,
        t = document.getElementById("paswo").value;
    if(e.includes("-+-+") || t.includes("-+-+") || e.includes("--") || t.includes("--")) //invalid characters
    {
      alert("Use of invalid characters in either your username or password");
    }else{
      username=e;
      con.send(username+"-+-+"+"signInRequest:" + e + "--" + t), (us = e), (ps = t);
    }
}

function addQ(e) {
    var t, n;
    console.log("add");
     if(letIn) {
            document.getElementById(e).remove();
            t = document.getElementById(e).textContent;
			document.getElementById('showQ').innerHTML=t;
			document.getElementById('idHold').innerHTML=e;
			modal.style.display = "block";
            console.log(t);
			/*
			n = prompt("Please enter Your response", "").replace("---", "").replace(":::", "").replace("signInRequest:", "").replace("DELETE", "delete");
            if(n.length < 500){
                  if(null == n || "" == n)
				  { alert("cancelled");
				  }else{
					con.send("ADD" + t + "---" + n);
					document.getElementById(e).remove();
					document.getElementById(e).remove();}
             }else{ alert("Please decrease your message size");}
			 */
	}else{alert("Sign in to do this");}

}
function submitVals() {
	if(letIn){
		var date = document.getElementById('deleteBy').value;
		var e=document.getElementById('idHold').innerHTML;
		var q=document.getElementById('showQ').innerHTML;
		var a=document.getElementById('Information').value;
		console.log(e);
		if(a.length < 400){
                  if(null == a || "" == a)
				  { alert("cancelled");

				  }else{
						con.send(username+"-+-+"+"ADD" + q + "---" + a +"---"+date);
						document.getElementById(e).remove();
						document.getElementById('Information').value="";
						document.getElementById('deleteBy').value="none";
						modal.style.display = "none";

					}

        }else{ alert("Please decrease your message size");}



	}
}
function addR(e) {
    var t, n;
    letIn
        ? (document.getElementById(e).remove(),
          (t = document.getElementById(e).textContent),
          console.log(t),
          (n = (n = (n = (n = (n = prompt("Please enter Your response", "")).replace("---", "")).replace(":::", "")).replace("signInRequest:", "")).replace("DELETE", "delete")).length < 500
              ? null == n || "" == n
                  ? alert("cancelled")
                  : (con.send(username+"-+-+"+"RADD" + t + "---" + n), document.getElementById(e).remove(), document.getElementById(e).remove())
              : alert("Please decrease your message size"))
        : alert("Sign in to do this");
}
function Delete(e) {
    var t;
    console.log("delete"),
        letIn
            ? (document.getElementById(e).remove(), (t = document.getElementById(e).textContent), con.send(username+"-+-+"+"DELETE" + t), document.getElementById(e).remove(), document.getElementById(e).remove(), stack.push(t))
            : alert("Sign in to do this");
}
function undo() {
    var e;
    stack.isEmpty() || ((e = stack.pop()), "V" == typeOfDisplay ? (con.send(username+"-+-+"+"QADD" + e), viewAll()) : (con.send(username+"-+-+"+"FADD" + e), viewFeedback()));
}
function DeleteR(e) {
    var t;
    console.log("delete reported"),
        letIn ? (document.getElementById(e).remove(), (t = document.getElementById(e).textContent), con.send(username+"-+-+"+"DELETER" + t), document.getElementById(e).remove(), document.getElementById(e).remove()) : alert("Sign in to do this");
}


function addOwn() {
    letIn ? ((document.getElementById("alertAdd").style.display = "block"), (document.getElementById("View").style.display = "none"), (document.getElementById("alertDelete").style.display = "none")) : alert("Sign in to do this");
}
function deleteOwn() {
    letIn ? ((document.getElementById("alertAdd").style.display = "none"), (document.getElementById("View").style.display = "none"), (document.getElementById("alertDelete").style.display = "block")) : alert("Sign in to do this");
}
function saveQuestionAnswer() {
    var e, t;
    letIn
        ? ((t = document.getElementById("inputQ1").value),
          (e = document.getElementById("inputQ2").value),
          (t = (t = (t = (t = (t = (t = (t = t.replace("---", "")).replace(":", "")).toLowerCase()).replace("?", "")).replace(".", "")).replace(",", "")).replace("DELETE", "delete")),
          (e = (e = (e = e.replace("---", "")).replace(":::", "")).replace("DELETE", "delete")).length + t.length < 530
              ? "" != t && "" != e
                  ? (con.send(username+"-+-+"+"ADD" + t + "---" + e+"---"), 
                  (document.getElementById("inputQ1").value = ""),
                  (document.getElementById("inputQ2").value = ""))
                  : alert("You cannot add that")
              : alert("Please decrease your message size"))
        : alert("Sign in to do this");
}
function delQuestionAnswer() {
    var e;
    letIn
        ? (e = (e = (e = (e = (e = document.getElementById("inputD1").value).replace("---", "")).replace(":::", "")).replace("DELETE", "delete")).toLowerCase()).length < 500
            ? "" != e
                ? (con.send(username+"-+-+"+"DELQUE" + e), (document.getElementById("inputD1").value = ""))
                : alert("You cannot delete that")
            : alert("Please decrease your message size")
        : alert("Sign in to do this");
}
function removeTopA() {
    10 < numA + startNumA &&
        (document.getElementById(startNumA.toString()).remove(),
        document.getElementById((startNumA + 1).toString()).remove(),
        document.getElementById(startNumA.toString()).remove(),
        document.getElementById((startNumA + 1).toString()).remove(),
        document.getElementById(startNumA.toString()).remove(),
        document.getElementById((startNumA + 1).toString()).remove(),
        (startNumA += 2));
}

connect();
