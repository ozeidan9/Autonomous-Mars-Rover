


#include "SPI.h"

#include <Robojax_L298N_DC_motor.h>
#include "WiFi.h"

// these pins may be different on different boards

#define PIN_SS        5
#define PIN_MISO      19
#define PIN_MOSI      23
#define PIN_SCK       18

#define PIN_MOUSECAM_RESET     35
#define PIN_MOUSECAM_CS        5

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
// TehCehPeh
#define RXP2 3
#define TXP2 1
// DRIVE
// motor 1 settings
#define CHA 0
#define ENA 2 // this pin must be PWM enabled pin if Arduino board is used D13 -> was 2
#define IN1 4 //D11
#define IN2 22 //D3 - was 15 (D12)
// motor 2 settings
#define IN3 21 //D4 //was 14  (D10)
#define IN4 16 //D9
#define ENB 17// this pin must be PWM enabled pin if Arduino board is used D8
#define CHB 1
const int CCW = 2; // do not change
const int CW  = 1; // do not change
#define motor1 1 // do not change
#define motor2 2 // do not change
// for two motors without debug information // Watch video instruciton for this line: https://youtu.be/2JTMqURJTwg
Robojax_L298N_DC_motor robot(IN1, IN2, ENA, CHA,  IN3, IN4, ENB, CHB);
// for two motors with debug information
//Robojax_L298N_DC_motor robot(IN1, IN2, ENA, CHA, IN3, IN4, ENB, CHB, true);
char DriveMap[32]; //storage for drive's message
char Command[32]; //storage for the actual command
char Commandchar;
const char* ssid = "AndroidAP5c48";//Wifi Name
const char* password = "janq9636";//Wifi password
const uint16_t port = 16000; //port number to connect to
const char * host = "192.168.43.192"; //IP to connect to (can be private or public)
bool drivemsgready = false; //bool which checks whether drive's message is ready for sending
bool alreadyconnected = false; //bool which checks whether the ESP32 has already connected with the server
bool commandready = false; //bool which checks whether command is ready for sending command
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

void Drivle(int i) {
  Serial.println("In drivle fn, i is: ");
  Serial.println(i);

 
  switch (i) {
    case 49:
      // move straight for 3 sec
      robot.rotate(motor1, 80, CW);//run motor1 at 60% speed in CW direction
      robot.rotate(motor2, 80, CCW);//run motor1 at 60% speed in CW direction
      Serial.println("rotated 1");
      delay(1000);
      robot.brake(1);
      robot.brake(2);
      delay(50);
      break;
    case 50:
      // rotate left for 3 sec
      robot.rotate(motor1, 80, CCW);//run motor1 at 60% speed in CW direction
      robot.rotate(motor2, 80, CCW);//run motor1 at 60% speed in CW direction
      Serial.println("rotated 2");

      delay(1000);
      robot.brake(1);
      robot.brake(2);
      delay(50);
      break;
    case 51:
      // rotate right for 3 sec
      robot.rotate(motor1, 80, CW);//run motor1 at 60% speed in CW direction
      robot.rotate(motor2, 80, CW);//run motor1 at 60% speed in CW direction
      Serial.println("rotated 3");

      delay(1000);
      robot.brake(1);
      robot.brake(2);
      delay(50);
      break;
    case 52:
      // move back for 3 sec
      robot.rotate(motor1, 85, CCW);//run motor1 at 60% speed in CW direction
      robot.rotate(motor2, 77, CW);//run motor1 at 60% speed in CW direction
      Serial.println("rotated 4");

      delay(2000);
      robot.brake(1);
      robot.brake(2);
      delay(50);
      break;
    case 53:
      while (i == 53) {
        //continuous case forward
        robot.rotate(motor1, 80, CW);//run motor1 at 60% speed in CW direction
        robot.rotate(motor2, 80, CCW);//run motor1 at 60% speed in CW direction
        Serial.println("rotated 5");

        delay(10);
        //Serial.println("We are a go");
        i = Serial.parseInt();
      }
      break;
    case 54:
      while (i == 54) {
        //continuous case left
        robot.rotate(motor1, 80, CCW);//run motor1 at 60% speed in CW direction
        robot.rotate(motor2, 80, CCW);//run motor1 at 60% speed in CW direction
        Serial.println("rotated 6");

        delay(10);
        i = Serial.parseInt();
      }
      break;
    case 55:
      while (i == 55) {
        //continuous case right
        robot.rotate(motor1, 80, CW);//run motor1 at 60% speed in CW direction
        robot.rotate(motor2, 80, CW);//run motor1 at 60% speed in CW direction
        Serial.println("rotated 7");

        delay(10);
        i = Serial.parseInt();
      }
      break;
    case 56:
      while (i == 56) {
        //continuous case back
        robot.rotate(motor1, 90, CCW);//run motor1 at 60% speed in CW direction .  //was 80
        robot.rotate(motor2, 75, CW);//run motor1 at 60% speed in CW direction
        Serial.println("rotated 8");

        delay(10);
        i = Serial.parseInt();
      }
      break;
    case 57:
      while (i == 57) {
        //adjust to the left
        robot.rotate(motor1, 75, CCW);//run motor1 at 60% speed in CCW direction
        robot.rotate(motor2, 80, CW);//run motor1 at 60% speed in CW direction
        Serial.println("rotated 9");

        delay(10);
        i = Serial.parseInt();
      }
      break;
    case 58:
      while (i == 58) {
        //adjust to the right
        robot.rotate(motor1, 80, CCW);//run motor1 at 60% speed in CCW direction
        robot.rotate(motor2, 75, CW);//run motor1 at 60% speed in CW direction
        delay(10);
        i = Serial.parseInt();
      }
      break;
    default:
      // brake
      robot.brake(1);
      robot.brake(2);
      delay(10);
      //Serial.println("We are a go0");
      break;
  }
}

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


