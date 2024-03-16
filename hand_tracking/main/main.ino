#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH1107.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 128 // OLED display height, in pixels

Adafruit_SH1107 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

void setup() {
  Serial.begin(9600);
  if (!display.begin(SH1107_ADDR_DEFAULT, SCREEN_HEIGHT)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;);
  }
  delay(2000);
  display.clearDisplay();
}

void loop() {
  display.clearDisplay();
  for (int i = 0; i <= 1000; i++) {
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);
    display.print("Count: ");
    display.println(i);
    display.display();
    delay(500); // Adjust delay as needed
  }
}