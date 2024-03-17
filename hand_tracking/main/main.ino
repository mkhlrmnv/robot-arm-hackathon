#include "OLED_Driver.h"
#include "GUI_paint.h"
#include "DEV_Config.h"
#include "Debug.h"
#include "ImageData.h"

String cmd;
int i = 100;

void setup() {
  System_Init();
  Serial.print(F("OLED_Init()...\r\n"));
  OLED_1in5_Init();
  Driver_Delay_ms(500); 
  OLED_1in5_Clear();  
  
  //0.Create a new image cache
  UBYTE *BlackImage;
  UWORD Imagesize = ((OLED_1in5_WIDTH%2==0)? (OLED_1in5_WIDTH/2): (OLED_1in5_WIDTH/2+1)) * OLED_1in5_HEIGHT;
  if((BlackImage = (UBYTE *)malloc(Imagesize/8)) == NULL) { //No enough memory
      Serial.print("Failed to apply for black memory...\r\n");
      return -1;
  }
  Serial.print("Paint_NewImage\r\n");
  Paint_NewImage(BlackImage, OLED_1in5_WIDTH/4, OLED_1in5_HEIGHT/2, 270, BLACK);  
  Paint_SetScale(16);

  //1.Select Image
  Paint_SelectImage(BlackImage);
  Paint_Clear(BLACK);
  Driver_Delay_ms(500); 

while (1) {
    i++;

    while (Serial.available() == 0){
    }
    cmd = Serial.readStringUntil('\r');

    Serial.print("Received command: ");
    Serial.println(cmd);

    char* token = strtok(cmd.c_str(), ";"); // Get the first token
    int x = atoi(token); // Convert token to float for x

    token = strtok(NULL, ";"); // Get the second token
    int y = atoi(token); // Convert token to float for y

    token = strtok(NULL, ";"); // Get the third token
    int open = atoi(token); // Convert token to float for open

    Paint_ClearWindows(10, 0, 64, 30, BLACK);
    OLED_1in5_Clear(); 

    char numberString[20]; // Increased size to accommodate larger numbers
    snprintf(numberString, sizeof(numberString), "x: %d", x); // Format x value as float with 2 decimal places

    char numberString2[20]; // Increased size to accommodate larger numbers
    snprintf(numberString2, sizeof(numberString2), "y: %d", y); // Format y value as float with 2 decimal places

    char numberString3[20]; // Increased size to accommodate larger numbers
    snprintf(numberString3, sizeof(numberString3), "z: %d", open); // Format open value as float with 2 decimal places
    
    Paint_DrawString_EN(10, 0, numberString, &Font12, WHITE, WHITE);
    Paint_DrawString_EN(10, 10, numberString2, &Font12, WHITE, WHITE);
    Paint_DrawString_EN(10, 20, numberString3, &Font12, WHITE, WHITE);
    OLED_1in5_Display_Part(BlackImage, 0, 0, 32, 64); 

    Driver_Delay_ms(100);  
    
    // OLED_1in5_Clear();  
  }   
}

void loop() {

}