int convTwosComp(int b) {
  //Convert from 2's complement
  if (b & 0x80) {
    b = -1 * ((b ^ 0xff) + 1);
  }
  return b;
}


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

struct MD
{
  byte motion;
  char dx, dy;
  byte squal;
  word shutter;
  byte max_pix;
};


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
  pinMode(PIN_SS, OUTPUT);
  pinMode(PIN_MISO, INPUT);
  pinMode(PIN_MOSI, OUTPUT);
  pinMode(PIN_SCK, OUTPUT);

  SPI.begin();
  SPI.setClockDivider(SPI_CLOCK_DIV32);
  SPI.setDataMode(SPI_MODE3);
  SPI.setBitOrder(MSBFIRST);

  Serial.begin(9600);


  if (mousecam_init() == -1)
  {
    Serial.println("Mouse cam failed to init");
    while (1);
  }

  robot.begin();
  
  SPI.begin(); // init SPI bus

  WiFi.disconnect(true);
  delay(1000);

  initWiFi();
}

char asciiart(int k)
{
  static char foo[] = "WX86*3I>!;~:,`. ";
  return foo[k >> 4];
}

byte frame[ADNS3080_PIXELS_X * ADNS3080_PIXELS_Y];

void loop()
{

  if (!alreadyconnected) {  //Attempts to connect to Server using provided Host and Port
    if (!client.connect(host, port)) {
      Serial.println("Connection to host failed");
      delay(100);
      return;
    }
    Serial.println("Connected to server!");
    client.print("Hello from Control!");
    alreadyconnected = true;
  }


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
  delay(250);

#else

  // if enabled this section produces a bar graph of the surface quality that can be used to focus the camera
  // also drawn is the average pixel value 0-63 and the shutter speed and the motion dx,dy.

  int val = mousecam_read_reg(ADNS3080_PIXEL_SUM);
  MD md;
  mousecam_read_motion(&md);
  for (int i = 0; i < md.squal / 4; i++)
    Serial.print('*');
  Serial.print(' ');
  Serial.print((val * 100) / 351);
  Serial.print(' ');
  Serial.print(md.shutter); Serial.print(" (");
  Serial.print((int)md.dx); Serial.print(',');
  Serial.print((int)md.dy); Serial.println(')');

  // Serial.println(md.max_pix);
  delay(100);


  distance_x = convTwosComp(md.dx);
  distance_y = convTwosComp(md.dy);

  total_x1 = total_x1 + distance_x;
  total_y1 = total_y1 + distance_y;

  total_x = total_x1 ;   //to be callibrated;
  total_y = total_y1 * 0.0224;  //callibrated;


  Serial.print('\n');

  client.write("POS");
  delay(1000);
  client.write(total_x);
  delay(1000);
  client.write(total_y);


  Serial.println("Distance_x = " + String(total_x));

  Serial.println("Distance_y = " + String(total_y));
  Serial.print('\n');

  delay(250);

#endif
  Serial.println("hi sent");

  Serial.println("checking for data from the client");
  if (client.available())
  {
    Serial.println("received data from client: ");

    while (client.available()) {
      Commandchar = client.read(); //client.read() reads one character at a time
      Serial.println(Commandchar);

      if (Commandchar) {
        Serial.println("The Command has been recorded");
        commandready = true;
        drivemsgready = true; //added for now here
        break;
      }
    
    }
  }

  //Checks if drive and command are rea

  if (drivemsgready && commandready) {
]   Serial.println("Sending command to drive: ");
    int Command = Commandchar;
    Drivle(Command);
    Serial.println("sent command");


    commandready = false;
    drivemsgready = false;

  }

  delay(500);






}