#include "SPI.h"
#include <Robojax_L298N_DC_motor.h>
#include "WiFi.h"
//vision
bool red_found;
bool green_found;
bool yellow_found;
bool pink_found;
bool darkblue_found;
bool lightgreen_found;
///////
//SPI settings
SPISettings settings(100000, MSBFIRST, SPI_MODE0);
SPIClass MySPI(HSPI);
uint8_t spi_counter[6]; // [0] = c20, [1] = c21, [2] = c22, [3] = c23, [4] = c24, [5] = c25
uint16_t spi_val, spi_val_prev1, spi_val_prev2;
uint8_t spi_reg;
uint16_t spi_returnval;
int spi_command;
int l;
int response;
bool will_read;
int last_read;
uint16_t colour_code;
uint16_t distrep;
uint16_t prev_distrep;
bool sent_dist;
int ball_counter = 0;
//////
//end of vision
bool vision_interrupt;
// these pins may be different on different boards
int motor1_val;
int motor2_val;
int motor_offset;
float desired = 0; //this will need to be a dynamic input connected to various things so it allows multiple directions instead of just one forward
unsigned long pathstart;//this should only be called during the update to record the time it takes for this new direction change, so this entire program needs to be called new each time the rover changes direction
//strt
//float pcoeff = 3;
//float icoeff = 0.025;
//float dcoeff = 3;
//float multiplier = 1;
float pcoeff = 3.6; //was 3.5, then 4.2
float icoeff = 0.005; //was 0.013, then 0.013
float dcoeff = 0.05; //was 0, then 0.2
float multiplier = 1;
//
//float pcoeff = 3.4;
//float icoeff = 0.02;
//float dcoeff = 3;
//float multiplier = 1;
//end
float ierror = 0;
float derror = 0;
float error;
unsigned long pathnow;
float correction;
//
uint8_t values[5];
int bytes_received;
bool angle_state = false;
bool distance_state = false;
int client_msg;
int opcode;
int magnitude;
char Commandchar;
int angle_reached;
int distance_reached;
//
#define PIN_SS        5
#define PIN_MISO      19
#define PIN_MOSI      23
#define PIN_SCK       18
#define PIN_MOUSECAM_RESET     35
#define PIN_MOUSECAM_CS        5
// TehCehPeh
#define RXP2 3
#define TXP2 1
// DRIVE
// motor 1 settings
#define CHA 0
#define ENA 2 // this pin must be PWM enabled pin if Arduino board is used D13 -> was 2
#define IN1 32 //D11
#define IN2 33 //D3 - was 15 (D12)
// motor 2 settings
#define IN3 21 //D4 //was 14  (D10)
#define IN4 16 //D9
#define ENB 17// this pin must be PWM enabled pin if Arduino board is used D8
#define CHB 1
#define ADNS3080_PIXELS_X                 30
#define ADNS3080_PIXELS_Y                 30
#define ADNS3080_PRODUCT_ID            0x00
#define ADNS3080_REVISION_ID           0x01
#define ADNS3080_MOTION                0x02
#define ADNS3080_DELTA_X               0x03
#define ADNS3080_DELTA_Y               0x04
#define ADNS3080_SQUAL                 0x05
#define ADNS3080_PIXEL_SUM             0x06
#define ADNS3080_MAXIMUM_PIXEL         0x07
#define ADNS3080_CONFIGURATION_BITS    0x0a
#define ADNS3080_EXTENDED_CONFIG       0x0b
#define ADNS3080_DATA_OUT_LOWER        0x0c
#define ADNS3080_DATA_OUT_UPPER        0x0d
#define ADNS3080_SHUTTER_LOWER         0x0e
#define ADNS3080_SHUTTER_UPPER         0x0f
#define ADNS3080_FRAME_PERIOD_LOWER    0x10
#define ADNS3080_FRAME_PERIOD_UPPER    0x11
#define ADNS3080_MOTION_CLEAR          0x12
#define ADNS3080_FRAME_CAPTURE         0x13
#define ADNS3080_SROM_ENABLE           0x14
#define ADNS3080_FRAME_PERIOD_MAX_BOUND_LOWER      0x19
#define ADNS3080_FRAME_PERIOD_MAX_BOUND_UPPER      0x1a
#define ADNS3080_FRAME_PERIOD_MIN_BOUND_LOWER      0x1b
#define ADNS3080_FRAME_PERIOD_MIN_BOUND_UPPER      0x1c
#define ADNS3080_SHUTTER_MAX_BOUND_LOWER           0x1e
#define ADNS3080_SHUTTER_MAX_BOUND_UPPER           0x1e
#define ADNS3080_SROM_ID               0x1f
#define ADNS3080_OBSERVATION           0x3d
#define ADNS3080_INVERSE_PRODUCT_ID    0x3f
#define ADNS3080_PIXEL_BURST           0x40
#define ADNS3080_MOTION_BURST          0x50
#define ADNS3080_SROM_LOAD             0x60
#define ADNS3080_PRODUCT_ID_VAL        0x17
WiFiClient client;
int distance_t = 0;
int angle_t = 0;
const int CCW = 2; // do not change
const int CW  = 1; // do not change
#define motor1 1 // do not change
#define motor2 2 // do not change
// for two motors without debug information // Watch video instruciton for this line: https://youtu.be/2JTMqURJTwg
Robojax_L298N_DC_motor robot(IN1, IN2, ENA, CHA,  IN3, IN4, ENB, CHB);
// for two motors with debug information
//Robojax_L298N_DC_motor robot(IN1, IN2, ENA, CHA, IN3, IN4, ENB, CHB, true);
char DriveMap[32]; //storage for drive's message
//char Command[32]; //storage for the actual command
const char* ssid = "AndroidAP5c48";//Wifi Name
const char* password = "janq9636";//Wifi password
const uint16_t port = 15000; //port number to connect to
const char * host = "192.168.43.192"; //IP to connect to (can be private or public)
bool drivemsgready = false; //bool which checks whether drive's message is ready for sending
bool alreadyconnected = false; //bool which checks whether the ESP32 has already connected with the server
bool Commandready = false; //bool which checks whether command is ready for sending command
bool SPIready = false;

