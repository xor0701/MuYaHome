#include <Ethernet.h>
#include <ArduinoJson.h>
#include <SPI.h>

bool receive_data=false;
bool data_check=false;

byte mac[] = { 0x90, 0xA2, 0xDA, 0x0D, 0x55, 0x6c };    // mac 주소만 변경해주자

EthernetClient client;

byte server[] = {118,67,130,241}; //서버의 ip를 적어주자
char web="118.67.130.241";
String answer;
int A = 2;
int B = 3;
int C = 4;
int D = 5;
int E = 6;
int F = 7;
int G = 8;
int headcount=0;
String line="";
String params="/callelevator12?signal=";


void getserver(){
  Serial.println(("Starting connection to server...")); 
  if (client.connect(server, 8080)) 
  { 
    Serial.println(("Connected to server")); 
    client.print("GET ");
    client.print("/callelevator12");
    client.println(" HTTP/1.1");
    client.print("Host: ");
    client.println(web);
    client.println("Connection: close");
    client.println();
    data_check=true;
  }

}

void setup(){

   pinMode(A, OUTPUT); 
   pinMode(B, OUTPUT);
   pinMode(C, OUTPUT);
   pinMode(D, OUTPUT);
   pinMode(E, OUTPUT);
   pinMode(F, OUTPUT);
   pinMode(G, OUTPUT);

   Serial.begin(9600);
   Ethernet.begin(mac);                       //mac 주소 이용해 알아서 IP등록이 된다.

   Serial.println(Ethernet.localIP());       //할당된 내 IP주소를 시리얼모니터롤 볼 수 있다.

   delay(1000);

 

  Serial.println("connecting...");

  client.connect(server, 8080);             //연결시도  만약 연결이 안되면 오래 지연됨

  if (client.connected()) {
    Serial.println("good");
    client.print("GET ");
    client.print("/callelevator12");
    client.println(" HTTP/1.1");

    client.print("Host: ");

    client.println(web);

    client.println("Connection: close");

    client.println();
    data_check=true;

  }

  else{ 

    Serial.println("fail");

  }

 

}


