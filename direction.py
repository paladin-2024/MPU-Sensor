#!/usr/bin/env python3
"""Reads roll/pitch JSON lines from the ESP32 over USB serial and draws a tilting
horizon line in a Tkinter window. Run: python3 direction.py [serial_port]
"""
import json
import sys
import tkinter as tk
import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/cu.usbmodem5A7C1844271"
BAUD = 115200
SIZE = 400

ser = serial.Serial(PORT, BAUD, timeout=1)

root = tk.Tk()
root.title("Direction")
canvas = tk.Canvas(root, width=SIZE, height=SIZE, bg="black")
canvas.pack()
label = tk.Label(root, text="", font=("Menlo", 14))
label.pack()

horizon = canvas.create_line(0, 0, 0, 0, fill="lime", width=4)
center_dot = canvas.create_oval(SIZE / 2 - 3, SIZE / 2 - 3, SIZE / 2 + 3, SIZE / 2 + 3, fill="red")


def draw(roll_deg, pitch_deg):
    import math
    cx, cy = SIZE / 2, SIZE / 2 - pitch_deg * 2   # pitch shifts horizon up/down
    rad = math.radians(roll_deg)
    length = SIZE
    dx = math.cos(rad) * length / 2
    dy = math.sin(rad) * length / 2
    canvas.coords(horizon, cx - dx, cy - dy, cx + dx, cy + dy)
    label.config(text=f"roll: {roll_deg:+.1f}   pitch: {pitch_deg:+.1f}")


def poll():
    line = ser.readline().decode(errors="ignore").strip()
    if line:
        try:
            data = json.loads(line)
            draw(data["roll"], data["pitch"])
        except (json.JSONDecodeError, KeyError):
            pass
    root.after(20, poll)


poll()
root.mainloop()
