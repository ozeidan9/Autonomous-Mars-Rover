#include "WiFi.h"
#include <SPI.h>

#define RXP2 3
#define TXP2 1


char DriveMap[32]; //storage for drive's message
char Command[32]; //storage for the actual command


const char* ssid = "ENTER_NAME_HERE"; //Wifi Name
const char* password = "ENTER_PASSWORD_HERE"; //Wifi password

const uint16_t port = 1800; //port number to connect to
const char * host = "ENTER_IP_HERE"; //IP to connect to (can be private or public)

bool drivemsgready = false; //bool which checks whether drive's message is ready for sending
bool alreadyconnected = false; //bool which checks whether the ESP32 has already connected with the server
bool commandready = false; //bool which checks whether command is ready for sending command

//Event for when the ESP32 successfully connects as a Wifi Station
void WiFiConnected(WiFiEvent_t event, WiFiEventInfo_t info){
  Serial.println("Connected to Web Backend successfully!");
}

//Event for when the ESP32 successfully receives it's local IP from the router
void WiFiGotIP(WiFiEvent_t event, WiFiEventInfo_t info){
  Serial.println("WiFi connected");
  Serial.print("RRSI: ");
  Serial.println(WiFi.RSSI());
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

//Event for when the ESP32 disconnects from the Wifi (tries to reconnect)
void WiFiDisconnected(WiFiEvent_t event, WiFiEventInfo_t info){
  Serial.println("Disconnected from WiFi access point");
  Serial.print("WiFi lost connection. Reason: ");
  Serial.println(info.disconnected.reason);
  Serial.println("Trying to Reconnect");
  WiFi.begin(ssid, password);
  Serial.print("Reconnecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(1000);
  }
}


//Function for initialising connection to the WIFI
void initWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(1000);
  }
}


void setup() {

  Serial.begin(115200); //Debugging Line
  Serial2.begin(115200, SERIAL_8N1, RXP2, TXP2); // UART with Drive
  
  WiFi.disconnect(true);
  delay(1000);

  //Initialising events so that they run when the corresponding events occur
  WiFi.onEvent(WiFiConnected, SYSTEM_EVENT_STA_CONNECTED);
  WiFi.onEvent(WiFiGotIP, SYSTEM_EVENT_STA_GOT_IP);
  WiFi.onEvent(WiFiDisconnected, SYSTEM_EVENT_STA_DISCONNECTED);

  //Running the initialisation of Wifi
  initWiFi();

}

void loop() {
  
  WiFiClient client; //Initialising ESP32 as a client

  while(true){

    if(!alreadyconnected){    //Attempts to connect to Server using provided Host and Port
      if (!client.connect(host, port)) {
        Serial.println("Connection to host failed");
        delay(100);
        return;
      }
      Serial.println("Connected to server!");
      client.print("Hello from Control!");
      alreadyconnected = true;
    }


    if(Serial2.available()){ // read the bytes incoming from the UART Port:
      driveready = true;
      drivemsgready = true;  //check

      char DriveMap = Serial2.read();
      DriveMap = 'MAP' + DriveMap;   //check if it concatenates
      Serial.print("Sending Drive MAP to command: ");
      for(int i = 0; i < 32; i++){
        Serial.write(DriveMap[i]);
        client.write(DriveMap[i]);
        DriveMap[i] = ' ';
      }
      Serial.println();
      client.write('\n');
      }

    if(client.available()  && !commandready ){
      while(client.available()){
        char Commandchar = client.read(); //client.read() reads one character at a time
        if(Commandchar != 'M' || Commandchar != 'O' || Commandchar != 'V'){
          Command[i] = Commandchar;
          i++;
        }else{
          Serial.println("The Command has been recorded");
          commandready = true;
          break;
        }
      }
    }

      //Checks if drive and command are ready for moving the rover
      if(drivemsgready && commandready){
        Serial.print("Sending command to drive: ");
        for(int i = 0; i < 32; i++){
          Serial.write(Command[i]);
          Serial2.write(Command[i]);
          Command[i] = ' ';
        }
        Serial.println();
        Serial2.write('\n');
        drivemsgready = false;
        commandready = false;
      }
        
    
  }
}