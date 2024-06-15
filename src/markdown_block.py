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

    def add_current_block(type):
        if current_block:
            blocks.append((type, '\n'.join(current_block)))
            current_block.clear()

    for line in lines:
        line_type = block_to_block_type(line)

        if line_type != current_type:
            add_current_block(current_type)
            current_type = line_type

        if line.strip():  # Ignore empty lines
            current_block.append(line)

    add_current_block(current_type)
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