void loop()
{


      while(client.available()){
        char c=client.read();
        if(c=='{')
        {
          receive_data=true;
        }
        else if(receive_data==true)
        {
          line+=c;
        }
      }
      if(data_check==true){
        if(!client.connected())
        {
          client.stop();
          String message=json_parser(line,"message");
          int el_before=json_parser(line,"el_before").toInt();
          int el_after=json_parser(line,"el_after").toInt();
          Serial.println(message);
          data_check=false;
          ELcheck(message,el_before,el_after);
        }
      }
      else if(data_check==false){
        delay(5000);
        getserver();
        line="";
      }
   

      

  
/*// number 0
digitalWrite (A,HIGH);
digitalWrite (B,HIGH);
digitalWrite (C,HIGH);
digitalWrite (D,HIGH);
digitalWrite (E,HIGH);
digitalWrite (F,HIGH);
digitalWrite (G,LOW);
delay (1000);
// number 1
digitalWrite (A,LOW);
digitalWrite (B,HIGH);
digitalWrite (C,HIGH);
digitalWrite (D,LOW);
digitalWrite (E,LOW);
digitalWrite (F,LOW);
digitalWrite (G,LOW);
if(digitalRead(A)==LOW && digitalRead(B)==HIGH && digitalRead(C)==HIGH && digitalRead(D)==LOW && digitalRead(E)==LOW && digitalRead(F)==LOW && digitalRead(G)==LOW ){
    client.print("GET ");
    client.print("/test?signal=1");
    client.println(" HTTP/1.0");
    client.print("Host: ");
    client.println(web);
    client.println("Connection: close");
    client.println();
}
delay (1000);
// number 2
digitalWrite (A,HIGH);
digitalWrite (B,HIGH);
digitalWrite (C,LOW);
digitalWrite (D,HIGH);
digitalWrite (E,HIGH);
digitalWrite (F,LOW);
digitalWrite (G,HIGH);
if(digitalRead(A)==HIGH && digitalRead(B)==HIGH && digitalRead(C)==LOW && digitalRead(D)==HIGH && digitalRead(E)==HIGH && digitalRead(F)==LOW && digitalRead(G)==HIGH ){
    client.print("GET ");
    client.print("/test?signal=2");
    client.println(" HTTP/1.0");
    client.print("Host: ");
    client.println(web);
    client.println("Connection: close");
    client.println();
}
delay (1000);
// number 3
digitalWrite (A,HIGH);
digitalWrite (B,HIGH);
digitalWrite (C,HIGH);
digitalWrite (D,HIGH);
digitalWrite (E,LOW);
digitalWrite (F,LOW);
digitalWrite (G,HIGH);
if(digitalRead(A)==HIGH && digitalRead(B)==HIGH && digitalRead(C)==HIGH && digitalRead(D)==HIGH && digitalRead(E)==LOW && digitalRead(F)==LOW && digitalRead(G)==HIGH ){
    client.print("GET ");
    client.print("/test?signal=3");
    client.println(" HTTP/1.0");
    client.print("Host: ");
    client.println(web);
    client.println("Connection: close");
    client.println();
}
delay (1000);
// number 4
digitalWrite (A,LOW);
digitalWrite (B,HIGH);
digitalWrite (C,HIGH);
digitalWrite (D,LOW);
digitalWrite (E,LOW);
digitalWrite (F,HIGH);
digitalWrite (G,HIGH);
if(digitalRead(A)==LOW && digitalRead(B)==HIGH && digitalRead(C)==HIGH && digitalRead(D)==LOW && digitalRead(E)==LOW && digitalRead(F)==HIGH && digitalRead(G)==HIGH ){
    client.print("GET ");
    client.print("/test?signal=4");
    client.println(" HTTP/1.0");
    client.print("Host: ");
    client.println(web);
    client.println("Connection: close");
    client.println();
}
delay (1000);
// number 5
digitalWrite (A,HIGH);
digitalWrite (B,LOW);
digitalWrite (C,HIGH);
digitalWrite (D,HIGH);
digitalWrite (E,LOW);
digitalWrite (F,HIGH);
digitalWrite (G,HIGH);
if(digitalRead(A)==HIGH && digitalRead(B)==LOW && digitalRead(C)==HIGH && digitalRead(D)==HIGH && digitalRead(E)==LOW && digitalRead(F)==HIGH && digitalRead(G)==HIGH ){
    client.print("GET ");
    client.print("/test?signal=5");
    client.println(" HTTP/1.0");
    client.print("Host: ");
    client.println(web);
    client.println("Connection: close");
    client.println();
}
delay (1000);
// number 6
digitalWrite (A,HIGH);
digitalWrite (B,LOW);
digitalWrite (C,HIGH);
digitalWrite (D,HIGH);
digitalWrite (E,HIGH);
digitalWrite (F,HIGH);
digitalWrite (G,HIGH);
if(digitalRead(A)==HIGH && digitalRead(B)==LOW && digitalRead(C)==HIGH && digitalRead(D)==HIGH && digitalRead(E)==HIGH && digitalRead(F)==HIGH && digitalRead(G)==HIGH ){
    client.print("GET ");
    client.print("/test?signal=6");
    client.println(" HTTP/1.0");
    client.print("Host: ");
    client.println(web);
    client.println("Connection: close");
    client.println();
}
delay (1000);
// number 7
digitalWrite (A,HIGH);
digitalWrite (B,HIGH);
digitalWrite (C,HIGH);
digitalWrite (D,LOW);
digitalWrite (E,LOW);
digitalWrite (F,LOW);
digitalWrite (G,LOW);
if(digitalRead(A)==HIGH && digitalRead(B)==HIGH && digitalRead(C)==HIGH && digitalRead(D)==LOW && digitalRead(E)==LOW && digitalRead(F)==LOW && digitalRead(G)==LOW ){
    client.print("GET ");
    client.print("/test?signal=7");
    client.println(" HTTP/1.0");
    client.print("Host: ");
    client.println(web);
    client.println("Connection: close");
    client.println();
}
delay (1000);
// number 8
digitalWrite (A,HIGH);
digitalWrite (B,HIGH);
digitalWrite (C,HIGH);
digitalWrite (D,HIGH);
digitalWrite (E,HIGH);
digitalWrite (F,HIGH);
digitalWrite (G,HIGH);
if(digitalRead(A)==HIGH && digitalRead(B)==HIGH && digitalRead(C)==HIGH && digitalRead(D)==HIGH && digitalRead(E)==HIGH && digitalRead(F)==HIGH && digitalRead(G)==HIGH ){
    client.print("GET ");
    client.print("/test?signal=8");
    client.println(" HTTP/1.0");
    client.print("Host: ");
    client.println(web);
    client.println("Connection: close");
    client.println();
}
delay (1000);
// number 9
digitalWrite (A,HIGH);
digitalWrite (B,HIGH);
digitalWrite (C,HIGH);
digitalWrite (D,HIGH);
digitalWrite (E,LOW);
digitalWrite (F,HIGH);
digitalWrite (G,HIGH);
if(digitalRead(A)==HIGH && digitalRead(B)==HIGH && digitalRead(C)==HIGH && digitalRead(D)==HIGH && digitalRead(E)==LOW && digitalRead(F)==HIGH && digitalRead(G)==HIGH ){
    client.print("GET ");
    client.print("/test?signal=9");
    client.println(" HTTP/1.0");
    client.print("Host: ");
    client.println(web);
    client.println("Connection: close");
    client.println();
}
delay (1000);*/
}

