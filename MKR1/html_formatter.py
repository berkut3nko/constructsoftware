"""
Lab: Behavioral Design Patterns in LightHTML
Patterns: Template Method, Iterator, Command, State, Visitor
"""

import collections

""" ========================================== """
""" BASE CLASSES (From previous Lab)           """
""" AND INJECTED BEHAVIORAL PATTERNS           """
""" ========================================== """

class LightNode:
    """ Base component """
    

class LightTextNode(LightNode):
    def __init__(self, text):
        self.text = text




    def get_default_outer_html(self):
        return self.text



class LightElementNode(LightNode):
    def __init__(self, tag_name, display_type, closing_type, css_classes=None):
        self.tag_name = tag_name
        self.display_type = display_type
        self.closing_type = closing_type
        self.css_classes = css_classes if css_classes else []
        self.children = []

    def on_created(self):
        print("Hook: ElementNode <" + self.tag_name + "> created")

    def on_inserted(self):
        print("Hook: ElementNode <" + self.tag_name + "> inserted into DOM")

    def on_before_render(self):
        print("Hook: Preparing to render <" + self.tag_name + ">")

    def add_child(self, child):
        self.children.append(child)
        child.on_inserted()

    def remove_child(self, child):
        if child in self.children:
            self.children.remove(child)
            child.on_removed()
            
    def do_render(self):
        """ Modified to work with State pattern if available, otherwise just use default logic """
        if hasattr(self, '_state'):
            return self._state.render_content(self)
        return self.get_default_outer_html()
    """ === PR #1 (Template Method) END === """

    def get_default_outer_html(self):
        class_attr = ""
        if self.css_classes:
            class_attr = " class=\"" + " ".join(self.css_classes) + "\""

        if self.closing_type == 'single':
            return "<" + self.tag_name + class_attr + " />"
        else:
            """ Note: updated to use render() instead of get_outer_html() for hooks """
            inner = "".join([child.render() if hasattr(child, 'render') else child.get_outer_html() for child in self.children])
            return "<" + self.tag_name + class_attr + ">" + inner + "</" + self.tag_name + ">"










""" ========================================== """
""" MAIN EXECUTION                             """
""" ========================================== """

def main():
    """ Setup Basic Elements """
    root = LightElementNode("div", "block", "closing")
    p1 = LightElementNode("p", "block", "closing")
    text1 = LightTextNode("Hello Patterns!")
    

    




if __name__ == "__main__":
    main()