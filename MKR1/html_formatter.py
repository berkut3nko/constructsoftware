"""
Lab: Behavioral Design Patterns in LightHTML
Patterns: Template Method (PR1), State (PR2), Iterator (PR3)
"""

import collections

""" ========================================== """
""" STATE PATTERN (PR #2)                      """
""" ========================================== """

class NodeState:
    """ Base state interface for element visibility """
    def render_content(self, node):
        raise NotImplementedError()

class VisibleState(NodeState):
    """ State when node is normally visible in the HTML output """
    def render_content(self, node):
        return node.get_default_outer_html()

class HiddenState(NodeState):
    """ State when node is hidden; returns an empty string during render """
    def render_content(self, node):
        return ""


""" ========================================== """
""" ITERATOR PATTERN (PR #3)                   """
""" ========================================== """

class DFSIterator:
    """ Depth-First Search Iterator (uses a stack) """
    def __init__(self, root):
        self._stack = [root]

    def __iter__(self):
        return self

    def __next__(self):
        if not self._stack:
            raise StopIteration
        
        current = self._stack.pop()
        
        """ If element has children, push them to stack in reverse order """
        if isinstance(current, LightElementNode):
            for child in reversed(current.children):
                self._stack.append(child)
                
        return current

class BFSIterator:
    """ Breadth-First Search Iterator (uses a queue) """
    def __init__(self, root):
        self._queue = collections.deque([root])

    def __iter__(self):
        return self

    def __next__(self):
        if not self._queue:
            raise StopIteration
        
        current = self._queue.popleft()
        
        """ If element has children, add them to the end of the queue """
        if isinstance(current, LightElementNode):
            for child in current.children:
                self._queue.append(child)
                
        return current


""" ========================================== """
""" BASE DOM CLASSES                           """
""" ========================================== """

class LightNode:
    """ Base component with Template Method hooks """
    
    def __init__(self):
        self.on_created()

    def on_created(self):
        pass

    def on_inserted(self):
        pass

    def on_removed(self):
        pass

    def on_before_render(self):
        pass

    def on_after_render(self):
        pass

    def render(self):
        """ Template Method directing the rendering lifecycle """
        self.on_before_render()
        result = self.do_render()
        self.on_after_render()
        return result

    def do_render(self):
        raise NotImplementedError()


class LightTextNode(LightNode):
    """ Leaf node for plain text """
    def __init__(self, text):
        self.text = text
        super().__init__()

    def on_created(self):
        print("Hook: TextNode created -> " + self.text)

    def do_render(self):
        return self.text

    def get_default_outer_html(self):
        return self.text


class LightElementNode(LightNode):
    """ Composite element node """
    def __init__(self, tag_name, display_type, closing_type, css_classes=None):
        self.tag_name = tag_name
        self.display_type = display_type
        self.closing_type = closing_type
        self.css_classes = css_classes if css_classes else []
        self.children = []
        self._state = VisibleState()
        super().__init__()

    def set_state(self, state):
        self._state = state

    def on_created(self):
        print("Hook: ElementNode <" + self.tag_name + "> created")

    def on_inserted(self):
        print("Hook: ElementNode <" + self.tag_name + "> inserted into DOM")

    def add_child(self, child):
        self.children.append(child)
        child.on_inserted()

    def do_render(self):
        return self._state.render_content(self)

    def get_default_outer_html(self):
        class_attr = ""
        if self.css_classes:
            class_attr = " class=\"" + " ".join(self.css_classes) + "\""

        if self.closing_type == 'single':
            return "<" + self.tag_name + class_attr + " />"
        else:
            inner = "".join([child.render() for child in self.children])
            return "<" + self.tag_name + class_attr + ">" + inner + "</" + self.tag_name + ">"


""" ========================================== """
""" MAIN EXECUTION                             """
""" ========================================== """

def main():
    """ 1. Setup Tree """
    root = LightElementNode("div", "block", "closing")
    
    header = LightElementNode("header", "block", "closing")
    header.add_child(LightTextNode("Header Content"))
    
    main_section = LightElementNode("main", "block", "closing")
    p1 = LightElementNode("p", "block", "closing")
    p1.add_child(LightTextNode("Paragraph 1 Text"))
    
    main_section.add_child(p1)
    
    root.add_child(header)
    root.add_child(main_section)
    
    print("\n--- Testing Iterator Pattern (PR #3) ---")
    
    print("\nDFS (Depth-First Search) Traversal:")
    """ DFS goes deep into the first child before moving to siblings """
    for node in DFSIterator(root):
        if isinstance(node, LightElementNode):
            print("Element: <" + node.tag_name + ">")
        else:
            print("Text: '" + node.text + "'")
            
    print("\nBFS (Breadth-First Search) Traversal:")
    """ BFS visits all siblings at the current level before going deeper """
    for node in BFSIterator(root):
        if isinstance(node, LightElementNode):
            print("Element: <" + node.tag_name + ">")
        else:
            print("Text: '" + node.text + "'")

if __name__ == "__main__":
    main()