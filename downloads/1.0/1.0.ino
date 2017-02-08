/*version 2 prototype code
 *developed by Dexter Shepherd
 *Age 14
 *the system will be able to get input from a user
 *then decide wha to say back using its memory of previous
 *user says and robot replies.
 */

#include <SPI.h>
#include <SD.h>

File Memory;    //create file variable for global use
//declare all variables
    
char incomingByte = 0;   // for incoming serial data

String bytes = "";
int var = 0;
String wordarray[20] = {}; 

int h = 0;
String wordstring; 
String lines;
const int chipSelect = 53;

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
int f = 2;

void setup() {
    
Serial.begin(9600);     

while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }


  

  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    return;
  } 
  



   //reset so the system can be used again. 
Serial.println("\n");
Serial.println("USER MESSAGE: ");
}
void loop()
{
 while(Serial.available() > 0) {    //get the user input, this will eventually be replaced by voice recognition
                // read the incoming byte:
                incomingByte = Serial.read();
                bytes += incomingByte;
 }

delay(1000);
 if (bytes != ""){

   Serial.println(bytes);
  bytes+= " ";
  var +=1;

 char array[32] = {};
while(variable <= bytes.length())
{
  array[i] = bytes[i];
  i++;
  
  wordstring += array[g];
  delay(25);
  
  if(array[g] == ' ')
  {
    wordarray[h] = wordstring;
    //Serial.print(wordarray[h]);
    h += 1;
    wordstring = "";
    arraysize += 1;
    delay(10);
  }
  variable += 1;
  g += 1;
}
bytes.toLowerCase();
bytes.trim(); //get rid of unecesary waste
check();
 }
}


void check()
{
  int variable2 = 0;
  String wordarray2[15] = {};
  delay(10);
  counter();
  Memory = SD.open("memory.txt");
  if(Memory)
  {
    while (var <= sizee)
    {
      string = "";
      findin();
      
      //debuggin |
      //         V
      //Serial.println("***");
      //Serial.println(bytes);
      //Serial.println("***");
      //Serial.println(string);
      if(bytes == string) //if the input has already been said and saved
      {
        Serial.println("\n");
        Serial.println("ROBOT MESSAGE:");
        findout();  //get the robots message
        Serial.println(outputString); //output the robots message
        globalx = 1;
        break;
      }else{
        string = "";
        nextbyte();
      }
      
      var +=1;
    }
    pos = 0; 
    variable = 0;
    if(globalx == 0){
      while(variable < sizee)
      {
        //find words and match
        getarray();
        variable += 1;
      }
        while(true)
            {
              //Serial.println(currentline);
              
              if (currentline == 0)
              {
                pos = 0;
                var = 0;
                outputString = "";
                writeu();
                Serial.println("save");
                delay(10);
                Memory.close();
                Memory = SD.open("lines.txt", FILE_WRITE);
                if(Memory)
                {
                  Memory.print("1");
                  Memory.close();
                }else{
                  Serial.println("error opening lines");
                }
      
                Memory = SD.open("memory.txt", FILE_WRITE);
                Memory.print(bytes);
                Memory.print("*");
                Memory.print(outputString);
                Memory.print(" /");
                
              }
        while(var < currentline*2)
        {
          pos = 0;
          var += 1;
          string = "";
          outputString = "";
          findin();
          //Serial.print("---");
          //Serial.println(currentline);
          pos = currentline;
          findout();
          
        }
        Serial.println("ROBOT MESSAGE: ");
        Serial.println(outputString);
        break;
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
  Serial.println("ROBOT MESSAGE: ");
          Serial.println("i dont know how to respond to that... How would you respond to that?");
          Serial.print("\n");
          Serial.println("USER MESSAGE:");
          outputString = "";
          while(true)
          {
            while(Serial.available() > 0) {    //get the user input, this will eventually be replaced by voice recognition
                // read the incoming byte:
                incomingByte = Serial.read();
                outputString += incomingByte;
            }
            delay(1000);
          if(outputString != ""){
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
    delay(5);
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
      sr.trim();
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
  delay(5);
  //Serial.println(datastring);
}
void nextbyte()
{

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
  Memory = SD.open("lines.txt");
  if(Memory)
  {
    sizee = Memory.size();
    //Serial.println(sizee);
    Memory.close();
  }else{
    Serial.println("error opening lines");
  }
}

