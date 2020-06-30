class Stack {
		constructor()
		{
			this.size=10;
			this.items=[];
		}
		push(element)
		{
			if(this.items.length<=this.size){
				this.items.push(element);
			}else{
				this.items.shift();
				this.items.push(element);
			}
		}
		pop(element)
		{
			if(this.items.length==0){
				return "overflow";
			}else{
				return this.items.pop();
			}
		}
		isEmpty()
		{
			if(this.items.length==0){return true;}else{return false;}
		}
	}
var con=new WebSocket("ws://80.5.202.205:50007"),lastMessage="",lastAnswer="",subs="";con.onopen=function(){con.send("hi---")},con.onerror=function(e){console.log("error"+e)},con.onmessage=function(e){console.log("message:"+e.data);var n=e.data.split("---"),t=n[0];subs=n[1];var s,o,a;for(t=(t=t.replace(/([\[(])(.+?)([\])])/g,"")).split("$"),0<num&&(s=(s=(s=(s=(s=document.getElementById(num-1).innerHTML).replace("?",".")).replace("!",".")).replace(/'/g,"'")).split(".")),i=0;i<t.length;i++){""!=t[i]&&(a='<br id="'+num+'bR"><div id="'+num+'" class="shepMessage">'+t[i]+'</div><div id="'+num+'" class="msgBrk"></div>',t[i].includes("This is something similar I found which may answer your question")&&(o=(o=t[i].replace("This is something similar I found which may answer your question ","")).replace(/'/g,""),a='<br id="'+num+'bR"><div id="'+num+'" class="shepMessage">'+t[i]+"<a onClick=\"feedback('"+s[i]+"','"+o+'\')"><p style="cursor: pointer;"><u> Did this answer your question? </u></p></a></div><div id="'+num+'" class="msgBrk"></div>'),num+=1,document.getElementById("mainContent").innerHTML+=a,document.getElementById("mainContent").scrollIntoView())}};var startNum=0,num=0;function enterMessage(){console.log("test");var e=document.getElementById("messageFAQ").value,n='<br id="'+num+'bR"><div id="'+num+'" class="userMessage">'+e+'</div><div id="'+num+'" class="msgBrk"></div>';num+=1,(e=(e=(e=(e=(e=(e=(e=e.toLowerCase()).replace("---","")).replace("FEEDBACKN","")).replace("FEEDBACKP","")).replace(":::","")).replace("[","(")).replace("]",")")).length<500?(con.send(e+"---"+subs),lastMessage=e,document.getElementById("mainContent").innerHTML+=n,document.getElementById("messageFAQ").value="",removeTop()):alert("Please decrease the size of your message")}function removeTop(){10<num+startNum&&(document.getElementById(startNum.toString()+"bR").remove(),document.getElementById((startNum+1).toString()+"bR").remove(),document.getElementById(startNum.toString()).remove(),document.getElementById((startNum+1).toString()).remove(),document.getElementById(startNum.toString()).remove(),document.getElementById((startNum+1).toString()).remove(),startNum+=2)}function report(){var e=prompt("Please enter the question you would like fixed:","");(e=(e=(e=(e=(e=e.replace("---","")).replace("FEEDBACKN","")).replace("FEEDBACKP","")).replace(":::","")).toLowerCase()).length<500&&(null!=e&&""!=e?con.send("REPORT"+e):alert("Invalid input"))}function feedback(e,n){modal.style.display="block",lastMessage=e,lastAnswer=n}function posFeedback(){modal.style.display="none",con.send("FEEDBACKP"+lastMessage+"---"+lastAnswer)}function negFeedback(){console.log("negative"),con.send("FEEDBACKN"+lastMessage),modal.style.display="none"}function toPython(e){console.log("uploading"+e),$.ajax({url:"http://80.5.202.205:50007",type:"POST",data:{information:"From SHEP client",userdata:e},dataType:"json",success:function(e){console.log("connected"),console.log(e)}})}document.getElementById("messageFAQ").addEventListener("keyup",function(e){13===e.keyCode&&enterMessage()});