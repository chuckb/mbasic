"""
Markdown to plain text renderer for curses help system.

Converts Markdown to terminal-friendly formatted text with:
- Headers converted to emphasized text
- Code blocks indented
- Lists with bullet points
- Links extracted as [text](url)
"""

import re
from typing import List, Tuple


class MarkdownRenderer:
    """Renders Markdown to plain text suitable for curses display."""

    def __init__(self):
        self.links = []  # List of (line_num, text, target) tuples

    def render(self, markdown_text: str) -> Tuple[List[str], List[Tuple[int, str, str]]]:
        """
        Render Markdown to plain text lines.

        Args:
            markdown_text: The Markdown content to render

        Returns:
            Tuple of (lines, links) where:
            - lines: List of plain text lines
            - links: List of (line_num, link_text, target_path) tuples
        """
        self.links = []
        lines = markdown_text.split('\n')
        output_lines = []
        in_code_block = False
        current_line_num = 0

        for line in lines:
            # Handle code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                # Indent code blocks
                output_lines.append('    ' + line)
                current_line_num += 1
                continue

            # Process the line
            processed = self._process_line(line, current_line_num)
            if isinstance(processed, list):
                output_lines.extend(processed)
                current_line_num += len(processed)
            else:
                output_lines.append(processed)
                current_line_num += 1

        return output_lines, self.links

    def _process_line(self, line: str, line_num: int) -> str:
        """Process a single line of Markdown."""

        # Headers
        if line.startswith('#'):
            level = 0
            while level < len(line) and line[level] == '#':
                level += 1
            text = line[level:].strip()

            if level == 1:
                # Main header - add spacing and emphasis
                return ['', '=' * len(text), text, '=' * len(text), '']
            elif level == 2:
                # Subheader
                return ['', text, '-' * len(text), '']
            else:
                # Smaller headers - just bold-ish
                return ['', text.upper(), '']

        # Unordered lists
        if line.strip().startswith('- '):
            indent = len(line) - len(line.lstrip())
            text = line.strip()[2:]
            # Extract links from list items
            text = self._extract_links(text, line_num)
            return ' ' * indent + '• ' + text

        # Ordered lists
        list_match = re.match(r'^(\s*)(\d+)\.\s+(.+)$', line)
        if list_match:
            indent, num, text = list_match.groups()
            text = self._extract_links(text, line_num)
            return indent + num + '. ' + text

        # Tables - just pass through simplified
        if '|' in line and line.strip().startswith('|'):
            # Simple table rendering - just clean up
            return line.strip()

        # Regular paragraphs - extract links
        if line.strip():
            return self._extract_links(line, line_num)

        # Empty lines
        return line

    def _extract_links(self, text: str, line_num: int) -> str:
        """
        Extract Markdown links and store them.

        Converts [text](url) to text and stores the link.
        """
        def replace_link(match):
            link_text = match.group(1)
            link_target = match.group(2)
            # Store the link
            self.links.append((line_num, link_text, link_target))
            # Return just the text (make it visually distinct)
            return f"[{link_text}]"

        # Match [text](url) pattern
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, text)

        # Strip other Markdown formatting
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*([^*]+)\*', r'\1', text)      # Italic
        text = re.sub(r'`([^`]+)`', r'\1', text)        # Code

        return text
