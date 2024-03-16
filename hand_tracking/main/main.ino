void setup() {
  Serial.begin(9600);
  Serial.println("Arduino initialized");
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    Serial.println("Received data: " + data);
    
    int commaIndex = data.indexOf(',');
    if (commaIndex != -1) {
      String x_str = data.substring(0, commaIndex);
      String y_str = data.substring(commaIndex + 1);

      int x = x_str.toInt();
      int y = y_str.toInt();

      Serial.print("Received coordinates: ");
      Serial.print(x);
      Serial.print(", ");
      Serial.println(y);
    } else {
      Serial.println("Invalid data format");
    }
  }
}
