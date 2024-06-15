import re
from extraction import extract_markdown_links, extract_markdown_images

 
text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_image = "image"
text_type_link = "link"

class TextNode:
    
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return(
            self.text == other.text and self.text_type == other.text_type and self.url == other.url
            )
    
    def __repr__(self):
        return f"TextNode({self.text!r},{self.text_type!r},{self.url!r})"


    

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    valid_pairs = {
        None: "text",
        "**": "bold",
        "*": "italic",
        "`": "code"
    }

    if valid_pairs.get(delimiter) != text_type:
        raise ValueError("Markup mismatch: delimiter does not match text_type")
    
    nodes = []

    for old_node in old_nodes:
        if not isinstance(old_node, TextNode) or old_node.text_type != "text":
            nodes.append(old_node)
        else:
            parts = old_node.text.split(delimiter)
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    nodes.append(TextNode(part, "text"))
                else:
                    nodes.append(TextNode(part, text_type))

    return nodes



def split_nodes_image(old_nodes):
    nodes = []
    
    for old_node in old_nodes:
        remaining_text = old_node.text
        while True:
            image_tup = extract_markdown_images(remaining_text)
            if image_tup:
                if len(image_tup) == 1 and len(image_tup[0]) == 2:
                    text_parts = remaining_text.split(f"![{image_tup[0][0]}]({image_tup[0][1]})", 1)
                    if text_parts[0]:
                        nodes.append(TextNode(text_parts[0], old_node.text_type))
                    nodes.append(TextNode(image_tup[0][0], text_type_image, image_tup[0][1]))
                    if len(text_parts) > 1 and text_parts[1]:
                        remaining_text = text_parts[1]
                    else:
                        break
                else:
                    nodes.append(old_node)
                    break
            else:
                nodes.append(TextNode(remaining_text, old_node.text_type))
                break
                
    return nodes

        
        
def split_nodes_link(old_nodes):
    nodes = []
    
    for old_node in old_nodes:
        remaining_text = old_node.text
        while True:
            link_tup = extract_markdown_links(remaining_text)
            if link_tup:
                if len(link_tup) == 1 and len(link_tup[0]) == 2:
                    text_parts = remaining_text.split(f"[{link_tup[0][0]}]({link_tup[0][1]})", 1)
                    if text_parts[0]:
                        nodes.append(TextNode(text_parts[0], old_node.text_type))
                    nodes.append(TextNode(link_tup[0][0], text_type_link, link_tup[0][1]))
                    if len(text_parts) > 1 and text_parts[1]:
                        remaining_text = text_parts[1]
                    else:
                        break
                else:
                    nodes.append(old_node)
                    break
            else:
                nodes.append(TextNode(remaining_text, old_node.text_type))
                break
                
    return nodes
        
def text_to_textnodes(text):
    nodes = [TextNode(text,text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", "bold")
    nodes = split_nodes_delimiter(nodes, "*", "italic")
    nodes = split_nodes_delimiter(nodes, "`", "code")
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

