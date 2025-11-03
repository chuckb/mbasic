"""Keymap display widget showing all keyboard shortcuts."""

import urwid
from .keybindings import KEYBINDINGS_BY_CATEGORY


class KeymapWidget(urwid.WidgetWrap):
    """Display all keyboard shortcuts in a scrollable window."""

    def __init__(self, on_close):
        """Initialize the keymap display.

        Args:
            on_close: Callback function when user closes the window
        """
        self.on_close = on_close

        # Build the keymap content
        content = self._build_keymap_content()

        # Create scrollable listbox
        self.listwalker = urwid.SimpleFocusListWalker(content)
        self.listbox = urwid.ListBox(self.listwalker)

        # Add title and borders
        title = urwid.Text(('title', 'Keyboard Shortcuts'), align='center')
        instructions = urwid.Text(
            "↑/↓ scroll  ESC/Q close",
            align='center'
        )

        # Build the layout
        pile = urwid.Pile([
            ('pack', urwid.AttrMap(title, 'title')),
            ('pack', urwid.Divider('─')),
            ('pack', urwid.AttrMap(instructions, 'help_text')),
            ('pack', urwid.Divider()),
            self.listbox,
        ])

        # Wrap in line box with black background
        linebox = urwid.LineBox(
            urwid.AttrMap(pile, 'body')
        )

        super().__init__(urwid.AttrMap(linebox, 'body'))

    def _build_keymap_content(self):
        """Build the keymap content from keybindings.

        Returns:
            List of urwid widgets for display
        """
        content = []

        for category, bindings in KEYBINDINGS_BY_CATEGORY.items():
            # Add category header
            content.append(
                urwid.AttrMap(
                    urwid.Text(('category', f'\n{category}')),
                    'category'
                )
            )
            content.append(urwid.Divider())

            # Add keybindings in this category
            for key, description in bindings:
                # Format: "  Key         Description"
                # Use 16 chars for key column for alignment
                line = f"  {key:<16} {description}"
                content.append(
                    urwid.Text(line)
                )

        return content

    def keypress(self, size, key):
        """Handle key presses."""
        # ESC or Q closes the window
        if key in ('esc', 'q', 'Q'):
            self.on_close()
            return None

        # Pass other keys to listbox for scrolling
        return super().keypress(size, key)
