var found=false;
	
function search()
{
		//search bar
		if(found){
			document.getElementById("searchbar").style.visibility = "hidden";
			document.getElementById("searchbar").style.display="none";
			console.log(document.getElementById("searchbar").value);
			var url="https://www.google.com/search?q=shep+ai+%22"+document.getElementById("searchbar").value+"%22";
			window.open(url);
			found=false;
		}else {
			document.getElementById("searchbar").style.visibility = "visible";
			document.getElementById("searchbar").style.display="inline";
			found=true;
		}
}
//utility code
var cookiePermission=false;
var lines= 6;var characterlength=90;
function detectmob() { 
			 if( navigator.userAgent.match(/Android/i)
			 || navigator.userAgent.match(/webOS/i)
			 || navigator.userAgent.match(/iPhone/i)
			 || navigator.userAgent.match(/iPad/i)
			 || navigator.userAgent.match(/iPod/i)
			 || navigator.userAgent.match(/BlackBerry/i)
			 || navigator.userAgent.match(/Windows Phone/i)
			 ){
				return true;
			  }
			 else {
				return false;
			  }
			}
			function cookieprompt(){ //get permission from the user
				
				if (window.confirm('SHEP uses cookies to store data, native to your device. By clicking okay, you agree for the AI to store data. Cancel to read out cookie policy')) 
				{
				cookiePermission=true;
				}else{
					window.location.href='cookie.html';
				};
				if(detectmob()){
					//mobile phone screen
					console.log("mobile");
					lines=3;characterlength=20;
					
				}
			}
			function download(filename, text) { //download a file 
			  var element = document.createElement('a');
			  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
			  element.setAttribute('download', filename);
				
			  element.style.display = 'none';
			  document.body.appendChild(element);

			  element.click();

			  document.body.removeChild(element);
			 
			}
			function upload()
			{ //upload an existing file from the PC to the browser
				console.log("upload file");
				var input = document.createElement('input');
				input.type = 'file';

				input.onchange = e => { 

				   // getting a hold of the file reference
				   var file = e.target.files[0]; 
					console.log(file.name);
					if(includes(file.name,".asp")){//check it is the correct file type
				   // setting up the reader
				   var reader = new FileReader();
				   reader.readAsText(file,'UTF-8');

				   // here we tell the reader what to do when it's done reading...
				   reader.onload = readerEvent => {
					  var content = readerEvent.target.result; // this is the content!
					  console.log("content:" + content );
					   textFile=content;
					   document.getElementById("errormessages").innerHTML="";
				   }
					}else{
						document.getElementById("errormessages").innerHTML="Incorrect file type";
					}
				}

				input.click();
			}
			function downloadFile(){ //download the file
				download("data.txt",textFile);
			}
			function A(){
				document.getElementById("AIinput").className = "codeinput";
				document.getElementById("consoleC").className = "AIbox";
				loadDoc("test.asp"); //load the file needed
				document.getElementById("AIoutput").innerHTML = ">";
				document.getElementById("explain").innerHTML = "This is the basic version of the AI. It checks your words matches what it knows in the data. Click button 2 to see the next stage, and have a go by typing where it says: >>>";
				document.getElementById("explaintitle").innerHTML ="Version 0.0.1 mock up";
				type=0;
				learn = false; //will the system learn
			}
			function B(){
				document.getElementById("AIinput").className = "codeinput2";
				document.getElementById("consoleC").className = "AIbox2";
				document.getElementById("AIoutput").innerHTML = ">Type a sentence/question";
				document.getElementById("explain").innerHTML = "This references your words with the database, analyzes frequency and word distribution to work yout what ou are saying.";
				loadDoc("tree.xml"); //load the file needed
				document.getElementById("explaintitle").innerHTML ="Version 0.0.7 theory mock up";
				learn = false; //will the sysrem learn
				type=1;
			}
			function C(){
				document.getElementById("AIinput").className = "codeinput1";
				document.getElementById("consoleC").className = "AIbox1";
				document.getElementById("AIoutput").innerHTML = ">'a' to add items, 'q' to quit adding, and type items to search up relation";
				document.getElementById("explain").value = "This allows you to type in items which could be inputted into a system through its many sensors. The items can be entered in multiple times with different other items. This helps sort what is linked and what is not. The system will learn this and output what are the most linked items when you type in an item name.";
				document.getElementById("explaintitle").innerHTML ="CLIVE basic principle";
				loadDoc("link.txt"); //load the file needed
				learn = false; //will the sysrem learn
				type=2;
			}
			function D(){
				document.getElementById("AIinput").className = "codeinput3";
				document.getElementById("consoleC").className = "AIbox3";
				document.getElementById("AIoutput").innerHTML = ">Still in development";
				document.getElementById("explain").value = "";
				document.getElementById("explaintitle").innerHTML ="";
				learn = false; //will the sysrem learn
				type=3;
			}
			function E(){
				document.getElementById("AIinput").className = "codeinput4";
				document.getElementById("consoleC").className = "AIbox4";
				document.getElementById("AIoutput").innerHTML = ">Still in development";
				document.getElementById("explain").value = "";
				document.getElementById("explaintitle").innerHTML ="";
				learn = false; //will the sysrem learn
				type=4;
			}
			function F(){
				document.getElementById("AIinput").className = "codeinput5";
				document.getElementById("consoleC").className = "AIbox5";
				document.getElementById("AIoutput").innerHTML = ">Still in development";
				document.getElementById("explain").value = "";
				document.getElementById("explaintitle").innerHTML ="";
				learn = false; //will the sysrem learn
				type=5;
			}
