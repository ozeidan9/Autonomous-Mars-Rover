#include "SPI.h"

#include <Robojax_L298N_DC_motor.h>
#include "WiFi.h"

// these pins may be different on different boards
int motor1_val;
int motor2_val;
int motor_offset;
int angle_reached;
int distance_reached;
int client_msg;
int opcode;
int magnitude;
bool angle_or_distance; // angle is AMO, distance is DMO
int bytes_received;
float desired = 0; //this will need to be a dynamic input connected to various things so it allows multiple directions instead of just one forward
unsigned long pathstart;//this should only be called during the update to record the time it takes for this new direction change, so this entire program needs to be called new each time the rover changes direction


//strt
float pcoeff = 3;
float icoeff = 0.025;
float dcoeff = 3;
float multiplier = 1;

//
//float pcoeff = 3.4;
//float icoeff = 0.02;
//float dcoeff = 3;
//float multiplier = 1;
//end


float ierror = 0;
float derror = 0;



float camerax; //this will also need to be a dynamic input
float error;
unsigned long pathnow;

float correction;
bool distance_state = false;
bool angle_state = false;



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
char Commandchar;
const char* ssid = "ArduinoTest";//Wifi Name
const char* password = "pASSWORD";//Wifi password
const uint16_t port = 16000; //port number to connect to
//const char * host = "192.168.137.12"; //IP to connect to (can be private or public)
IPAddress remoteHost(192,168,137,162);
bool drivemsgready = false; //bool which checks whether drive's message is ready for sending
bool alreadyconnected = false; //bool which checks whether the ESP32 has already connected with the server
bool Commandready = false; //bool which checks whether command is ready for sending command
bool SPIready = false;
//Event for when the ESP32 successfully connects as a Wifi Station

///////
SPISettings settings(100000, MSBFIRST, SPI_MODE0);
SPIClass MySPI(HSPI);
uint8_t spi_counter[6]; // [0] = c20, [1] = c21, [2] = c22, [3] = c23, [4] = c24, [5] = c25
uint16_t spi_val;
uint8_t spi_reg;
uint16_t spi_returnval;
int spi_command;
int l;
int Command;
char angle_char;
//////
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



void control_turn(int target_angle){
  while(total_x > target_angle + 1 | total_x < target_angle - 1){
        while (total_x < target_angle-1){
          robot.rotate(motor1, 80, CW);//run motor1 at 60% speed in CW direction
          robot.rotate(motor2, 80, CW);//run motor1 at 60% speed in CW direction
        }
        robot.brake(1);
        robot.brake(2);
        delay(300);
        while (total_x > target_angle + 1){
          robot.rotate(motor1, 80, CCW);//run motor1 at 60% speed in CW direction
          robot.rotate(motor2, 80, CCW);//run motor1 at 60% speed in CW direction
        }
        robot.brake(1);
        robot.brake(2);
        delay(300);
      }
}



