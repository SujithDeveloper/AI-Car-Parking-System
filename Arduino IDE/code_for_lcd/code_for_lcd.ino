#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 1);
  lcd.begin(16, 2);
  

}

void loop() {
  lcd.setCursor(0, 0);
  lcd.print(" Welcome: ");
  delay(500);
  lcd.setCursor(0, 1);
  lcd.print(" GuyZzz... ");

}
