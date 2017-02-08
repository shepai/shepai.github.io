/*version 2 prototype code
 *developed by Dexter Shepherd
 *Age 15
 *the system will be able to get input from a user
 *then decide wha to say back using its memory of previous
 *user says and robot replies.
 *the system will look at the vocabulary to decide
 *the mood of conversation (negative/ positive)
 */

#include <SPI.h>
#include <SD.h>
#include <Wire.h>
#include "MOVIShield.h"
#ifdef ARDUINO_ARCH_AVR 
#include <SoftwareSerial.h> // This is nice and flexible but only supported on AVR architecture, other boards need to use Serial1 
#endif

//declare all variables

MOVI recognizer(true);
File Memory;    //create file variable for global use

char incomingByte = 0;   // for incoming serial data
String filename = ""; //decide the mood file to open up
String linenum = "";  //to find the amount of programed in commands within files
String bytes = "";  //gather input
int var = 0;

String wordarray[18] = {}; //gather the words
int h = 0;
String wordstring; 
String lines;
const int chipSelect = 53; //sd pin
boolean stop = true;
int variable = 0;
int sizee = 0;
String response = "";
char x;
int pos = 0;
String string;
String outputString;
int globalx = 0;
int i = 0;
int g = 0;
int count = 0;
int arraysize = 0;
int times = 0;
int current; 
int currentline;
int spacepos = 0;
int globaly = 0;
int f = 5;
int gx1 = 0;
String trigger[60] = {};

const int led = 13;
int currentTH = 0;
void setup() {
    
Serial.begin(9600);     
Wire.begin(2);
   

 while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    return;
  } 
  Memory = SD.open("words.txt");
  if (Memory) {
    Serial.println("words.txt:");
    int aaa = 0;
    // read from the file until there's nothing else in it:
    while (true){
      Memory.seek(pos);
      char rb = Memory.peek();
      if(rb == ',')
      {
        trigger[aaa] = string;
        Serial.println(trigger[aaa]);
        aaa += 1;
        string = "";
      }else if(rb == '/')
      {
        trigger[aaa] = string;
        break;
      }else{
        string += rb;
      }
      pos += 1;
    }
    pos = 0;
    string = "";
    // close the file:
    Memory.close();
  } else {
    // if the file didn't open, print an error:
    Serial.println("error opening words.txt");
  }
  delay(1000);
Serial.println("\n");
Serial.println("USER MESSAGE: "); //for user interface
Wire.beginTransmission(1); // transmit to device #8
      Wire.write('#');        // sends three bytes
      Wire.endTransmission(stop); 
delay(1000);
pinMode(led, OUTPUT);    // Make LED port writeable
  digitalWrite(led, HIGH); // Blink LED.   
  delay(1);                   
  digitalWrite(led, LOW);  
  delay(1); 

  recognizer.init();      // Initialize MOVI (waits for it to boot)

  //*
  // Note: training can only be performed in setup(). 
  // The training functions are "lazy" and only do something if there are changes. 
  // They can be commented out to save memory and startup time once training has been performed.
  recognizer.callSign("Robot"); // Train callsign Arduino (may take 20 seconds)
  recognizer.addSentence("Hello you"); // Add sentence 1
  recognizer.addSentence("you have cancer");            // Add sentence 2
  recognizer.addSentence("how are you");
  recognizer.addSentence("i am good thank you");
  recognizer.addSentence("i am sad");
  recognizer.addSentence("i am good");
  while(trigger[pos] != "")
  {
    recognizer.addSentence(trigger[pos]);
    pos += 1;
  }
  pos = 0;
  recognizer.train();       
}
void loop()
{
getinput();
}

