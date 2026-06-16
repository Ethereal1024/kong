import re
from typing import List, Iterator, Tuple, Optional, Any, Callable
from ast_nodes import *

class Parser:
    def __init__(self, text: str) -> None:
        self.lines: list[str] = text.splitlines()
        self.document: str = ""
        self.pos: int = 0
        self.conditions: List[Callable[[], bool]] = []
        
    def keep_this_level(self):
        return all(cond() for cond in self.conditions)
        
    def parse(self) -> None:    
        self.document += "<document>"
        self.conditions.append(lambda: self.pos < len(self.lines))
        while self.keep_this_level():
            heading_match = re.match(r'^(#{1,6})\s+(.*)$', self.lines[self.pos])
            if heading_match:
                level = len(heading_match.group(1))
                s = heading_match.group(2)
                self.parse_heading(level, s)
            
            self.parse_content()
        
        self.document += "</document>"


    def parse_heading(self, level, s) ->None:
        self.document += f"<heading level={level}>{s}</heading>"
        self.pos += 1
    
    def parse_content(self) -> None:
        self.document += "<content>"
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
                self.parse_paragraph()
            
        self.conditions.pop()
        self.pos += 1
        self.document += "</content>"
    
    def parse_code(self, lang: str) -> None:
        self.document += f"<code language={lang}>"
        self.conditions.append(lambda: not self.lines[self.pos].startswith("```"))
        
        while self.keep_this_level():
            self.document += self.lines[self.pos] + "\n"
            self.pos += 1
            
        self.conditions.pop()
        self.pos += 1
        self.document += "</code>"
        
    def parse_ol(self, s: str) -> None:
        self.document += f"<ol>{s}</ol>"
        self.pos += 1
        
    def parse_ul(self, s: str) -> None:
        self.document += f"<ul>{s}</ul>"
        self.pos += 1
        
    def parse_table(self, align: str) -> None:
        self.document += f"<table align={align}>"
        self.conditions.append(lambda: self.lines[self.pos].count('|') - 1 == len(align))
        
        while self.keep_this_level():
            self.parse_table_row(self.lines[self.pos])
            
        self.document += "</table>"
        self.pos += 1
    
    def parse_table_row(self, s: str) -> None:
        self.document += "<table_row>"
        paras: List[str] = s.strip('|').split('|')
        for para in paras:
            self.parse_paragraph(para)
        self.document += "</table_row>"
        self.pos += 1
    
    def parse_paragraph(self, s: str) ->None:
        self.document += "<paragraph>"
        
        s = re.sub(
            pattern=r"\*\*(.+?)\*\*",
            repl=r'<strong>\1</strong>',
            string=s,
            flags=re.DOTALL,
        )
        
        s = re.sub(
            pattern = r"(?<!\\)\*(?!\*|\s)(.+?)(?<!\s)(?<!\\)\*(?!\*)",
            repl=r'<emphasis>\1</emphasis>',
            string=s
        )
        
        s = re.sub(
            pattern=r"\$\$(.+?)\$\$",
            repl=r'<math style=display>\1</math>',
            string=s,
            flags=re.DOTALL,
        )

        s = re.sub(
            pattern=r"(?<!\\)\$(?!\$)(.+?)(?<!\\)\$(?!\$)",
            repl=r'<math style=inline>\1</math>',
            string=s
        )
    