String json_parser(String s, String a) { 
  String val; 
  if (s.indexOf(a) != -1) 
  { 
    int st_index = s.indexOf(a); 
    int val_index = s.indexOf(':', st_index); 
    if (s.charAt(val_index + 1) == '"')
    { 
      int ed_index = s.indexOf('"', val_index + 2); 
      val = s.substring(val_index + 2, ed_index);
    } 
    else 
    { 
      int ed_index = s.indexOf(',', val_index + 1); 
      val = s.substring(val_index + 1, ed_index); 
    } 
   } else 
   { 
    Serial.print(a); 
    Serial.println(F(" is not available")); 
    } 
    return val; 
 }

void ELcheck(String message,int el_before, int el_after)
{
  if(message=="연결됨"){
    Serial.println("공동문열림");

    if(el_before==1){
      //1층
      digitalWrite (A,LOW);
      digitalWrite (B,HIGH);
      digitalWrite (C,HIGH);
      digitalWrite (D,LOW);
      digitalWrite (E,LOW);
      digitalWrite (F,LOW);
      digitalWrite (G,LOW);
      delay(3000);
    }
    else if(el_before==2){
      //2층
      digitalWrite (A,HIGH);
      digitalWrite (B,HIGH);
      digitalWrite (C,LOW);
      digitalWrite (D,HIGH);
      digitalWrite (E,HIGH);
      digitalWrite (F,LOW);
      digitalWrite (G,HIGH);
      delay(3000);
      
      //1층
      digitalWrite (A,LOW);
      digitalWrite (B,HIGH);
      digitalWrite (C,HIGH);
      digitalWrite (D,LOW);
      digitalWrite (E,LOW);
      digitalWrite (F,LOW);
      digitalWrite (G,LOW);
      delay(3000);
    }
    else if(el_before==3){
      //3층
      digitalWrite (A,HIGH);
      digitalWrite (B,HIGH);
      digitalWrite (C,HIGH);
      digitalWrite (D,HIGH);
      digitalWrite (E,LOW);
      digitalWrite (F,LOW);
      digitalWrite (G,HIGH);
      delay(3000);

      //2층
      digitalWrite (A,HIGH);
      digitalWrite (B,HIGH);
      digitalWrite (C,LOW);
      digitalWrite (D,HIGH);
      digitalWrite (E,HIGH);
      digitalWrite (F,LOW);
      digitalWrite (G,HIGH);
      delay(3000);

       //1층
      digitalWrite (A,LOW);
      digitalWrite (B,HIGH);
      digitalWrite (C,HIGH);
      digitalWrite (D,LOW);
      digitalWrite (E,LOW);
      digitalWrite (F,LOW);
      digitalWrite (G,LOW);
      delay(3000);
    }


    if(el_after==1){
      //1층
        digitalWrite (A,LOW);
        digitalWrite (B,HIGH);
        digitalWrite (C,HIGH);
        digitalWrite (D,LOW);
        digitalWrite (E,LOW);
        digitalWrite (F,LOW);
        digitalWrite (G,LOW);
        delay(3000);
    }
    else if(el_after==2){
      //1층
      digitalWrite (A,LOW);
      digitalWrite (B,HIGH);
      digitalWrite (C,HIGH);
      digitalWrite (D,LOW);
      digitalWrite (E,LOW);
      digitalWrite (F,LOW);
      digitalWrite (G,LOW);
      delay(3000);

      //2층
      digitalWrite (A,HIGH);
      digitalWrite (B,HIGH);
      digitalWrite (C,LOW);
      digitalWrite (D,HIGH);
      digitalWrite (E,HIGH);
      digitalWrite (F,LOW);
      digitalWrite (G,HIGH);
      delay(3000);
    }
    else if(el_after==3){
      //1층
      digitalWrite (A,LOW);
      digitalWrite (B,HIGH);
      digitalWrite (C,HIGH);
      digitalWrite (D,LOW);
      digitalWrite (E,LOW);
      digitalWrite (F,LOW);
      digitalWrite (G,LOW);
      delay(3000);

      //2층
      digitalWrite (A,HIGH);
      digitalWrite (B,HIGH);
      digitalWrite (C,LOW);
      digitalWrite (D,HIGH);
      digitalWrite (E,HIGH);
      digitalWrite (F,LOW);
      digitalWrite (G,HIGH);
      delay(3000);

      //3층
      digitalWrite (A,HIGH);
      digitalWrite (B,HIGH);
      digitalWrite (C,HIGH);
      digitalWrite (D,HIGH);
      digitalWrite (E,LOW);
      digitalWrite (F,LOW);
      digitalWrite (G,HIGH);
      delay(3000);
    }
  }
  else if(message=="연결안됨"){
    Serial.println("문안열림");
  }
}