void getinput()
{
  int val;
  int val1;
  int potpin = A0;
  int potpin1 = A1;
  int currentV = 0;
  while(true)
  {
    /*
    val = analogRead(potpin);            // reads the value of the potentiometer (value between 0 and 1023)
  val = map(val, 0, 1023, 0, 100);
    if(currentTH == val)
    {
      recognizer.setThreshold(val);
    }
    val1 = analogRead(potpin1);            // reads the value of the potentiometer (value between 0 and 1023)
  val1 = map(val1, 0, 1023, 0, 100);
    if(currentV == val1)
    {
      recognizer.setVolume(val1);
    }
    */
    signed int res=recognizer.poll(); 
  if (res==RAW_WORDS) {             // The event raw_words let's us get the words via getResult()
    String result=recognizer.getResult();  // Get the result and save it in a string
    int numwords=1;     
    Serial.println(result);
     
    delay(1000);
    if(gx1 == 0)
    {  
      bytes = result; 
      int a = 0;
      while(a != bytes.length())
        {
        Wire.beginTransmission(1); // transmit to device #8
              Wire.write(bytes[a]);        // sends three bytes
              Wire.endTransmission(stop); 
        Serial.println(bytes); //show user theri sentence
           a += 1;
        }
    checkaudio();
    break;
    }else if(gx1 == 2)
    {
      outputString = result;
      break;
    }
  }  
  }
}
void check()
{
  //main function which sorts through all the senarios on what its going to output
  checkfile();  //goes to the fucntion which checks the mood of conversation
  int variable2 = 0;
  String wordarray2[15] = {};
  delay(10);
  
  counter();  //counts the amount of lines in the sentence
  Memory = SD.open(filename); //opens the mood file
  if(Memory)
  {
    while (var <= sizee)  //while the counter is less than the amount of phrases in the data
    {
      
      //this part checks for an exact replica 
      string = "";
      findin(); //get the first input
      
      //debuggin |
      //         V
      //Serial.println("***");
      //Serial.println(bytes);
      //Serial.println("***");
      //Serial.println(string);
      if(bytes == string) //if the input has already been said and saved
      {
        Serial.println("\n");
        Serial.println("ROBOT MESSAGE:"); //UI 
        findout();  //get the robots message
        Serial.println(outputString); //output the robots message
        recognizer.say(outputString);
        globalx = 1;
        Memory.close();
        reset();
      }else{
        string = "";
        nextbyte(); //go to the next phrase in the data
      }
      
      var +=1;
    }
    delay(10);
    pos = 0; 
    variable = 0;
    if(globalx == 0){ //decider whether to exit or not (if an input has already be found or not)
      //this part checks for likely phrases
      while(variable < sizee)
      {
        //find words and match
        getarray(); //split the phrase into an array and check the simularities
        variable += 1;
      }
        while(true)
            {
              //Serial.println(currentline);
              
              if (currentline == 0)
              {
                //if nothing mathes or is simular in the data
                pos = 0;
                var = 0;
                outputString = "";
                writeu(); //get input from the user for next time to save equal to the current user input
                Serial.println("save");
                delay(10);
                Memory.close();
                Memory = SD.open(linenum, FILE_WRITE);  //increase the tally file on the amount of phrases inside
                if(Memory)
                {
                  Memory.print("1");
                  Memory.close();
                }else{
                  Serial.println("error opening lines");
                }
      
                Memory = SD.open(filename, FILE_WRITE); //save the new phrases and its response
                Memory.print(bytes);
                Memory.print("*");
                Memory.print(outputString);
                Memory.print(" /");
                Memory.close();
                reset();
              }
              
              //code gets here if it had likely inputs
        while(var < currentline*2)  //random loop condition
        {
          pos = 0;
          var += 1;
          string = "";
          outputString = "";
          findin(); //find input
          //Serial.print("---");
          //Serial.println(currentline);
          pos = currentline;
          findout();  //find output
          
        }
        Serial.println("ROBOT MESSAGE: ");
        Serial.println(outputString); //output likely scenario
        recognizer.say(outputString);
        Memory.close();
        reset();
      }
    }
    Memory.close();
  }else{
    Serial.println("error opening memory");
  }
  //reset so it will be able to start again
  reset();

}
void writeu()
{
  //the learning code
  Serial.println("ROBOT MESSAGE: ");
          Serial.println("i dont know how to respond to that... How would you respond to that?");
          recognizer.say("i dont know how to respond to that... How would you respond to that?");
          Serial.print("\n");
          Serial.println("USER MESSAGE:");
          outputString = "";
          gx1 = 2;
          while(true)
          {
            getinput();
            delay(2000);
          if(outputString != ""){
            delay(500);
            Serial.println(outputString);
            break;
          }else{
            
          }
          }
          
          
}

void findout()
{
  while(true)
        {
          pos +=1;
          Memory.seek(pos);
          x = Memory.peek();
          
          if(x == '/')
          {
            break;
          }
          
          outputString += x;
        }
}

