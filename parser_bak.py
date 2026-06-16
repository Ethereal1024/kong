import re
from typing import Iterator, Tuple, Optional, Any
from ast_nodes import *

class Parser:
    def __init__(self, text: str) -> None:
        self.lines: list[str] = text.splitlines()
        
    def parse(self) -> Document:
        document = Document([])
        pos: int = 0
        begin: int = pos
        
        while pos < len(self.lines):
            heading_match = re.match(r'^(#{1,6})\s+(.*)$', self.lines[pos])
            if heading_match:
                level = len(heading_match.group(1))
                s = heading_match.group(2)
                document.children.append(self.parse_content(begin, pos))
                document.children.append(self.parse_heading(level, s))
                begin = pos + 1
                continue
            
            if self.lines[pos].strip() == "":
                document.children.append(self.parse_content(begin, pos))
                begin = pos + 1
                
            pos += 1
            
        return document

    def parse_heading(self, level, s) ->Heading:
        return Heading(level=level , para=self.parse_paragraph(s))
    
    def parse_content(self, begin, end) -> Content:
        content = Content([])
        pos: int = begin
        para_begin: int = pos
        
        while pos < end:
            
        
        return content
    
    def parse_paragraph(self, s: str) ->Paragraph:
        paragraph = Paragraph([])
        return paragraph