void control_drive(int target_distance){
      Serial.println("started control drive loop");
      while(total_y > target_distance + 1 | total_y < target_distance - 1){
        Serial.println("not within range");
        while (total_y < target_distance-1){
          Serial.print("total y is: ");
          Serial.println(total_y);
          robot.rotate(motor1, 85, CW);//run motor1 at 60% speed in CW direction
          robot.rotate(motor2, 77, CCW);//run motor1 at 60% speed in CW direction
        }
        robot.brake(1);
        robot.brake(2);
        delay(300);
        while (total_y > target_distance + 1){
          Serial.println("too close");
          robot.rotate(motor1, 85, CCW);//run motor1 at 60% speed in CW direction
          robot.rotate(motor2, 77, CW);//run motor1 at 60% speed in CW direction
        }
        robot.brake(1);
        robot.brake(2);
        delay(300);
      }
      Serial.println("ended control drive loop");
}


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

  for(;;){

//    Serial.print("Opticaltaskcode running in core: ");
//    Serial.println(xPortGetCoreID());

  
    #if 0
    /*
        if(movementflag){

        tdistance = tdistance + convTwosComp(xydat[0]);
        Serial.println("Distance = " + String(tdistance));
        movementflag=0;
        delay(3);
        }

    */
    // if enabled this section grabs frames and outputs them as ascii art

    if (mousecam_frame_capture(frame) == 0)
    {
      int i, j, k;
      for (i = 0, k = 0; i < ADNS3080_PIXELS_Y; i++)
      {
        for (j = 0; j < ADNS3080_PIXELS_X; j++, k++)
        {
          Serial.print(asciiart(frame[k]));
          Serial.print(' ');
        }
        Serial.println();
      }
    }
    Serial.println();

  #else

    // if enabled this section produces a bar graph of the surface quality that can be used to focus the camera
    // also drawn is the average pixel value 0-63 and the shutter speed and the motion dx,dy.

    int val = mousecam_read_reg(ADNS3080_PIXEL_SUM);
    MD md;
    mousecam_read_motion(&md);
//    for (int i = 0; i < md.squal / 4; i++)
//      Serial.print('*');
//    Serial.print(' ');
//    Serial.print((val * 100) / 351);
//    Serial.print(' ');
//    Serial.print(md.shutter); Serial.print(" (");
//    Serial.print((int)md.dx); Serial.print(',');
//    Serial.print((int)md.dy); Serial.println(')');

    // Serial.println(md.max_pix);


    distance_x = convTwosComp(md.dx);
    distance_y = convTwosComp(md.dy);

    total_x1 = total_x1 + distance_x;
    total_y1 = total_y1 + distance_y;

    total_x = total_x1 * 0.0840;   //callibrated;
    total_y = total_y1 * 0.0193;  //callibrated;


//    Serial.print('\n');

//
//    Serial.println("Distance_x = " + String(total_x));
//
//    Serial.println("Distance_y = " + String(total_y));
//    Serial.print('\n');

  #endif

  }
}

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


void setup()
{
  Serial.begin(9600);

 //Drive SPI setup
  pinMode(PIN_SS, OUTPUT);
  pinMode(PIN_MISO, INPUT);
  pinMode(PIN_MOSI, OUTPUT);
  pinMode(PIN_SCK, OUTPUT);


  robot.begin();

  xTaskCreatePinnedToCore(
    Opticaltaskcode,
    "Optical_task",
    10000, //stack size in words
    NULL,  // input paramter to task
    0, //priority of task
    &Optical_task,
    0); //Core 0

  distance_t = 50;
  delay(4000);


  initWiFi();

  if(!client.connect(remoteHost, 15000)){
    while(!client.connect(remoteHost, 15000)){
    Serial.println("not connected");
    }
  }
  
  Serial.println("Connected to server");



}

char asciiart(int k)
{
  static char foo[] = "WX86*3I>!;~:,`. ";
  return foo[k >> 4];
}


