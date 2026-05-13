"""
Lab: Behavioral Design Patterns in LightHTML
Patterns: Template Method (PR1), State (PR2)
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
        """ Basic text rendering """
        return self.text


class LightElementNode(LightNode):
    """ Composite element node with State support """
    def __init__(self, tag_name, display_type, closing_type, css_classes=None):
        self.tag_name = tag_name
        self.display_type = display_type
        self.closing_type = closing_type
        self.css_classes = css_classes if css_classes else []
        self.children = []
        
        """ State Pattern Initialization (PR #2) """
        self._state = VisibleState()
        
        super().__init__()

    def set_state(self, state):
        """ Changes the current rendering state of the element """
        self._state = state

    def on_created(self):
        print("Hook: ElementNode <" + self.tag_name + "> created")

    def on_inserted(self):
        print("Hook: ElementNode <" + self.tag_name + "> inserted into DOM")

    def add_child(self, child):
        self.children.append(child)
        child.on_inserted()

    def do_render(self):
        """ 
        The rendering logic is now delegated to the State object.
        This allows visibility control (PR #2).
        """
        return self._state.render_content(self)

    def get_default_outer_html(self):
        """ Standard HTML generation for the element """
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
    print("--- Demonstrating State Pattern (Visibility) ---")
    
    """ Build a simple tree """
    root = LightElementNode("div", "block", "closing")
    paragraph = LightElementNode("p", "block", "closing")
    text = LightTextNode("This text can be hidden using States.")
    
    paragraph.add_child(text)
    root.add_child(paragraph)
    
    print("\n1. Initial Render (Visible State):")
    print(root.render())
    
    print("\n2. Switching Paragraph to Hidden State:")
    """ Change internal state of the paragraph element """
    paragraph.set_state(HiddenState())
    
    print("Render Output (Paragraph should be gone):")
    print(root.render())
    
    print("\n3. Reverting back to Visible State:")
    paragraph.set_state(VisibleState())
    print(root.render())

if __name__ == "__main__":
    main()