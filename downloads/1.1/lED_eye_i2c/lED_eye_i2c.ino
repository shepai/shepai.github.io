#include <Wire.h>

/* AI LED eye output code
 *  written by Joshua Hasset, age 15
 *  updated by Dexter Shepherd, age 15
*/
char c;
int face = 0;
// Arduino Pin Definitions
int rowPin[] = {2,3,4,5,6,7,8,9};         // An Array defining which Arduino pin each row is attached to
                                          // (The rows are common anode (driven HIGH))
int colPin[] = {17,16,15,14,13,12,11,10}; // An Array defining which pin each column is attached to

//the faces are to be added               // (The columns are common cathode (driven LOW))
byte smile[] = {                          // The array used to hold a bitmap of the display 
  B00000000,
  B00000000,
  B01000010, 
  B10111101, 
  B10011001,
  B01011010, 
  B00111100, 
  B00000000};

byte sad[] = {                          // The array used to hold a bitmap of the display 
  B00000000,
  B00111100,
  B01011010, 
  B10011001, 
  B10111101,
  B01000010, 
  B00000000, 
  B00000000};

byte normal[] = {                          // The array used to hold a bitmap of the display 
  B00000000,
  B00111100,
  B01000010, 
  B10011001, 
  B10011001,
  B01000010, 
  B00111100, 
  B00000000};
void setup()
{ 
  Wire.begin(8);                // join i2c bus with address #8
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(9600);
  for(int i = 0; i <8; i++){             // Set the 16 pins used to control the array to be OUTPUTs
    pinMode(rowPin[i], OUTPUT);          // These correspond to the Arduino pins stored in the arrays
    pinMode(colPin[i], OUTPUT);
  }
}

void loop()
{
  displaySprite();                       // Display the Sprite
}

void displaySprite(){
  for(int count = 0; count < 8; count++){ // A utility counter
    for(int i = 0; i < 8; i++){                          
      digitalWrite(rowPin[i], LOW);       // Turn off all row pins  
    }
    for(int i = 0; i < 8; i++){           // Activate only the Arduino pin of the column to light up
      if(i == count){     
        digitalWrite(colPin[i], LOW);     // Setting this LOW connects the current column's cathode to ground
      }  
      else{                
        digitalWrite(colPin[i], HIGH);    // Setting HIGH Turns all the other rows off
      }
    }
    if(face == 1){
    for(int row = 0; row < 8; row++){       // Iterate through each pixel in the current column
      int bit = (smile[count] >> row) & 1;  // Use a bit shift in the data[] array to do a bitwise comparison
                                            // And assign the result of the comparison to the bit
      if(bit == 1){                         // If the bitwise comparison is 1, 
        digitalWrite(rowPin[row], HIGH);    // Then light up the LED
      }
    }
    }else if(face == 2){
      for(int row = 0; row < 8; row++){       // Iterate through each pixel in the current column
      int bit = (sad[count] >> row) & 1;  // Use a bit shift in the data[] array to do a bitwise comparison
                                            // And assign the result of the comparison to the bit
      if(bit == 1){                         // If the bitwise comparison is 1, 
        digitalWrite(rowPin[row], HIGH);    // Then light up the LED
      }
    }
    }else{
      for(int row = 0; row < 8; row++){       // Iterate through each pixel in the current column
      int bit = (normal[count] >> row) & 1;  // Use a bit shift in the data[] array to do a bitwise comparison
                                            // And assign the result of the comparison to the bit
      if(bit == 1){                         // If the bitwise comparison is 1, 
        digitalWrite(rowPin[row], HIGH);    // Then light up the LED
      }
    }
    }
  } 
}
void receiveEvent(int howMany) {

  char x = Wire.read();   
  Serial.println(x);         // print the integer
  if(x == 'h'){
    face = 1;
  }else if(x == 's'){
    face = 2;
  }else{
    face = 0;
  }
  Serial.println(face);
}
