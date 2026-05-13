"""
Lab: Behavioral Design Patterns in LightHTML
Pattern: Template Method (Lifecycle Hooks)
"""

import collections

class LightNode:
    """ Base component with Template Method for rendering lifecycle """
    
    def __init__(self):
        """ Logic triggered upon instance creation """
        self.on_created()

    def on_created(self):
        """ Hook: Triggered when instance is initialized """
        pass

    def on_inserted(self):
        """ Hook: Triggered when node is added to a parent element """
        pass

    def on_removed(self):
        """ Hook: Triggered when node is removed from a parent element """
        pass

    def on_before_render(self):
        """ Hook: Triggered immediately before rendering starts """
        pass

    def on_after_render(self):
        """ Hook: Triggered immediately after rendering finishes """
        pass

    def render(self):
        """ 
        Template Method: defines the skeleton of the rendering algorithm.
        Subclasses override do_render, but the order of hooks remains fixed.
        """
        self.on_before_render()
        result = self.do_render()
        self.on_after_render()
        return result

    def do_render(self):
        """ Actual rendering implementation to be defined by subclasses """
        raise NotImplementedError()


class LightTextNode(LightNode):
    """ Leaf node containing plain text """
    def __init__(self, text):
        self.text = text
        super().__init__()

    def on_created(self):
        """ Custom implementation for creation hook """
        print("Hook: TextNode created -> " + self.text)

    def do_render(self):
        """ Returns the raw text as content """
        return self.text


class LightElementNode(LightNode):
    """ Composite node that can contain other nodes """
    def __init__(self, tag_name, display_type, closing_type, css_classes=None):
        self.tag_name = tag_name
        self.display_type = display_type
        self.closing_type = closing_type
        self.css_classes = css_classes if css_classes else []
        self.children = []
        super().__init__()

    def on_created(self):
        """ Custom implementation for creation hook """
        print("Hook: ElementNode <" + self.tag_name + "> created")

    def on_inserted(self):
        """ Custom implementation for insertion hook """
        print("Hook: ElementNode <" + self.tag_name + "> inserted into DOM")

    def on_removed(self):
        """ Custom implementation for removal hook """
        print("Hook: ElementNode <" + self.tag_name + "> removed from DOM")

    def on_before_render(self):
        """ Custom implementation for pre-render hook """
        print("Hook: Preparing to render <" + self.tag_name + ">")

    def add_child(self, child):
        """ Adds a child and triggers its insertion hook """
        self.children.append(child)
        child.on_inserted()

    def remove_child(self, child):
        """ Removes a child and triggers its removal hook """
        if child in self.children:
            self.children.remove(child)
            child.on_removed()

    def do_render(self):
        """ Composite rendering logic for elements and their children """
        class_attr = ""
        if self.css_classes:
            class_attr = " class=\"" + " ".join(self.css_classes) + "\""

        if self.closing_type == 'single':
            return "<" + self.tag_name + class_attr + " />"
        else:
            """ Calls render() on children to ensure their hooks are triggered """
            inner = "".join([child.render() for child in self.children])
            return "<" + self.tag_name + class_attr + ">" + inner + "</" + self.tag_name + ">"


def main():
    """ Demonstration of Template Method hooks functionality """
    print("--- Demonstrating Template Method (Lifecycle Hooks) ---")
    
    """ 1. Triggering creation hooks """
    container = LightElementNode("div", "block", "closing", ["main-container"])
    paragraph = LightElementNode("p", "block", "closing")
    text = LightTextNode("Welcome to LightHTML!")
    
    print("\n--- Testing Insertion Hooks ---")
    """ 2. Triggering insertion hooks via add_child method """
    paragraph.add_child(text)
    container.add_child(paragraph)
    
    print("\n--- Testing Rendering Hooks (Template Method) ---")
    """ 3. Triggering pre and post render hooks via Template Method """
    html_output = container.render()
    
    print("\nFinal HTML Output:")
    print(html_output)
    
    print("\n--- Testing Removal Hooks ---")
    """ 4. Triggering removal hooks via remove_child method """
    container.remove_child(paragraph)


if __name__ == "__main__":
    main()