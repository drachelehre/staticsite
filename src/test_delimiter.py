import unittest

from textnode import TextNode, split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_valid_bold_split(self):
        nodes = [TextNode("This is **bold** text.", "text")]
        delimiter = "**"
        text_type = "bold"
        expected_output = [TextNode("This is ", "text"), TextNode("bold", "bold"), TextNode(" text.", "text")]
        self.assertEqual(split_nodes_delimiter(nodes, delimiter, text_type), expected_output)
    
    def test_valid_italic_split(self):
        nodes = [TextNode("This is *italic* text.", "text")]
        delimiter = "*"
        text_type = "italic"
        expected_output = [TextNode("This is ", "text"), TextNode("italic", "italic"), TextNode(" text.", "text")]
        self.assertEqual(split_nodes_delimiter(nodes, delimiter, text_type), expected_output)
    
    def test_valid_code_split(self):
        nodes = [TextNode("This is `code` text.", "text")]
        delimiter = "`"
        text_type = "code"
        expected_output = [TextNode("This is ", "text"), TextNode("code", "code"), TextNode(" text.", "text")]
        self.assertEqual(split_nodes_delimiter(nodes, delimiter, text_type), expected_output)
    
    def test_invalid_bold_split(self):
        nodes = [TextNode("This is **bold** text.", "text")]
        delimiter = "**"
        text_type = "italic"
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, delimiter, text_type)
    
    def test_invalid_italic_split(self):
        nodes = [TextNode("This is *italic* text.", "text")]
        delimiter = "*"
        text_type = "bold"
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, delimiter, text_type)
    
    def test_invalid_code_split(self):
        nodes = [TextNode("This is `code` text.", "text")]
        delimiter = "`"
        text_type = "italic"
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, delimiter, text_type)
    
    def test_none_delimiter(self):
        nodes = [TextNode("This is plain text.", "text")]
        delimiter = None
        text_type = "text"
        expected_output = [TextNode("This is plain text.", "text")]
        self.assertEqual(split_nodes_delimiter(nodes, delimiter, text_type), expected_output)
    
    def test_mixed_nodes(self):
        nodes = [TextNode("This is **bold** text.", "text"), TextNode("Non-text node", "other")]
        delimiter = "**"
        text_type = "bold"
        expected_output = [TextNode("This is ", "text"), TextNode("bold", "bold"), TextNode(" text.", "text"), TextNode("Non-text node", "other")]
        self.assertEqual(split_nodes_delimiter(nodes, delimiter, text_type), expected_output)
    
    def test_no_delimiter_in_text(self):
        nodes = [TextNode("This has no delimiters.", "text")]
        delimiter = "**"
        text_type = "bold"
        expected_output = [TextNode("This has no delimiters.", "text")]
        self.assertEqual(split_nodes_delimiter(nodes, delimiter, text_type), expected_output)
    
if __name__ == '__main__':
    unittest.main()


