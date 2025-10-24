#!/usr/bin/env python3
"""Debug script to test mouse events in curses."""

import curses
import time

def main(stdscr):
    """Test mouse event handling."""
    # Enable mouse events
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)

    # Set up screen
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()
    stdscr.nodelay(True)  # Non-blocking

    # Display instructions
    stdscr.addstr(0, 0, "Mouse Event Debug - Click anywhere to see coordinates")
    stdscr.addstr(1, 0, "Press 'q' to quit")
    stdscr.addstr(3, 0, "Sample text with breakpoint indicator:")
    stdscr.addstr(4, 0, "●10 PRINT \"Line 10\"")
    stdscr.addstr(5, 0, " 20 PRINT \"Line 20\"")
    stdscr.addstr(6, 0, "●30 PRINT \"Line 30\"")
    stdscr.addstr(7, 0, " 40 PRINT \"Line 40\"")
    stdscr.addstr(9, 0, "Click on the ● character to test")
    stdscr.refresh()

    event_count = 0
    while True:
        try:
            ch = stdscr.getch()

            if ch == ord('q') or ch == ord('Q'):
                break
            elif ch == curses.KEY_MOUSE:
                try:
                    mouse_id, mouse_x, mouse_y, mouse_z, bstate = curses.getmouse()
                    event_count += 1

                    # Clear event display area
                    for i in range(11, 20):
                        stdscr.move(i, 0)
                        stdscr.clrtoeol()

                    # Display mouse event details
                    stdscr.addstr(11, 0, f"Event #{event_count}:")
                    stdscr.addstr(12, 0, f"  Position: x={mouse_x}, y={mouse_y}")
                    stdscr.addstr(13, 0, f"  Button state: {bstate}")

                    if bstate & curses.BUTTON1_CLICKED:
                        stdscr.addstr(14, 0, "  Type: BUTTON1_CLICKED")
                    elif bstate & curses.BUTTON1_PRESSED:
                        stdscr.addstr(14, 0, "  Type: BUTTON1_PRESSED")
                    elif bstate & curses.BUTTON1_RELEASED:
                        stdscr.addstr(14, 0, "  Type: BUTTON1_RELEASED")

                    # Check if clicked on breakpoint column (x=0 or x=1)
                    if 4 <= mouse_y <= 7 and mouse_x <= 1:
                        stdscr.addstr(15, 0, "  *** Clicked on breakpoint column! ***", curses.A_BOLD)
                        # Toggle the ● character
                        line_char = chr(stdscr.inch(mouse_y, 0) & 0xFF)
                        if line_char == '●':
                            stdscr.addstr(mouse_y, 0, ' ')
                        else:
                            stdscr.addstr(mouse_y, 0, '●')

                    stdscr.refresh()
                except Exception as e:
                    stdscr.addstr(16, 0, f"Error processing mouse: {e}")
                    stdscr.refresh()

            time.sleep(0.01)
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    curses.wrapper(main)
