from __future__ import annotations
from typing import List, Union, Optional
from block_lexer import BlockLexer, BlockTokenType
from ast_nodes import (
    Document, Heading, Paragraph, ListBlock, ListItem, CodeBlock, Text
)

class BlockParser:
    def __init__(self, lexer: BlockLexer) -> None:
        self.lexer = lexer
        self.current_token: Optional[tuple[BlockTokenType, any]] = None
        self._next_token()
        
    def _next_token(self) -> None:
        self.current_token = self.lexer.next_token()
    
    def _parse_heading(self) -> Heading:
        token_type, value = self.current_token
        level, content = value
        return Heading(level=level, children=[Text(content)])
    
    def _parse_paragraph(self) -> Paragraph:
        lines: list[str] = []
        while self.current_token is not None:
            _, line_text = self.current_token
            lines.append(line_text)
            self._next_token()
        raw_text = "\n".join(lines)
        return Paragraph(children=[Text(raw_text)])
    
    def _parse_list(self) -> ListBlock:
        _, value = self.current_token
        ordered, content = value