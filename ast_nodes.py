from __future__ import annotations
from dataclasses import dataclass
from typing import List, Union


@dataclass
class Text:
    value: str


@dataclass
class Strong:
    children: List[Union["Text", "Emphasis", "CodeInline", "Link", "Image"]]


@dataclass
class Emphasis:
    children: List[Union["Text", "Strong", "CodeInline", "Link", "Image"]]


@dataclass
class CodeInline:
    value: str


@dataclass
class Link:
    text: List[Union["Text", "Strong", "Emphasis", "CodeInline"]]


@dataclass
class Image:
    alt: str
    url: str

@dataclass
class Latex:
    display: bool
    formular: str

@dataclass
class Heading:
    level: int
    para: Paragraph


@dataclass
class Paragraph:
    children: List[Union[Text, Strong, Emphasis, CodeInline, Link, Image, Latex]]


@dataclass
class ListBlock:
    ordered: bool
    children: List[Content]


@dataclass
class CodeBlock:
    language: str
    code: str
    
@dataclass
class TableRow:
    children: List[Paragraph]
    
@dataclass
class Table:
    children: List[TableRow]
    
@dataclass
class Content:
    children: List[Union[Paragraph, ListBlock, CodeBlock, Table]]


@dataclass
class Document:
    children: List[Union[Heading, Content]]