//the main code for the AI
				var type=1; //set the type of code to run
			var previous="";
			var addmode=false;
			//document.cookie ="";
			var learn = false; //will the sysrem learn
			var inputArray=[];
			function sort()
			{
				//sort the memory content into an array
				var phrases= textFile.split('#');
				console.log(phrases.length);
				var array=[];
				var numbers=0;
				for(var i=0;i<phrases.length;i++){
					//sort each words and where they link to.
				     var splitted = ((phrases[i].replace("↵", "").split(',')[0]).split(':')); //get splitted words
					 
					 numbers = (splitted.length);  //get the size of it
					 console.log(numbers+":::"+splitted); //alert user the size
					 
					 array.push(splitted); //add array to array
					 
				}
				console.log(array);
				return array;
				
			}
			function sortdata(phrase){
			//remove out detail	
			var array=textFile.split("<"+phrase+">");
			var sorted=[];
			for(var i=0;i<array.length;i++){
				//remove all uneeded detail
				var string="";
				for(var j=0;j<array[i].length;j++){
					//go through each position
					if(array[i][j]=='<'){ //the word is finished is present 
						//finished
						break;
					}else{
						string+=array[i][j]; //add it to
					}
				}
				sorted.push(string); //add to string
			}
			return sorted;
		}
			function reply(ID)
			{
				//find the correct reply for the given input
				var phrases= textFile.split('#');
				console.log(phrases.length);
				var string = phrases[ID]; //get in string form
				console.log("id to get:",ID," Which is:",phrases[ID]);
				var start = false;var output="";
				for(var i=0;i<string.length;i++){
					//sort ouot what is wanted
					if(start==true)
					{
						output+=string[i]; //gather the spoken bit
					}
					if(string[i]==","){
						start=true; //find change over
					}
				}
				return output.replace(/:/gi," ");//put in spaces
				

				
			}
			function writeTo(words, answers)
			{
				//write the textFile in the format
				document.cookie = "content="+textFile + words.replace(/ /gi,":") + "," + answers.replace(/ /gi,":") + "#"+"; expires=Thu, 01 Jan 2037 00:00:01 GMT";
				textFile = textFile + words.replace(/ /gi,":") + "," + answers.replace(/ /gi,":") + "#";
				console.log(textFile);
			}
			
			function includes(string,substring){
				//returns if a substring is within a substring
				var x=0;
				var i=0;
				var j=0;
				var state=false;
				//console.log(string.length);
				for (i=0;i<string.length;i++){
					
					for(j=0;j<substring.length;j++){
						//console.log(string[x+1]);
						if (j < string.length){
							//console.log(string[x+1]);
							//console.log(string[j]);
							if (string[x+i] == substring[j]){
								x++;
							}
						}	
					}
					if(x == substring.length){
						state=true;
						break;
					}
					x=0
				}
				return state
			}
				function isNumeric(n){ //check for numeric values
			return /^\d+$/.test(n);
		}
		function getPop(){
			//get the popular words by finding the threshold
			var list = sortdata("visited");
			var total=0;
			var n=0;
			var square=0
			for(i=0;i<list.length;i++){
				 //check each word
				if(isNumeric(list[i])){ //a number
					total+=parseInt(list[i]); //add more
					square+=Math.pow(parseInt(list[i]), 2);
					n=n+1; //add one to n
				}
			}
			var average=total/n;
			var sd =Math.sqrt((square/n)-Math.pow(average,2))
			return (average+sd);
		}
		function getWord(word){
			//get the node to, byt finding the node
			var words=sortdata("word");
			var index=-1;
			for(var i=0;i<words.length;i++){
			//new array
				if(word==words[i]){
					//words which are found
					index=i;
				}
			}
			if(index>=0){
				return sortdata("node_to")[index];
			}else{
				return false
			}
		}
		function getVisited(word){
			//get the number of visited to
			var words=sortdata("word");
			var index=-1;
			for(var i=0;i<words.length;i++){
			//new array
				if(word==words[i]){
					//words which are found
					index=i;
				}
			}
			if(index>=0){
				return sortdata("visited")[index];
			}else{
				return false
			}
		}
			function getAI(Userinput) {
				//main algorithm
				var string="";var counter=0;var found=false;var current=0;var saveID=0;
				//console.log(Userinput);
				var words=sort();
				//clear the string of needed characters
				Userinput=Userinput.replace(/,/gi,"");
				Userinput=Userinput.replace(/:/gi,"");
				Userinput=Userinput.replace(/#/gi,"");
				Userinput=Userinput.split(" ")
				console.log("length"+Userinput.length);
				for(var i=0;i<words.length;i++){
					
					for(var j=0;j<words[i].length;j++){
						//console.log(words[i][j]+","+Userinput[j]);
						if(words[i][j]==Userinput[j]){current+=1;}//count each time the word is the same
						//future versions check here for words in slightly different orders
					}
					
					if(counter <current && Userinput.length==words[i].length){
						//find most likely sentence
						counter = current;
						console.log("id"+saveID);
						saveID=i;
					}
					console.log("ID:",saveID," Words:",words[i][0],"::",Userinput[0],"Counter:",counter);
					current=0;
				}
				
				if(counter == words[saveID].length && counter==Userinput.length){ //check if this is the found word
					string=reply(saveID);
				}else{
					string="I don't know that one. How would you like me to respond in the future?";
					learn = true; //learn mode on
				}
			  return string;
			}
			var textFile=null; //define the file
			loadDoc("test.asp"); //load the file needed
			function loadDoc(file) { //read a file
				//takes a while to fully load
			
			  var xhttp = new XMLHttpRequest();
			  xhttp.onreadystatechange = function() {
				if (this.readyState == 4 && this.status == 200) {
				  textFile=this.responseText;
				  if(textFile != null){
					  //text is present
					  console.log("file:"+textFile);
					  
				  }
				}
			  };
			  xhttp.open("GET", file, true); //open the specific file
			  xhttp.send();
			}
			
			console.log("cookie: "+((document.cookie.replace("↵", "")).replace("; expires=Thu, 01 Jan 2037 00:00:01 GMT;", "")).replace("content=","")+"ENDCOOKIE"); //output the file
			function write(message)
			{
				//output in the console box
				message=message.replace('>', '');
				
				var text = document.getElementById("AIoutput");
				var number = (text.innerHTML).length; //get the character length
				var lines = (text.innerHTML).split('>');
				
				if (lines.length >= lines ||number >= characterlength)
				{
					lines=lines.splice(1,lines.length);
					text = lines.join('>');
					document.getElementById("AIoutput").innerHTML  = text;
				}
				document.getElementById("AIoutput").innerHTML  = document.getElementById("AIoutput").innerHTML+ ('<br/>')+('>')+(message);
				
			}
				
				//
  				var User = document.getElementById("AIinput");
				var checker=true;
				if (User) {
				User.addEventListener("keyup", function(event) {
					//listen for keys
				  event.preventDefault();
				  
				  if (event.keyCode === 13) {
					  //enter key pressed
					  User.value=User.value.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"");
					  if(type == 0){ //the type 1 is selected
					  write(User.value.toLowerCase());
					  if(learn == false)
					  {
					  	if(checker==true){ //do this once
							if(textFile==null){
							  //if in debug mode
							  textFile="hello:there,hi#hi,hello#" ; //format of data
						  }else{
							  textFile=textFile+((document.cookie.replace("↵", "")).replace("; expires=Thu, 01 Jan 2037 00:00:01 GMT;", "")).replace("content=","") ; //format of data
						  }	
							checker=false;
						}
					  
					 console.log("file:"+textFile);
						  console.log(document.cookie);
					
					//console.log(User.value);
					previous=User.value.toLowerCase();
					write("Robot message: "+getAI(User.value.toLowerCase()));
					
					
					  }else{
						//learn mode
						 writeTo(previous,User.value);
						  learn=false; //make learn mode be off
						  
					  }
					  document.getElementById("AIinput").value = "";
					}else if(type == 1){
					  var sentence=(User.value).split(" ");//split to sentences
					  var sig=[];//significant words
					  var threshold=getPop();
					  console.log("threshold of significance: "+threshold);
					  for(i=0;i<sentence.length;i++){ //loop through every word
						  var vis=getVisited(sentence[i]);
						  
						  if(vis !=false){
							  if(vis >= threshold){ //word is deemed significant
								  sig.push(sentence[i]);
							  }
						  }
					  }
					  console.log("significant words: "+sig);
					  write("User input: "+User.value);
					  write("What you are trying to find out/say: "+sig);
					  document.getElementById("AIinput").value = "";
					  var other = "";
					  for(i=0;i<sentence.length;i++){
						  var found=0
						  for(j=0;j<sig.length;j++){
							  console.log(sig[j],sentence[i]);
							  if(sig[j]==sentence[i]){
								//found in array 
								  found+=1;
								  
							  }
						}
						  if(found==0){
							  other+=sentence[i]+",";//add the words which have no meaning
						  }
					  }
					  write("What you are discussing: "+other);
				  }else if(type == 2)
				{
					write("User message: "+User.value);
					  //cognitive example
					  //data layout 'pk:item:linkpk(strength),linkpk(strength)'
					  //check input
						 //add
						 
						 if(User.value=="a"){
							//enable add mode
							write("Add mode on");
							
							addmode=true;
						}else if(User.value=="q"){
							//quit
							write("Add mode off");
							write("Data entered: "+inputArray);
							//do stuff with data
							inputArray=[];
							addmode=false;
						}else if(addmode==true){
								inputArray.push(User.value);
								//gather each item till quit
								//add to string
								//set nodes as increased
						}
						
						
							document.getElementById("AIinput").value = "";
				}else{
					  write("User message: "+User.value);
					  document.getElementById("AIinput").value = "";
				  }
				  }
				  
				});
				}
