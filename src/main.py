from textnode import TextNode, split_nodes_delimiter, split_nodes_link, split_nodes_image
from htmlnode import HTMLNode, LeafNode, ParentNode, markdown_to_html, text_node_to_html_node, block_to_block_type, markdown_to_block
from extraction import extract_markdown_links, extract_markdown_images
import os
import shutil


def copy_files(src, dst):
    # Clear destination directory if it exists
    if os.path.exists(dst):
        for item in os.listdir(dst):
            item_path = os.path.join(dst, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
    else:
        os.makedirs(dst)
    
    # Recursively copy files and directories from src to dst
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            os.makedirs(d, exist_ok=True)
            print(f"Directory created: {d}")
            copy_files(s, d)
        else:
            shutil.copy2(s, d)
            print(f"File copied from {s} to {d}")

def extract_title(markdown):
    blocks = markdown_to_block(markdown)
    first_line = blocks[0]
    if not first_line.startswith("# "):
        raise Exception("No appropriate header")
    else:
        return first_line.lstrip("# ").strip()
    
def generate_page_recursive(from_path,temp_path,dest_path):
    pass
 
def generate_page(from_path,temp_path,dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {temp_path}')

    # Open files using context managers for better file handling
    with open(from_path, "r") as markdown_file:
        md_content = markdown_file.read()
    
    with open(temp_path, "r") as template_file:
        temp_content = template_file.read()

    # Extract title and convert markdown to HTML
    title = extract_title(md_content)
    markdown_node = markdown_to_html(md_content)

    # Replace template elements
    replaced_title = temp_content.replace("{{ Title }}", title)
    replaced_content = replaced_title.replace("{{ Content }}", markdown_node)

    # Print the resulting string for testing purposes
    print(replaced_content)

    # Write the final HTML string to the destination
    with open(dest_path, "w") as dest_file:
        dest_file.write(replaced_content)
    
    
def main():
    copy_files("./static", "./public")    
    from_path = "./content/index.md"
    temp_path = "./template.html"
    dest_path = "./public/index.html"
    generate_page(from_path,temp_path,dest_path)
    
if __name__ == "__main__":
    main()
