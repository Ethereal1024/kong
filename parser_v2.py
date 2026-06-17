import re
from typing import List, Iterator, Tuple, Optional, Any, Callable
from ast_nodes import *

class Parser:
    def __init__(self, text: str) -> None:
        self.raw: str = text
        self.document: str = ""
        self.idx: int = 0
        self.new_line: bool = True
        self.conditions: List[Callable[[], bool]] = []
        
    def keep_this_level(self):
        return all(cond() for cond in self.conditions)
        
    def parse(self) -> None:    
        self.document += "<document>\n"
        self.conditions.append(lambda: self.idx < len(self.raw))
        
        while self.keep_this_level():
            if self.new_line and self.raw[self.idx] == '#':
                self.parse_heading()
            else:
                self.parse_content()
        
        self.document += "\n</document>\n"

    def parse_heading(self) -> None:
        self.new_line = False
        level: int = 0
        
        self.conditions.append(lambda: self.raw[self.idx] == '#')
        while self.keep_this_level():
            level += 1
            self.idx += 1
        self.conditions.pop()

        if self.raw[self.idx] != ' ':
            self.document += '#' * level
            return
        
        self.document += f"<heading level={level}>"

        self.conditions.append(lambda: self.raw[self.idx] != '\n')
        while self.keep_this_level():
            self.document += self.raw[self.idx]
            self.idx += 1
        self.conditions.pop()
            
        self.document += "</heading>\n"
        self.new_line = True
        self.idx += 1
    
    def parse_content(self) -> None:
        if self.raw[self.idx] == '\n':
            self.new_line = True
            self.idx += 1
            return
        
        self.document += "<content>\n"
        self.conditions.append(lambda: self.lines[self.pos].strip() != "")
        
        while self.keep_this_level():
            line = self.lines[self.pos]
            ordered_match = re.match(r'^\d+\.\s+(.*)$', line)
            unorded_match = re.match(r'^[-*]\s+(.*)$', line)
            table_match = re.match(r'^\|\s*[-:]+[-|\s]*\|\s*$', self.lines[self.pos + 1])
            
            if line.startswith("```"):
                lang = line[3:].strip()
                self.parse_code(lang)
            elif ordered_match:
                self.parse_ol(ordered_match.group(1))
            elif unorded_match:
                self.parse_ul(unorded_match.group(1))
            elif table_match:
                delimiter_line = table_match.group(0)
                align = ""
                columns = delimiter_line.strip('|').split('|')
                for col in columns:
                    if col.startswith(':') and col.endswith(':'):
                        align += 'c'
                    elif col.endswith(':'):
                        align += 'r'
                    else:
                        align += 'l'
                self.parse_table(align)
            else:
                pass
                # self.parse_paragraph()
            
        self.conditions.pop()
        self.pos += 1
        self.document += "\n</content>\n"
    
    def parse_code(self, lang: str) -> None:
        self.document += f"<code language={lang}>\n"
        self.conditions.append(lambda: not self.lines[self.pos].startswith("```"))
        
        while self.keep_this_level():
            self.document += self.lines[self.pos] + "\n"
            self.pos += 1
            
        self.conditions.pop()
        self.pos += 1
        self.document += "\n</code>\n"
        
    def parse_ol(self, s: str) -> None:
        self.document += f"<list style=ordered>\n"
        
        
        
        self.pos += 1
        
    def parse_ul(self, s: str) -> None:
        self.document += f"<ul>{s}</ul>\n"
        self.pos += 1
        
    def parse_table(self, align: str) -> None:
        self.document += f"<table align={align}>\n"
        self.conditions.append(lambda: self.lines[self.pos].count('|') - 1 == len(align))
        
        while self.keep_this_level():
            self.parse_table_row(self.lines[self.pos])
            
        self.document += "\n</table>\n"
        self.pos += 1
    
    def parse_table_row(self, s: str) -> None:
        self.document += "<table_row>"
        paras: List[str] = s.strip('|').split('|')
        for para in paras:
            self.parse_paragraph(para)
        self.document += "</table_row>\n"
        self.pos += 1
    
    def parse_paragraph(self, s: str) ->None:
        self.document += "<paragraph>\n"
        
        
    