// MPU6050 tilt sensor -> JSON over USB serial, read by direction.py on the Mac.
// No external MPU6050 library needed: raw I2C register reads via Wire.h.
//
// Wiring (I2C): SDA -> GPIO8, SCL -> GPIO9, VCC -> 3V3, GND -> GND.
// (Chosen to avoid the TFT pins already in use: 2,4,15,18,19,21.)

#include <Wire.h>

const int SDA_PIN = 8;
const int SCL_PIN = 9;
const uint8_t MPU_ADDR = 0x68;

void mpuWrite(uint8_t reg, uint8_t val) {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(reg);
  Wire.write(val);
  Wire.endTransmission();
}

int16_t read16(uint8_t reg) {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(reg);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDR, (uint8_t)2);
  int16_t hi = Wire.read();
  int16_t lo = Wire.read();
  return (hi << 8) | lo;
}

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("booting");
  Wire.begin(SDA_PIN, SCL_PIN);
  Serial.println("wire begin done");

  Wire.beginTransmission(MPU_ADDR);
  uint8_t err = Wire.endTransmission();
  Serial.print("i2c probe err=");
  Serial.println(err);   // 0 = ACK received, device present. nonzero = no response.

  mpuWrite(0x6B, 0x00);   // wake MPU6050 (clear sleep bit in PWR_MGMT_1)
  Serial.println("wake sent");
  delay(100);
}

void loop() {
  int16_t ax = read16(0x3B);
  int16_t ay = read16(0x3D);
  int16_t az = read16(0x3F);

  float axg = ax / 16384.0;
  float ayg = ay / 16384.0;
  float azg = az / 16384.0;

  float roll  = atan2(ayg, azg) * 180.0 / PI;
  float pitch = atan2(-axg, sqrt(ayg * ayg + azg * azg)) * 180.0 / PI;

  Serial.print("{\"roll\":");
  Serial.print(roll, 2);
  Serial.print(",\"pitch\":");
  Serial.print(pitch, 2);
  Serial.println("}");

  delay(100);
}
