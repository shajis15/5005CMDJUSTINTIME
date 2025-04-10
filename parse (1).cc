//This C++ code is used to take an input string and  
// put the instructions in an array   
#include <iostream>   
#include <string>   
#include <sstream>  
using namespace std;   
int main() {  //set up input string
      string input="left 2seconds";
      //initalise input stream
       stringstream currentstring(input);
      int count=-1;
      string instruction[10];
      //Repeatedly put instruction in string array
      while (currentstring.good())
          {
           count=count+1;
           currentstring >> instruction[count];
          }
      return 0;   }
