import re

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        props_list = [f'{key}="{value}"' for key, value in self.props.items()]
        return " ".join(props_list)

    def __repr__(self):
        props_str = self.props_to_html()
        return f"HTMLNode(tag={self.tag!r}, props={props_str!r}, value={self.value!r}, children={self.children!r})"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if not self.tag:
            return self.value if self.value else ""

        props_str = self.props_to_html()
        return f"<{self.tag} {props_str}>{self.value}</{self.tag}>" if props_str else f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        children_html = "".join(child.to_html() for child in self.children)
        props_str = self.props_to_html()

        return f"<{self.tag} {props_str}>{children_html}</{self.tag}>" if props_str else f"<{self.tag}>{children_html}</{self.tag}>"
    
def text_node_to_html_node(textnode):
    mapping = {
        "text": {"tag": None, "props": {}},
        "bold": {"tag": "b", "props": {}},
        "italic": {"tag": "i", "props": {}},
        "code": {"tag": "code", "props": {}},
        "link": {"tag": "a", "props": {"href": textnode.url if hasattr(textnode, 'url') else ""}},
        "image": {"tag": "img", "props": {"src": textnode.url if hasattr(textnode, 'url') else "", "alt": textnode.alt if hasattr(textnode, 'alt') else ""}}
    }

    if textnode.text_type not in mapping:
        raise ValueError("type not found")

    tag = mapping[textnode.text_type]["tag"]
    props = mapping[textnode.text_type]["props"]

    # Create and return the corresponding LeafNode
    html_node = LeafNode(tag=tag, value=textnode.text, props=props)

    return html_node

def heading_to_html(block):
    level = len(block.split(' ')[0])  # Count the number of '#' to determine the header level
    tag = f"h{level}"
    content = block.lstrip("# ").strip()
    return LeafNode(tag, content)

def code_to_html(block):
    content = block.strip().lstrip("```").rstrip("```").strip()
    code_node = LeafNode("code", content)
    return ParentNode("pre", [code_node])

def paragraph_to_html(block):
    content = block.strip()
    return LeafNode("p", content)

def quote_to_html(block):
    content = block.lstrip("> ").strip()
    return LeafNode("blockquote", content)

def unordered_to_html(block):
    split_block = block.strip().split("\n")
    nodes = [LeafNode("li", line.lstrip("*- ").strip()) for line in split_block if line.strip()]
    return ParentNode("ul", nodes)

def ordered_to_html(block):
    split_block = block.strip().split("\n")
    nodes = [LeafNode("li", line.lstrip("0123456789. ").strip()) for line in split_block if line.strip()]
    return ParentNode("ol", nodes)

block_type_para = "paragraph"
block_type_head = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered = "unordered_list"
block_type_ordered = "ordered_list"

def markdown_to_block(markdown):
    lines = markdown.strip().split('\n')
    blocks = []
    current_block = []
    current_type = None

    def add_current_block():
        if current_block:
            blocks.append('\n'.join(current_block))
            current_block.clear()

    for line in lines:
        line_type = block_to_block_type(line)
        if line_type != current_type or line_type in [block_type_head, block_type_para]:
            add_current_block()
            current_type = line_type
        if line.strip():  # Ignore empty lines
            current_block.append(line)
   
    add_current_block()
    return blocks

def block_to_block_type(block):
    stripped = block.strip()
    if stripped.startswith('#'):
        return block_type_head
    elif stripped.startswith('```'):
        return block_type_code
    elif stripped.startswith('>'):
        return block_type_quote
    elif stripped.startswith(('*', '-')):
        return block_type_unordered
    elif len(stripped) > 1 and stripped[0].isdigit() and stripped[1] == '.':
        return block_type_ordered
    else:
        return block_type_para

import re
import os

def markdown_to_html(markdown_content):
    html_content = ""
    lines = markdown_content.split('\n')
    in_ul_list = False
    in_ol_list = False
    in_paragraph = False

    for line in lines:
        stripped_line = line.strip()

        # Headers
        if stripped_line.startswith('# '):
            html_content += f"<h1>{stripped_line[2:].strip()}</h1>\n"
        elif stripped_line.startswith('## '):
            html_content += f"<h2>{stripped_line[3:].strip()}</h2>\n"
        elif stripped_line.startswith('### '):
            html_content += f"<h3>{stripped_line[4:].strip()}</h3>\n"
        # Unordered lists
        elif stripped_line.startswith('- '):
            if not in_ul_list:
                if in_ol_list:
                    html_content += "</ol>\n"
                    in_ol_list = False
                html_content += "<ul>\n"
                in_ul_list = True
            html_content += f"<li>{stripped_line[2:].strip()}</li>\n"
        # Ordered lists
        elif re.match(r'^\d+\.\s', stripped_line):
            if not in_ol_list:
                if in_ul_list:
                    html_content += "</ul>\n"
                    in_ul_list = False
                html_content += "<ol>\n"
                in_ol_list = True
            html_content += f"<li>{stripped_line[3:].strip()}</li>\n"
        else:
            # End list if necessary
            if in_ul_list:
                html_content += "</ul>\n"
                in_ul_list = False
            if in_ol_list:
                html_content += "</ol>\n"
                in_ol_list = False

            # Convert Markdown links to HTML links
            line = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', line)
            
            # Convert Markdown images to HTML images
            line = re.sub(r'!\[(.*?)\]\((.+?)\)', r'<img src="\2" alt="\1">', line)
            
            if stripped_line:  # Non-empty line
                if not in_paragraph:
                    html_content += "<p>"
                    in_paragraph = True
                html_content += line + " "
            else:  # Empty line
                if in_paragraph:
                    html_content += "</p>\n"
                    in_paragraph = False
    
    # Close any remaining open tags
    if in_ul_list:
        html_content += "</ul>\n"
    if in_ol_list:
        html_content += "</ol>\n"
    if in_paragraph:
        html_content += "</p>\n"
    
    return html_content