void findin()
{
  while(true)
      {
        Memory.seek(pos);
        x = Memory.peek();
        
        if(x == '*')
        {
          break;
        }
        
        string += x;
        pos += 1;
      }
}

void getarray()       //sort thorugh and find likely sentence
{
  
  //Serial.println("array");
  String c = "";
  String datastring = "";
  string = "";
  
  findin();
  count = 0;
  int a = 0;
  int vara = 0;
  int wordlen = 0;
  string += " ";
  while(vara != arraysize)
  {
  while(var != string.length())
  {
    delay(10);
    c = string[a];
    //Serial.print(c);
    //Serial.println(pos);
    if (c == "/")
    {
      
    }else if(c == " "){
      //Serial.println("new word");
      //Serial.println(datastring);
      
      String sr = "";
      sr = wordarray[vara];
      sr.trim();  //get rid of waiste
      sr.trim();
      //Serial.println(wordarray[vara]);
      wordlen += 1;
      if(datastring == sr){

         
        
        count += 1;
        
      }
      datastring = "";
    }else if(c == ""){
      break;
    }else{
    
    //Serial.println(wordarray[vara]);
      datastring += c;
      
    }
    var += 1;
    a += 1;
  }
  
  vara += 1;
  var = 0;
  }
  if (count > current)
  {
     if(count >= wordlen/2)    //check if it is equal to half the sentence using luck algorithm
        {
    current = count;
    currentline = pos;
    //Serial.println(currentline);
        }
  }
  findout();
  delay(10);
  //Serial.println(datastring);
}
void nextbyte()
{
//skip through the system to find the next phrase
        while(true)
        {
          Memory.seek(pos);
          x = Memory.peek();
          pos +=1;
          if(x == '/')
          {
            break;
          }
          
        }
}

void reset()
{
//reset system
delay(500);
pinMode(f, OUTPUT);
digitalWrite(f, HIGH);
}


void counter()
{
  //finds the amount of numbers
  Memory = SD.open(linenum);
  if(Memory)
  {
    sizee = Memory.size();
    //Serial.println(sizee);
    Memory.close();
  }else{
    Serial.println("error opening lines");
  }
}


void checkfile()
{
  //this code checks whcih data file to open
  int abc = 0;
  //Serial.println("de-crypting");
  while(true)
  {
    String checker = "";
    checker = wordarray[abc];
    checker.trim();
    if(checker == "good"||checker == "happy"||checker == "exited"||checker == "great"||checker == "perfect")
    {
      filename = "positive.txt";
      linenum = "lines1.txt";
      Wire.beginTransmission(8); // transmit to device #8
      Wire.write("h");        // sends five bytes
      Wire.endTransmission(stop);    // stop transmitting
      break;
    }else if(checker == "sad"||checker == "bad"||checker == "disapointed"||checker == "depressed"||checker == "upset")
    {
      filename = "negitive.txt";
      linenum = "lines2.txt";
      Wire.beginTransmission(8); // transmit to device #8
      Wire.write("s");        // sends three bytes
      Wire.endTransmission(stop);    // stop transmitting
      break;
    }else{
      filename = "memory.txt";
      linenum = "lines.txt";
       Wire.beginTransmission(8); // transmit to device #8
      Wire.write("n");        // sends six bytes
      Wire.endTransmission(stop);    // stop transmitting
      delay(10);
      delay(10);
    }
    if(abc >= arraysize)
    {
      break;
    }
    abc += 1;
  }
 Serial.println(filename);
}

void checkaudio()
{
 if (bytes != ""){  //makes sure the code does not skip through with no input
  bytes.toLowerCase();  //get rid of capitals so all words are the same
bytes.trim(); //get rid of unecesary waste
int a = 0;

a = 0;
  bytes+= " ";
  var +=1;
  
 char array[16] = {};
while(variable <= bytes.length())
{
  array[i] = bytes[i];
  i++;
  
  wordstring += array[g];
  delay(25);
  
  if(array[g] == ' ')
  {
    //at every space, split the word into a string array for later processing
    wordarray[h] = wordstring;
    h += 1;
    wordstring = "";
    arraysize += 1;
    delay(10);
  }
  variable += 1;
  g += 1;
}
checkfile();
check();  //go to the check function
 }
  }

