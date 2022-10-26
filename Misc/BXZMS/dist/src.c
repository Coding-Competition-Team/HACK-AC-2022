#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2);  // set the LCD address to 0x27 for a 16 chars and 2 line display

void scrollMessage(int row, String message, int delayTime, int totalColumns) {
  for (int i=0; i < totalColumns; i++) {
    message = " " + message;  
  } 
  message = message + " "; 
  for (int position = 0; position < message.length(); position=position+16) {
    lcd.setCursor(0, row);
    lcd.print(message.substring(position, position + totalColumns));
    delay(delayTime);
  }
}

void setup()
{
  lcd.init();                       // initialize the 16x2 lcd module
  lcd.backlight();                  // enable backlight for the LCD module
}

void loop()
{
  lcd.setCursor(0, 0);
  lcd.print("INCOMING MESSAGE");
  String msg = "[START] some_very_long_message_that_you_need_to_decode  [END]    ";
  scrollMessage(1, msg, 500, 16);
}