void loop()
{
  
  
    client.write("POS");
    delay(250); //tell james to update his
    client.write(x);
    delay(250);
    client.write(y);


  Serial.println("checking for data from the server");
  if (client.available())
  {
    Serial.println("received data from server: ");
    bytes_received = 0;
    while (client.available()) {
      Commandchar = client.read(); //client.read() reads one character at a time
      Serial.println(Commandchar);
      if(bytes_received == 0){
        client_msg = Commandchar << 8;
        bytes_received = 1;
      }
      if(bytes_received == 1){
        client_msg += Commandchar;
        opcode = client_msg >> 14;
        magnitude = client_msg & 16383;
        bytes_received = 0;
      }
      if (Commandchar) {
        Serial.println("The Command has been recorded");
        Commandready = true;
        break;
      }
    
    }
  }
  if(!distance_state & !angle_state){
    client.write("UPM");
  }
   Serial.println("Enter Command");
   if(Serial.available()){
      Serial.println("got reply!");
      String Commandstr = Serial.readString();
      
      int Comm = Commandstr.toInt();//convert char to int to pass into function -> 10001111: 15 -> 143(dec)
      distance_t = Comm;
      Serial.print("distance_t is:");
      Serial.println(distance_t);
      unsigned long pathstart = millis(); 

      //int value = Comm & 127;
      //bool negative_number = Comm >> 7;
      //Serial.print("negative_number:");
      //Serial.println(negative_number);

      //Serial.print("value:");
      //Serial.println(value);
      //if(negative_number){
           //control_drive(value);
           //control_drive(value);
      
      }


    if(opcode==0){
        while (client.available()) {
            // angle_t = client.read(); //client.read() reads one character at a time
            angle_t = magnitude;
            Serial.println(angle_t);
        }
        angle_state = true;
        angle_reached = 0;
        distance_reached = 0;
    }


    if(opcode==1){
        while (client.available()) {
            distance_t = magnitude; //client.read() reads one character at a time
            Serial.println(distance_t);
        }

        distance_state = true;
        angle_reached = 0;
        distance_reached = 0;

      }
      if(total_y > distance_t + 1 | total_y < distance_t - 1 && distance_state){
        distance_reached = 0;
        camerax = total_x; //this will also need to be a dynamic input
        error = desired - camerax;
        pathnow = millis();
//        ierror = error*(pathnow - pathstart) + ierror;
        if(error == 0){
          ierror = 0;
        }else{
          ierror = ierror+error;
        }
        pathstart = millis();
        derror = error - derror;
        correction = multiplier*(error*pcoeff + ierror*icoeff + derror*dcoeff);
  

        Serial.println("not within range");
        if (total_y < distance_t-1){
          Serial.println("too far");
          Serial.print("ideal y is: ");
          Serial.println(distance_t);
          
          Serial.print("total y is: ");
          Serial.println(total_y);
          motor1_val = 43;
          motor2_val = 38;
          motor_offset = 3*angle_t - 3*total_x;
          Serial.print("offset is: ");
          Serial.println(motor_offset);
          robot.rotate(motor1, 43-correction, CW);//run motor1 at 60% speed in CW direction
          robot.rotate(motor2, 38+correction, CCW);//run motor1 at 60% speed in CW direction
        }
    
        if (total_y > distance_t + 1){
          Serial.println("too close");
          Serial.print("ideal y is: ");
          Serial.println(distance_t);
          
          Serial.print("total y is: ");
          Serial.println(total_y);
          motor1_val = 43;
          motor2_val = 38;
          motor_offset = 3*angle_t - 3*total_x;
          Serial.print("offset is: ");
          Serial.println(motor_offset);
          motor_offset = 3*angle_t - 3*total_x;
          
          robot.rotate(motor1, 42-correction, CCW);//run motor1 at 60% speed in CW direction
          robot.rotate(motor2, 37+correction, CW);//run motor1 at 60% speed in CW direction
        }
      }else{
        distance_reached = distance_reached + 1;
        Serial.println("within range");
        Serial.print("ideal y is: ");
        Serial.println(distance_y);
          
        Serial.print("total y is: ");
        Serial.println(total_y);
        robot.brake(1);
        robot.brake(2);
      //0-360 is all positive
      //-360 to 0 : 361 is -1, 362 is -2

        if(distance_reached >= 3){
          distance_reached = 0;
          distance_state = false;
          client.write("UPM");
        }
        
      }  



     if(total_x > angle_t + 1 | total_x < angle_t - 1 && angle_state){
       angle_reached = 0;
       Serial.println("not within range");
       if (total_x < angle_t-1){
         Serial.println("too far");
         Serial.print("ideal x is: ");
         Serial.println(angle_t);
         
         Serial.print("total x is: ");
         Serial.println(total_x);
         robot.rotate(motor1, 30, CCW);//run motor1 at 60% speed in CW direction
         robot.rotate(motor2, 30, CCW);//run motor1 at 60% speed in CW direction
       }
   
       if (total_x > angle_t + 1){
         Serial.println("too close");
         Serial.print("ideal x is: ");
         Serial.println(angle_t);
         
         Serial.print("total x is: ");
         Serial.println(total_x);
         robot.rotate(motor1, 30, CW);//run motor1 at 60% speed in CW direction
         robot.rotate(motor2, 30, CW);//run motor1 at 60% speed in CW direction
       }
     }else{
       angle_reached = angle_reached + 1;
       Serial.println("within range");
       Serial.print("ideal x is: ");
       Serial.println(angle_t);
         
       Serial.print("total x is: ");
       Serial.println(total_x);
       robot.brake(1);
       robot.brake(2);
     //0-360 is all positive
     //-360 to 0 : 361 is -1, 362 is -2
      if(angle_reached >= 3){
        angle_reached = 0;
        angle_state = false;
        client.write("UPM");
      }
       

     
     }  



      
   
  

      
      

}