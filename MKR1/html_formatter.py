"""
Lab: Behavioral Design Patterns in LightHTML
Patterns: Template Method, State, Iterator, Command, Visitor
"""

import collections

""" ========================================== """
""" VISITOR PATTERN INTERFACES                 """
""" ========================================== """

class NodeVisitor:
    """ 
    Visitor interface to define operations on different node types 
    without changing their classes.
    """
    def visit_element_node(self, node):
        raise NotImplementedError()
        
    def visit_text_node(self, node):
        raise NotImplementedError()

class TagCounterVisitor(NodeVisitor):
    """ 
    Concrete Visitor that counts the occurrences of each HTML tag.
    """
    def __init__(self):
        self.tag_counts = {}

    def visit_element_node(self, node):
        if node.tag_name not in self.tag_counts:
            self.tag_counts[node.tag_name] = 0
        self.tag_counts[node.tag_name] += 1

    def visit_text_node(self, node):
        """ Text nodes do not contribute to tag counts """
        pass

    def get_report(self):
        return self.tag_counts


""" ========================================== """
""" STATE PATTERN                              """
""" ========================================== """

class NodeState:
    """ Base state interface for visibility management """
    def render_content(self, node):
        raise NotImplementedError()

class VisibleState(NodeState):
    """ Default state where content is rendered normally """
    def render_content(self, node):
        return node.get_default_outer_html()

class HiddenState(NodeState):
    """ Hidden state where node produces no HTML output """
    def render_content(self, node):
        return ""


""" ========================================== """
""" ITERATOR PATTERN                           """
""" ========================================== """

class DFSIterator:
    """ Depth-First Search implementation for DOM traversal """
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
    """ Breadth-First Search implementation for DOM traversal """
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
""" COMMAND PATTERN                            """
""" ========================================== """

class Command:
    """ Interface for undoable operations """
    def execute(self):
        raise NotImplementedError()
        
    def undo(self):
        raise NotImplementedError()

class AddChildCommand(Command):
    """ Command to add a node to a parent with undo capability """
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child

    def execute(self):
        self.parent.add_child(self.child)

    def undo(self):
        self.parent.remove_child(self.child)

class CommandHistory:
    """ Invoker that manages command history and provides undo functionality """
    def __init__(self):
        self._history = []

    def execute_command(self, command):
        command.execute()
        self._history.append(command)

    def undo(self):
        if self._history:
            command = self._history.pop()
            command.undo()
            print("Action undone.")


""" ========================================== """
""" BASE DOM CLASSES (With Template Method)    """
""" ========================================== """

class LightNode:
    """ 
    Base component with lifecycle hooks (Template Method) 
    and Visitor acceptance logic.
    """
    
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

    def accept(self, visitor):
        """ Accept method for Visitor Pattern """
        raise NotImplementedError()


class LightTextNode(LightNode):
    def __init__(self, text):
        self.text = text
        super().__init__()

    def on_created(self):
        print("Hook: TextNode created -> " + self.text)

    def do_render(self):
        return self.text

    def get_default_outer_html(self):
        return self.text

    def accept(self, visitor):
        visitor.visit_text_node(self)


class LightElementNode(LightNode):
    def __init__(self, tag_name, display_type, closing_type, css_classes=None):
        self.tag_name = tag_name
        self.display_type = display_type
        self.closing_type = closing_type
        self.css_classes = css_classes if css_classes else []
        self.children = []
        self._state = VisibleState()
        super().__init__()

    def set_state(self, state):
        """ State Pattern: Change internal visibility state """
        self._state = state

    def on_created(self):
        print("Hook: ElementNode <" + self.tag_name + "> created")

    def on_inserted(self):
        print("Hook: ElementNode <" + self.tag_name + "> inserted into DOM")

    def on_removed(self):
        print("Hook: ElementNode <" + self.tag_name + "> removed from DOM")

    def add_child(self, child):
        self.children.append(child)
        child.on_inserted()

    def remove_child(self, child):
        if child in self.children:
            self.children.remove(child)
            child.on_removed()

    def do_render(self):
        """ Rendering behavior is delegated to the current state """
        return self._state.render_content(self)

    def get_default_outer_html(self):
        """ Default rendering logic for the element """
        class_attr = ""
        if self.css_classes:
            class_attr = " class=\"" + " ".join(self.css_classes) + "\""

        if self.closing_type == 'single':
            return "<" + self.tag_name + class_attr + " />"
        else:
            inner = "".join([child.render() for child in self.children])
            return "<" + self.tag_name + class_attr + ">" + inner + "</" + self.tag_name + ">"

    def accept(self, visitor):
        """ Passes visitor to itself and then to all children recursively """
        visitor.visit_element_node(self)
        for child in self.children:
            child.accept(visitor)


""" ========================================== """
""" MAIN EXECUTION                             """
""" ========================================== """

def main():
    print("--- Testing Final Integration ---")
    
    root = LightElementNode("div", "block", "closing")
    history = CommandHistory()
    
    """ 1. Testing Command & Template Method hooks """
    header = LightElementNode("header", "block", "closing")
    history.execute_command(AddChildCommand(root, header))
    
    nav = LightElementNode("nav", "block", "closing")
    history.execute_command(AddChildCommand(header, nav))
    
    link = LightElementNode("a", "inline", "closing", ["link-primary"])
    link.add_child(LightTextNode("Home"))
    history.execute_command(AddChildCommand(nav, link))
    
    print("\nInitial Render:")
    print(root.render())
    
    """ 2. Testing State Pattern """
    print("\n--- Testing State (Hiding Nav) ---")
    nav.set_state(HiddenState())
    print(root.render())
    nav.set_state(VisibleState())
    
    """ 3. Testing Iterators """
    print("\n--- Testing BFS Iterator ---")
    for node in BFSIterator(root):
        info = node.tag_name if isinstance(node, LightElementNode) else "Text"
        print("BFS Visit: " + info)
        
    """ 4. Testing Visitor Pattern """
    print("\n--- Testing Visitor (Tag Counting) ---")
    counter = TagCounterVisitor()
    root.accept(counter)
    print("Tag Report: " + str(counter.get_report()))
    
    """ 5. Testing Command Undo """
    print("\n--- Testing Undo (Removing Header) ---")
    history.undo()
    history.undo()
    history.undo()
    print("\nFinal State Render:")
    print(root.render())

if __name__ == "__main__":
    main()