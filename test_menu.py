#!/usr/bin/env python3
"""
Simple test to check if menu windows are being created and drawn correctly.
"""
import curses
import time

def test_menu(stdscr):
    curses.curs_set(0)

    # Initialize colors
    if curses.has_colors():
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)

    height, width = stdscr.getmaxyx()

    # Create menu window at top
    menu_win = curses.newwin(1, width, 0, 0)

    # Create editor window below menu
    editor_win = curses.newwin(height - 2, width, 1, 0)

    # Create status at bottom
    status_win = curses.newwin(1, width, height - 1, 0)

    # Clear main screen
    stdscr.clear()
    stdscr.noutrefresh()

    # Draw menu
    menu_win.clear()
    if curses.has_colors():
        menu_win.bkgd(' ', curses.color_pair(1))
    menu_win.addstr(0, 0, ' ' * (width - 1))
    menu_win.addstr(0, 1, ' File ', curses.A_REVERSE)
    menu_win.addstr(0, 8, ' Edit ')
    menu_win.addstr(0, 15, ' Run ')
    menu_win.addstr(0, 21, ' Help ')
    menu_win.noutrefresh()

    # Draw editor
    editor_win.clear()
    editor_win.addstr(0, 0, "Editor area")
    editor_win.noutrefresh()

    # Draw status
    status_win.clear()
    if curses.has_colors():
        status_win.bkgd(' ', curses.color_pair(1))
    status_win.addstr(0, 0, "Press any key to test dropdown, q to quit")
    status_win.noutrefresh()

    # Update screen
    curses.doupdate()

    # Wait for key
    key = stdscr.getch()

    if key != ord('q'):
        # Draw dropdown
        dropdown = curses.newwin(6, 15, 1, 1)
        dropdown.box()
        dropdown.addstr(1, 1, " New       ", curses.A_REVERSE)
        dropdown.addstr(2, 1, " Load...   ")
        dropdown.addstr(3, 1, " Save...   ")
        dropdown.addstr(4, 1, " Quit      ")
        dropdown.noutrefresh()

        status_win.clear()
        if curses.has_colors():
            status_win.bkgd(' ', curses.color_pair(1))
        status_win.addstr(0, 0, "Dropdown should be visible. Press q to quit")
        status_win.noutrefresh()

        curses.doupdate()

        # Wait for quit
        while stdscr.getch() != ord('q'):
            pass

if __name__ == '__main__':
    curses.wrapper(test_menu)
