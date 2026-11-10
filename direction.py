#!/usr/bin/env python3
"""Reads roll/pitch JSON lines from the ESP32 over USB serial and shows a live
terminal tilt indicator via curses. Run: python3 direction.py [serial_port]
Quit with 'q'.
"""
import curses
import json
import sys
import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "/dev/cu.usbmodem5A7C1844271"
BAUD = 115200

WIDTH = 41   # odd width so there's a true center column
HEIGHT = 11  # odd height so there's a true center row


def bar(value, lo, hi, width):
    value = max(lo, min(hi, value))
    pos = int((value - lo) / (hi - lo) * (width - 1))
    return "".join("#" if i == pos else "-" for i in range(width))


def draw(stdscr, roll, pitch):
    stdscr.erase()
    cy, cx = HEIGHT // 2, WIDTH // 2
    tilt_col = cx + int(roll / 90 * cx)
    tilt_col = max(0, min(WIDTH - 1, tilt_col))
    tilt_row = cy + int(pitch / 90 * cy)
    tilt_row = max(0, min(HEIGHT - 1, tilt_row))

    for r in range(HEIGHT):
        line = ["."] * WIDTH
        if r == cy:
            line = ["-"] * WIDTH
        if r == tilt_row:
            line[tilt_col] = "O"
        stdscr.addstr(r, 0, "".join(line))

    stdscr.addstr(HEIGHT + 1, 0, f"roll : {roll:+6.1f}  {bar(roll, -90, 90, 30)}")
    stdscr.addstr(HEIGHT + 2, 0, f"pitch: {pitch:+6.1f}  {bar(pitch, -90, 90, 30)}")
    stdscr.addstr(HEIGHT + 4, 0, "press 'q' to quit")
    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    ser = serial.Serial(PORT, BAUD, timeout=0.1)
    roll, pitch = 0.0, 0.0
    draw(stdscr, roll, pitch)
    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if line:
            try:
                data = json.loads(line)
                roll, pitch = data["roll"], data["pitch"]
            except (json.JSONDecodeError, KeyError):
                pass
            draw(stdscr, roll, pitch)
        try:
            if stdscr.getch() == ord("q"):
                break
        except curses.error:
            pass


if __name__ == "__main__":
    curses.wrapper(main)
