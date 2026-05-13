"""
Lab: Behavioral Design Patterns in LightHTML
Patterns: Template Method (PR1), State (PR2), Iterator (PR3), Command (PR4)
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
        
        if isinstance(current, LightElementNode):
            for child in current.children:
                self._queue.append(child)
                
        return current


""" ========================================== """
""" COMMAND PATTERN (PR #4)                    """
""" ========================================== """

class Command:
    """ Base interface for DOM manipulation commands """
    def execute(self):
        raise NotImplementedError()
        
    def undo(self):
        raise NotImplementedError()

class AddChildCommand(Command):
    """ Concrete command to add a child node to a parent element """
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child

    def execute(self):
        """ Adds child and triggers its lifecycle hooks """
        self.parent.add_child(self.child)

    def undo(self):
        """ Removes the previously added child """
        self.parent.remove_child(self.child)

class CommandHistory:
    """ Invoker class that manages execution and undo history """
    def __init__(self):
        self._history = []

    def execute_command(self, command):
        """ Executes a command and saves it for potential undoing """
        command.execute()
        self._history.append(command)

    def undo(self):
        """ Pops the last command and calls its undo method """
        if self._history:
            command = self._history.pop()
            command.undo()
            print("Action undone.")


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

    def on_removed(self):
        print("Hook: ElementNode <" + self.tag_name + "> removed from DOM")

    def add_child(self, child):
        """ Internal method used by commands to modify children """
        self.children.append(child)
        child.on_inserted()

    def remove_child(self, child):
        """ Internal method used by commands to undo changes """
        if child in self.children:
            self.children.remove(child)
            child.on_removed()

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
    """ 1. Setup Base Document Structure """
    root = LightElementNode("div", "block", "closing")
    history = CommandHistory()
    
    print("--- Testing Command Pattern (PR #4) ---")
    
    """ 2. Use commands to build the tree """
    header = LightElementNode("header", "block", "closing")
    add_header_cmd = AddChildCommand(root, header)
    history.execute_command(add_header_cmd)
    
    p_tag = LightElementNode("p", "block", "closing")
    add_p_cmd = AddChildCommand(header, p_tag)
    history.execute_command(add_p_cmd)
    
    text_node = LightTextNode("This was added via a command.")
    add_text_cmd = AddChildCommand(p_tag, text_node)
    history.execute_command(add_text_cmd)
    
    print("\nRender after commands:")
    print(root.render())
    
    """ 3. Test Undo functionality """
    print("\n--- Testing Undo ---")
    history.undo() """ Removes text node """
    print("Render after 1 undo:")
    print(root.render())
    
    history.undo() """ Removes p tag """
    print("Render after 2 undos:")
    print(root.render())
    
    print("\n--- Testing Iterators along with Commands ---")
    """ Re-add p tag for iteration test """
    history.execute_command(add_p_cmd)
    
    print("\nDFS Traversal of current tree:")
    for node in DFSIterator(root):
        name = node.tag_name if isinstance(node, LightElementNode) else "Text"
        print("Visited: " + name)

if __name__ == "__main__":
    main()