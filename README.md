# MPU-Sensor

ESP32 + MPU6050 tilt sensor, streamed over USB serial and visualized live on the desktop as a tilting horizon line.

## Hardware

ESP32-S3 DevKitC-1 + MPU6050 breakout, wired over I2C:

| MPU6050 pin | ESP32-S3 GPIO |
|---|---|
| VCC | 3V3 |
| GND | GND |
| SCL | 9 |
| SDA | 8 |

`XDA`, `XCL`, `INT` are left unconnected; `AD0` is left floating (keeps the I2C address at the default `0x68`).

## How it works

- **`mpu.ino`** — runs on the ESP32. Reads the MPU6050's accelerometer over I2C (raw register access, no external library), computes roll/pitch, and prints it as a JSON line over USB serial every 100ms:
  ```json
  {"roll":12.34,"pitch":-4.56}
  ```
- **`direction.py`** — runs on the Mac. Opens the serial port, reads those JSON lines, and draws a live tilting horizon line (plus a numeric roll/pitch readout) in a Tkinter window.

This is accelerometer-only tilt (no gyro fusion), so readings are a bit jittery and won't track fast rotation well — good enough to see live orientation, not a precision IMU.

## Setup

1. Flash `mpu.ino` to the ESP32 (Arduino IDE or `arduino-cli`, board: `esp32:esp32:esp32s3`).
2. Create a virtualenv and install the one dependency:
   ```
   python3 -m venv venv
   ./venv/bin/pip install pyserial
   ```
   On Homebrew Python you'll also need Tk support: `brew install python-tk@3.14` (or whatever version matches your `python3`).
3. Run the UI, pointing at your board's serial port:
   ```
   ./venv/bin/python3 direction.py /dev/cu.usbmodemXXXXXXXX
   ```
   (defaults to `/dev/cu.usbmodem5A7C1844271` if no port is given — check `ls /dev/cu.*` for yours).
