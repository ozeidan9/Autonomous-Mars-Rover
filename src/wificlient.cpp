#include <Arduino.h>
#include <WiFi.h>
#include <SPI.h>
#define LED 2

// IPAddress local_IP (192, 168, 1, 184);
// IPAddress gateway(192, 168, 1, 1);
// IPAddress subnet (255, 255, 0, 0);
#define RXP1 17 //Defining UART With Vision (Pins 8 and 9 on Arduino Adaptor)
#define TXP1 16

WiFiClient client;
unsigned long previousMillis = 0;
unsigned long interval = 30000;

bool connected = false;
const char * host = "192.168.137.190";
const uint16_t port = 9000;
char vision_msg;
int i = 0;

void initWifi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin("DESKTOP-6F3P5EH 1900", "L;5189d0");
  Serial.print("Connecting to wifi...");
  while (WiFi.status() != WL_CONNECTED){
    Serial.print('.');
    delay(1000);
  }
  Serial.println("coming in 3");
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(115200);
  Serial1.begin(115200, SERIAL_8N1, RXP1, TXP1); //Uart with Vision);

  pinMode(LED, OUTPUT);
  Serial.println("started setup");
  initWifi();
  if (!WiFi.config(local_IP, gateway, subnet)){
    Serial.println("STA failed to configure");
  }else{
    Serial.println("changed IP");
  }
  Serial.println("finishing setup");
  Serial.println("done setting up wifi");
  
}

void loop() {
  Serial.println("started loop");
  unsigned long currentMillis = millis();
  if ((WiFi.status() != WL_CONNECTED) && (currentMillis - previousMillis >= interval)){
    Serial.println(millis());
    Serial.println("reconnecting to wifi");
    WiFi.disconnect();
    WiFi.reconnect();
    previousMillis = currentMillis;
  }
    


    //code for communicating with command via TCP
    while(true){
        if(!connected){
            if (!client.connect(host, port)) {
            Serial.println("Connection to host failed");
            delay(100);
            return;
            }
            Serial.println("Connected to server!");
            client.print("0");
            connected = true;
        }
        else{
            if (i == 0){
              i = 1;
              Serial.println("printing 1");
              client.print("1");
            }else{
              i = 0;
              Serial.println("printing 0");
              client.print("0");
            }
            
        }
        while (client.available())
        {
          char c = client.read();
          Serial.println(c);
        }
        delay(1000);


    // code for communicating with FPGA via UART
      while(Serial1.available()){
        vision_msg = Serial1.read();
        Serial.println(vision_msg);
      }
      Serial.println("end of msg");
      
    
      Serial.println("end of loop");
      delay(1000);
    }
        
}

// #include <Arduino.h>
// #define LED 2
// void setup() {
//   Serial.begin(115200);
//   pinMode(LED, OUTPUT);
// }

// void loop() {
//   digitalWrite(LED, HIGH);
//   Serial.println("LED is on");
//   delay(1000);
//   digitalWrite(LED, LOW);
//   Serial.println("LED is off");
//   delay(1000);
// }