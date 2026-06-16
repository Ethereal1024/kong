from typing import Iterator, Tuple, Optional, Any
from enum import Enum, auto
import re

class BlockTokenType(Enum):
    BLANK = auto()
    HEADING = auto()
    TABLE = auto()
    LIST = auto()
    CODE = auto()
    PARA = auto()
    

class BlockLexer:
    def __init__(self, text: str) -> None:
        self.lines: list[str] = text.splitlines()
        self.pos: int = 0
        
    def next_token(self) -> Optional[Tuple[BlockTokenType, Any]]:
        if self.pos >= len(self.lines):
            return None
        
        line = self.lines[self.pos]
        
        if line.strip() == "":
            self.pos += 1
            return (BlockTokenType.BLANK, None)
        
        if line.startswith("```"):
            lang = line[3:].strip()
            self.pos += 1
            code_lines: list[str] = []
            while self.pos < len(self.lines) and not self.lines[self.pos].startswith("```"):
                code_lines.append(self.lines[self.pos])
                self.pos += 1
            if self.pos < len(self.lines) and self.lines[self.pos].startswith("```"):
                self.pos += 1
            code_text = "\n".join(code_lines)
            return (BlockTokenType.CODE, (lang, code_text))
        
        heading_match = re.match(r'^(#{1,6})\s+(.*)$', line)
        if heading_match:
            level = len(heading_match.group(1))
            content = heading_match.group(2)
            self.pos += 1
            return (BlockTokenType.HEADING, (level, content))
        
        ordered_match = re.match(r'^\d+\.\s+(.*)$', line)
        unorded_match = re.match(r'^[-*]\s+(.*)$', line)
        if ordered_match:
            content = ordered_match.group(1)
            self.pos += 1
            return (BlockTokenType.LIST, (True, content))
        elif unorded_match:
            content = unorded_match.group(1)
            self.pos += 1
            return (BlockTokenType.LIST, (False, content))
        
        self.pos += 1
        return (BlockTokenType.PARA, line)
    
    def token_stream(self) -> Iterator[Tuple[BlockTokenType, Any]]:
        token = self.next_token()
        while token is not None:
            yield next_token()
            token = self.next_token()
            