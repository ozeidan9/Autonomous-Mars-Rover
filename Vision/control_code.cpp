// comms:
// ball d1etected ->  -> rover needs to stop
// when ball detected -> r_ball_distance -> send this to command
// when too far left -> 9
// when too far right -> 10
// when too close -> 8
// when too far -> 5
// just right (don't move) -> 0
// when done -> 2


// #include <SPI.h>
// #include <Arduino.h>
// #define VSPI_MISO   MISO
// #define VSPI_MOSI   MOSI
// #define VSPI_SCLK   SCK
// #define VSPI_SS     SS


// #define VSPI_MISO   MISO
// #define VSPI_MOShspiI   MOSI
// #define VSPI_SCLK   SCK
// #define VSPI_SS     SS

// //Changing the VPSI to HSPI because drive is using the VSPI

// SPISettings settings(100000, MSBFIRST, SPI_MODE0);

// uint8_t spi_counter[6]; // [0] = c20, [1] = c21, [2] = c22, [3] = c23, [4] = c24, [5] = c25
// uint16_t spi_val;
// uint8_t spi_reg;
// uint16_t spi_returnval;
// void resetCounter();
// int l;
// //vspi default pins SCLK = 18, MISO = 19, MOSI = 23, SS = 5 
// void setup() {
//   l = 1;
//   Serial.begin(115200);

//   pinMode(VSPI_SS, OUTPUT);
//   SPI.begin();
//   resetCounter();
//   spi_returnval = 0;
// }

// void loop() {

//     // Transfer stuff


//     //run this to receive data (l can be any input)
//     SPI.beginTransaction(settings);
//     digitalWrite(VSPI_SS, LOW);
//     spi_val = SPI.transfer16(l); // spi_val is the message you revceive
//     spi_returnval = 0;
//     digitalWrite(VSPI_SS, HIGH);
//     SPI.endTransaction();
//     //run block



//     Serial.print("start of data, having sent: ");
//     Serial.println(l);
//     Serial.println(spi_val);
//     Serial.println("end of data");
//     if(l >= 7){
//       l = 1;
//     }else{
//       l = l + 1;
//     }
//     delay(1000);
// }


#include <SPI.h>
#include <Arduino.h>

#define HSPI_MISO 4
#define HSPI_MOSI 22
#define HSPI_SCLK 14
#define HSPI_CS   15

//HSPI ports SCLK = 14 MISO = 4 MOSI = 22 SS = 15
//vspi pins SCLK = 18, MISO = 19, MOSI = 23, SS = 5 

//Changing the VPSI to HSPI because drive is using the VSPI

uint8_t spi_counter[6]; // [0] = c20, [1] = c21, [2] = c22, [3] = c23, [4] = c24, [5] = c25
uint16_t spi_val;
uint8_t spi_reg;
uint16_t spi_returnval;
void resetCounter();
int l;
SPISettings settings(100000, MSBFIRST, SPI_MODE0);
//vspi default pins SCLK = 18, MISO = 19, MOSI = 23, SS = 5 
void setup() {
  l = 1;
  Serial.begin(115200);

  pinMode(HSPI_CS, OUTPUT);
  SPI.begin();
  SPIClass hspi(HSPI);
  // hspi.begin(HSPI_SCLK, HSPI_MISO, HSPI_MOSI, HSPI_CS); //SCLK, MISO, MOSI, SS
  resetCounter();
  spi_returnval = 0;
}

void loop() {

    // Transfer stuff


    //run this to receive data (l can be any input)
    SPI.beginTransaction(settings);
    digitalWrite(HSPI_CS, LOW);
    spi_val = SPI.transfer16(l); // spi_val is the message you revceive
    spi_returnval = 0;
    digitalWrite(HSPI_CS, HIGH);
    SPI.endTransaction();
    //run block



    Serial.print("start of data, having sent: ");
    Serial.println(l);
    Serial.println(spi_val);
    Serial.println("end of data");
    if(l >= 7){
      l = 1;
    }else{
      l = l + 1;
    }
    delay(1000);
}