//Event for when the ESP32 successfully connects as a Wifi Station
void WiFiConnected(WiFiEvent_t event, WiFiEventInfo_t info) {
  Serial.println("Connected to Web Backend successfully!");
}
//Event for when the ESP32 successfully receives it's local IP from the router
void WiFiGotIP(WiFiEvent_t event, WiFiEventInfo_t info) {
  Serial.println("WiFi connected");
  Serial.print("RRSI: ");
  Serial.println(WiFi.RSSI());
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}
//Event for when the ESP32 disconnects from the Wifi (tries to reconnect)
void WiFiDisconnected(WiFiEvent_t event, WiFiEventInfo_t info) {
  Serial.println("Disconnected from WiFi access point");
  Serial.print("WiFi lost connection. Reason: ");
  //Serial.println(info.disconnected.reason);
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
int angle;
int total_x = 0;
int total_y = 0;
int total_x1 = 0;
int total_y1 = 0;
int x = 0;
int y = 0;
int a = 0;
int b = 0;
int distance_x = 0;
int distance_y = 0;
volatile byte movementflag = 0;
volatile int xydat[2];
//Multitasking
TaskHandle_t Optical_task;
int convTwosComp(int b) {
  //Convert from 2's complement
  if (b & 0x80) {
    b = -1 * ((b ^ 0xff) + 1);
  }
  return b;
}
struct MD
{
  byte motion;
  char dx, dy;
  byte squal;
  word shutter;
  byte max_pix;
};
int tdistance = 0;
void mousecam_reset()
{
  digitalWrite(PIN_MOUSECAM_RESET, HIGH);
  delay(1); // reset pulse >10us
  digitalWrite(PIN_MOUSECAM_RESET, LOW);
  delay(35); // 35ms from reset to functional
}
int mousecam_init()
{
  pinMode(PIN_MOUSECAM_RESET, OUTPUT);
  pinMode(PIN_MOUSECAM_CS, OUTPUT);
  digitalWrite(PIN_MOUSECAM_CS, HIGH);
  mousecam_reset();
  return 1;
}
byte frame[ADNS3080_PIXELS_X * ADNS3080_PIXELS_Y];
void mousecam_write_reg(int reg, int val)
{
  digitalWrite(PIN_MOUSECAM_CS, LOW);
  SPI.transfer(reg | 0x80);
  SPI.transfer(val);
  digitalWrite(PIN_MOUSECAM_CS, HIGH);
  delayMicroseconds(50);
}
int mousecam_read_reg(int reg)
{
  digitalWrite(PIN_MOUSECAM_CS, LOW);
  SPI.transfer(reg);
  delayMicroseconds(75);
  int ret = SPI.transfer(0xff);
  digitalWrite(PIN_MOUSECAM_CS, HIGH);
  delayMicroseconds(1);
  return ret;
}
void mousecam_read_motion(struct MD *p)
{
  digitalWrite(PIN_MOUSECAM_CS, LOW);
  SPI.transfer(ADNS3080_MOTION_BURST);
  delayMicroseconds(75);
  p->motion =  SPI.transfer(0xff);
  p->dx =  SPI.transfer(0xff);
  p->dy =  SPI.transfer(0xff);
  p->squal =  SPI.transfer(0xff);
  p->shutter =  SPI.transfer(0xff) << 8;
  p->shutter |=  SPI.transfer(0xff);
  p->max_pix =  SPI.transfer(0xff);
  digitalWrite(PIN_MOUSECAM_CS, HIGH);
  delayMicroseconds(5);
}
// pdata must point to an array of size ADNS3080_PIXELS_X x ADNS3080_PIXELS_Y
// you must call mousecam_reset() after this if you want to go back to normal operation
int mousecam_frame_capture(byte *pdata)
{
  mousecam_write_reg(ADNS3080_FRAME_CAPTURE, 0x83);
  digitalWrite(PIN_MOUSECAM_CS, LOW);
  SPI.transfer(ADNS3080_PIXEL_BURST);
  delayMicroseconds(50);
  int pix;
  byte started = 0;
  int count;
  int timeout = 0;
  int ret = 0;
  for (count = 0; count < ADNS3080_PIXELS_X * ADNS3080_PIXELS_Y; )
  {
    pix = SPI.transfer(0xff);
    delayMicroseconds(10);
    if (started == 0)
    {
      if (pix & 0x40)
        started = 1;
      else
      {
        timeout++;
        if (timeout == 100)
        {
          ret = -1;
          break;
        }
      }
    }
    if (started == 1)
    {
      pdata[count++] = (pix & 0x3f) << 2; // scale to normal grayscale byte range
    }
  }
  digitalWrite(PIN_MOUSECAM_CS, HIGH);
  delayMicroseconds(14);
  return ret;
}
void Opticaltaskcode(void *param){
  SPI.begin();
  SPI.setClockDivider(SPI_CLOCK_DIV32);
  SPI.setDataMode(SPI_MODE3);
  SPI.setBitOrder(MSBFIRST);
 if (mousecam_init() == -1)
  {
    Serial.println("Mouse cam failed to init");
    while (1);
  }
  SPI.begin(); // init SPI bus
  while(1){
    int val = mousecam_read_reg(ADNS3080_PIXEL_SUM);
    MD md;
    mousecam_read_motion(&md);
    distance_x = convTwosComp(md.dx);
    distance_y = convTwosComp(md.dy);
    total_x1 = total_x1 - distance_x;
    total_y1 = total_y1 + distance_y;
    total_x = total_x1 * 0.0840;   //callibrated;
    total_y = total_y1 * 0.0193;  //callibrated;
  }
}
void setup()
{
  vision_interrupt = false;
  delay(6000);
  Serial.println("started setup");
  Serial.begin(115200);
  
  //vision setup
    spi_val=-1;
    pinMode(15, OUTPUT);
    MySPI.begin(14, 4, 22, 15);
    spi_returnval = 0;
    red_found = 0;
    green_found = 0;
    yellow_found = 0;
    pink_found = 0;
    darkblue_found = 0;
    lightgreen_found = 0;
    response = 0;
  //end of vision setup
 //Drive SPI setup
  pinMode(PIN_SS, OUTPUT);
  pinMode(PIN_MISO, INPUT);
  pinMode(PIN_MOSI, OUTPUT);
  pinMode(PIN_SCK, OUTPUT);
  WiFi.disconnect(true);
  
  robot.begin();
  //Second core shit...
  xTaskCreatePinnedToCore(
    Opticaltaskcode,
    "Optical_task",
    10000, //stack size in words
    NULL,  // input paramter to task
    0, //priority of task
    &Optical_task,
    0); //Core 0
  //initWiFi();
    WiFi.mode(WIFI_STA);
    WiFi.begin("AndroidAP5c48", "janq9636");
    Serial.print("Connecting to wifi...");
    while (WiFi.status() != WL_CONNECTED){
    Serial.print('.');
    delay(1000);
  }
  Serial.println("wifi connected");
  Serial.println(WiFi.localIP());
  client.connect(host, port);
  Serial.println("client connected");
  client.write("rover");
  Serial.println("line 547");
  sendtoServer(1, 0, 0);//initial sending of UPM
}
char asciiart(int k)
{
  static char foo[] = "WX86*3I>!;~:,`. ";
  return foo[k >> 4];
}
//function to send sets of bytes to the server...
void sendtoServer(int op,uint16_t first , uint16_t second){
      memset(values, 0, 4); //just resetting the buffer
      values[0] = op;
      values[1] = (first & 65280)>>8;
      values[2] = first & 255;
      values[3] = (second & 65280)>>8;
      values[4] = second & 255;
      client.write(values, 5);
      delay(100);
 //sendtoSever(3,0,0)
}
void loop()
{
//    if((counter % 2) == 0){
//      sendtoServer(0, 65484, 8396);
//      counter++;
//    }
//
//    if((counter % 2) == 1){
//      sendtoServer(1, 50, 60);
//      counter++;
//    }
//RE ADD ADDED ARDUINO CODE....
//start of vision loop
//Listening to vision:
    // MySPI.beginTransaction(settings);
    // digitalWrite(15, LOW);
    // spi_val = MySPI.transfer16(0);
    // spi_returnval = 0;
    // digitalWrite(15, HIGH);
    // MySPI.endTransaction();
    // Serial.print("start of data, having sent: ");
    // Serial.println(spi_val);
    // Serial.println("end of data");
    // //no data
    // if (spi_val == 0){
    //     SPIready = false;
    //     Serial.println("received zero");
    //     response=0;
    //     ball_counter = 0;
    // }
    // //too clsoe command
    // else if  (spi_val==13){
    //     spi_command = 0;
    //     SPIready = true;
    //     response=0;
    //     Serial.println("received 13. Too close!");
    //     ball_counter = 0;
    // }
    // //too far
    // else if  (spi_val==14){
    //     response=0;
    //     if (will_read=true){
    //     last_read=millis();
    //     will_read=false;
    //     spi_command = 0;
    //     SPIready = true;
    //     response=14;
    //     sent_dist = false;
    //     ball_counter = 0;
    //     Serial.println("received 14. requesting to measure building");
    //     //send back 14-                        ROHAN MA G let me know yeah
    //     }
    // }
    // //too far left/right
    // else if (spi_val == 9 || spi_val == 10) { 
    //     distance_t = total_y;
    //     if(vision_interrupt = false){
    //       Serial.println("executing vision interrupt");
    //       distance_t = total_y;
    //       angle_t = total_x;
    //       distance_state = false;
    //       angle_state = false;
    //       vision_interrupt = true;
    //       robot.brake(1);
    //       robot.brake(2);
    //     }
    //     else {
    //       angle_state = true;
    //       if(spi_val == 9){
    //         angle_t = total_y - 2;
    //       }
    //       else{
    //         angle_t = total_y + 2
    //       }
    //     }
  
    //     ball_counter = 0;
    // }
    // //error...
    // else if (spi_val ==-1){
    //     Serial.println("error failed to update spi connection");
    //     ball_counter = 0;
    // }
    // //detecting a ball/building
    // else{
    //     angle_t = total_x;
    //     distance_t = distance_y;
    //     angle_state = false;
    //     if(vision_interrupt = false){
    //       distance_t = total_y;
    //       angle_t = total_x;
    //       distance_state = false;
    //       angle_state = false;
    //       vision_interrupt = true;
    //       robot.brake(1);
    //       robot.brake(2);
    //     }
        
    //     colour_code = spi_val >> 11; //obtaining the colour code
    //     distrep = spi_val & 2047; //obtaining the message
    //     Serial.print("Colour_code: ");
    //     Serial.print(colour_code);
    //     Serial.print(" Distance: ");
    //     Serial.println(distrep);
    //     SPIready = true;
    //     Serial.println("Sending to server!");
    //     //incrementing ball_counter
    //     if(ball_counter ==0){
    //       prev_distrep = distrep;
    //     }
    //     else  if((distrep < prev_distrep+1) && (distrep >= prev_distrep-1)){
    //       ball_counter++;
    //       prev_distrep = distrep;
    //     }
    //     if(ball_counter > 3){
    //       sendtoServer(0, total_x, total_y);
    //       sendtoServer(2, colour_code, distrep);
    //       //registered the colour;
    //       MySPI.beginTransaction(settings);
    //       digitalWrite(15, LOW);
    //       spi_val = MySPI.transfer16(colour_code);
    //       spi_returnval = 0;
    //       digitalWrite(15, HIGH);
    //       MySPI.endTransaction();
    //       delay(500);
    //       ball_counter =0;
    //       vision_interrupt = false;
    //       sendtoServer(1, 0, 0);
    //     }
    //     spi_command = 0;
    //     if(colour_code == 1){
    //     Serial.println("Red has been detected");
    //     red_found = 1;
    //     }
    //     else if(colour_code == 2){
    //     Serial.println("Green has been detected");
    //     green_found = 1;
    //     }
    //     else if(colour_code == 3){
    //     Serial.println("Yellow has been detected");
    //     yellow_found = 1;
    //     }
    //     else if(colour_code == 4){
    //     Serial.println("Pink has been detected");
    //     pink_found = 1;
    //     }
    //     else if(colour_code == 5){
    //     Serial.println("Darkblue has been detected");
    //     darkblue_found = 1;
    //     }
    //     else if(colour_code == 6){
    //     Serial.println("Light green has been detected");
    //     lightgreen_found = 1;
    //     }
    //     else if(colour_code == 7){
    //     Serial.println("building has been detected");
    //     }
    //     response =colour_code;
    //     sent_dist =true;
    // }



//end of vision loop

//////////////////////////////////////////////////////////////////
////////Receiving new command list from the server...//////////////
  // Serial.println("checking for data from the server");
  if (!vision_interrupt & client.available())
  {
    // Serial.print("client available is high. number of bytes available is: ");
    // Serial.println(client.available());
    bytes_received = 0;
    while (client.available() && (bytes_received < 2)) {
      // Serial.println("received data from server: ");
      Commandchar = client.read(); //client.read() reads one character at a time
      // Serial.println(Commandchar);
      if(bytes_received == 0){
        client_msg = Commandchar << 8;
        // Serial.print("Halfway client message: ");
        // Serial.println(client_msg);
        bytes_received = 1;
      }
      else if(bytes_received == 1){
        client_msg += Commandchar;
        Serial.print("finished client message is: ");
        Serial.println(client_msg);
        opcode = client_msg >> 14;
        magnitude = client_msg & 16383;
        bytes_received = 2;
      }
    // Serial.print("received byte: ");
    // Serial.println(bytes_received);    
    }
    // Serial.print("Magnitude: ");
    // Serial.print(magnitude);
    //Angle
    // Serial.print("Opcode: ");
    // Serial.println(opcode);
    if(opcode==0){
        angle_t = magnitude;
        distance_t = total_y;
        angle_state = true;
        distance_state = false;
        angle_reached = 0;
        distance_reached = 0;
    }
    //Dista
    else if(opcode == 1){
        if(magnitude > 500){
          distance_t = total_y -(magnitude-500);
        }else{
          distance_t = total_y + magnitude;
        }
        angle_t = total_x;
        angle_state = false;
        distance_state = true;
        angle_reached = 0;
        distance_reached = 0;
        desired = total_x;
    }
  }
      if((total_y > distance_t + 1 | total_y < distance_t - 1) && distance_state){
        distance_reached = 0;
        error =  desired - total_x;
        // pathnow = millis();
//        ierror = error*(pathnow - pathstart) + ierror;
        if(error == 0){
          ierror = 0;
        }else{
          ierror = ierror+error;
        }
        // pathstart = millis();
        derror = error - derror;
        correction = multiplier*(error*pcoeff + ierror*icoeff + derror*dcoeff);
        if (total_y < distance_t-1){
          motor1_val = 43;
          motor2_val = 38;
          motor_offset = 3*angle_t - 3*total_x;
          robot.rotate(motor1, 44+correction, CW);//run motor1 at 60% speed in CW direction
          robot.rotate(motor2, 38-correction, CCW);//run motor1 at 60% speed in CW direction
        }
        if (total_y > distance_t + 1){
          motor1_val = 43;
          motor2_val = 38;
          motor_offset = 3*angle_t - 3*total_x;
          motor_offset = 3*angle_t - 3*total_x;
          robot.rotate(motor1, 44-correction, CCW);//run motor1 at 60% speed in CW direction
          robot.rotate(motor2, 38+correction, CW);//run motor1 at 60% speed in CW direction
        }
      }else if(distance_state){
        distance_reached = distance_reached + 1;
        //Serial.println("within range");
        //Serial.print("ideal y is: ");
        //Serial.println(distance_y);
        // Serial.print("total y is: ");
        // Serial.println(total_y);
        robot.brake(1);
        robot.brake(2);
        //0-360 is all positive
        //-360 to 0 : 361 is -1, 362 is -2
        if(distance_reached >= 3){
          distance_reached = 0;
          distance_state = false;
          sendtoServer(0, total_x, total_y); //POS sent to server
          delay(100);
          // Serial.println("line 707");
          sendtoServer(1, 0, 0); // UPM sent to server
        }
          angle_state = false;
      }  
     if((total_x % 360 > angle_t + 1 | total_x % 360 < angle_t - 1) && angle_state){
       angle_reached = 0;
       if (total_x % 360 < angle_t-1){
         robot.rotate(motor1, 30, CW);//run motor1 at 60% speed in CW direction
         robot.rotate(motor2, 30, CW);//run motor1 at 60% speed in CW direction
       }
       if (total_x % 360 > angle_t + 1){
        //  Serial.println("too close");
         Serial.print("ideal x is: ");
        Serial.println(angle_t);
         Serial.print("total x is: ");
          Serial.println(total_x);
         robot.rotate(motor1, 30, CCW);//run motor1 at 60% speed in CW direction
         robot.rotate(motor2, 30, CCW);//run motor1 at 60% speed in CW direction
       }
     }else if(angle_state){
       angle_reached = angle_reached + 1;
       //Serial.println("within range");
       //Serial.print("ideal x is: ");
       //Serial.println(angle_t);
       //Serial.print("total x is: ");
       //Serial.println(total_x);
       robot.brake(1);
       robot.brake(2);
     //0-360 is all positive
     //-360 to 0 : 361 is -1, 362 is -2
      if(angle_reached >= 3){
        angle_reached = 0;
        angle_state = false;   //RETURN LATER PLSSSSSS
        sendtoServer(0, total_x, total_y); //POS sent to server
        delay(100);
        sendtoServer(1, 0, 0); // UPM sent to server
      }
        distance_state = false;
     }  
// when the pins high, sendtoServer(3,0,0) <--- check exact name
// flag when found to turn off radar, make a variable which is a flag when told and !flag pin high radar in 
}