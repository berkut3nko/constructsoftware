"""
Lab 3: Structural Design Patterns
Tasks: Adapter, Decorator, Bridge, Proxy, Composite, Flyweight
"""

import os
import re
import sys

""" ========================================== """
""" TASK 1: ADAPTER                            """
""" ========================================== """

class Logger:
    """ Base Logger that logs to console using ANSI color codes """
    def log(self, message):
        """ Green color """
        print("\033[92m" + "Log: " + message + "\033[0m")

    def error(self, message):
        """ Red color """
        print("\033[91m" + "Error: " + message + "\033[0m")

    def warn(self, message):
        """ Orange/Yellow color """
        print("\033[93m" + "Warn: " + message + "\033[0m")


class FileWriter:
    """ Target class that only knows how to write to files """
    def __init__(self, filename):
        self.filename = filename

    def write(self, text):
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write(text)

    def write_line(self, text):
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write(text + "\n")


class FileLoggerAdapter(Logger):
    """ Adapter to make FileWriter work seamlessly with Logger interface """
    def __init__(self, file_writer):
        self.file_writer = file_writer

    def log(self, message):
        self.file_writer.write_line("Log: " + message)

    def error(self, message):
        self.file_writer.write_line("Error: " + message)

    def warn(self, message):
        self.file_writer.write_line("Warn: " + message)


""" ========================================== """
""" TASK 2: DECORATOR                          """
""" ========================================== """

class Hero:
    """ Base component for our heroes """
    def get_description(self):
        return "Unknown Hero"

    def get_power(self):
        return 0

class Warrior(Hero):
    def get_description(self):
        return "Warrior"

    def get_power(self):
        return 10

class Mage(Hero):
    def get_description(self):
        return "Mage"

    def get_power(self):
        return 8

class Palladin(Hero):
    def get_description(self):
        return "Palladin"

    def get_power(self):
        return 12

class InventoryDecorator(Hero):
    """ Base decorator class that holds a reference to a Hero """
    def __init__(self, hero):
        self._hero = hero

    def get_description(self):
        return self._hero.get_description()

    def get_power(self):
        return self._hero.get_power()

class Weapon(InventoryDecorator):
    def get_description(self):
        return self._hero.get_description() + ", Sword"

    def get_power(self):
        return self._hero.get_power() + 15

class Clothing(InventoryDecorator):
    def get_description(self):
        return self._hero.get_description() + ", Armor"

    def get_power(self):
        return self._hero.get_power() + 5

class Artifact(InventoryDecorator):
    def get_description(self):
        return self._hero.get_description() + ", Magic Ring"

    def get_power(self):
        return self._hero.get_power() + 20


""" ========================================== """
""" TASK 3: BRIDGE                             """
""" ========================================== """

class Renderer:
    """ Implementor interface for Bridge """
    def render(self, shape_name):
        pass

class VectorRenderer(Renderer):
    def render(self, shape_name):
        print("Drawing " + shape_name + " as vectors")

class RasterRenderer(Renderer):
    def render(self, shape_name):
        print("Drawing " + shape_name + " as pixels")

class Shape:
    """ Abstraction that uses a Renderer """
    def __init__(self, renderer):
        self.renderer = renderer

    def draw(self):
        pass

class Circle(Shape):
    def draw(self):
        self.renderer.render("Circle")

class Square(Shape):
    def draw(self):
        self.renderer.render("Square")

class Triangle(Shape):
    def draw(self):
        self.renderer.render("Triangle")


""" ========================================== """
""" TASK 4: PROXY                              """
""" ========================================== """

class TextReader:
    def read_file(self, filepath):
        pass

class SmartTextReader(TextReader):
    """ Real subject that reads text lines into a 2D array of chars """
    def read_file(self, filepath):
        if not os.path.exists(filepath):
            return []
        result = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                result.append(list(line.strip('\n')))
        return result

class SmartTextChecker(TextReader):
    """ Proxy for logging file reads and measuring lines/chars """
    def __init__(self, reader):
        self.reader = reader

    def read_file(self, filepath):
        print("Opening file: " + filepath)
        result = self.reader.read_file(filepath)
        print("Successfully read file: " + filepath)
        print("Closing file: " + filepath)

        total_lines = len(result)
        total_chars = sum(len(line) for line in result)
        print("Total lines: " + str(total_lines))
        print("Total chars: " + str(total_chars))

        return result

class SmartTextReaderLocker(TextReader):
    """ Proxy for restricting access to certain files via regex """
    def __init__(self, reader, regex_pattern):
        self.reader = reader
        self.pattern = re.compile(regex_pattern)

    def read_file(self, filepath):
        if self.pattern.search(filepath):
            print("Access denied!")
            return None
        return self.reader.read_file(filepath)


""" ========================================== """
""" TASK 5: COMPOSITE                          """
""" ========================================== """

class LightNode:
    """ Component interface """
    __slots__ = ()
    def get_outer_html(self):
        pass
    def get_inner_html(self):
        pass

class LightTextNode(LightNode):
    """ Leaf class containing simple text """
    __slots__ = ['text']
    def __init__(self, text):
        self.text = text

    def get_outer_html(self):
        return self.text

    def get_inner_html(self):
        return self.text

class LightElementNode(LightNode):
    """ Composite class that can hold children nodes """
    __slots__ = ['tag_name', 'display_type', 'closing_type', 'css_classes', 'children']
    def __init__(self, tag_name, display_type, closing_type, css_classes=None):
        self.tag_name = tag_name
        self.display_type = display_type
        self.closing_type = closing_type
        self.css_classes = css_classes if css_classes else []
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def get_inner_html(self):
        return "".join([child.get_outer_html() for child in self.children])

    def get_outer_html(self):
        class_attr = ""
        if self.css_classes:
            class_attr = " class=\"" + " ".join(self.css_classes) + "\""

        if self.closing_type == 'single':
            return "<" + self.tag_name + class_attr + " />"
        else:
            inner = self.get_inner_html()
            return "<" + self.tag_name + class_attr + ">" + inner + "</" + self.tag_name + ">"


""" ========================================== """
""" TASK 6: FLYWEIGHT                          """
""" ========================================== """

class ElementNodeState:
    """ Intrinsic state of an HTML element to be shared """
    __slots__ = ['tag_name', 'display_type', 'closing_type']
    def __init__(self, tag_name, display_type, closing_type):
        self.tag_name = tag_name
        self.display_type = display_type
        self.closing_type = closing_type

class NodeStateFactory:
    """ Factory to manage and cache flyweight states """
    _states = {}

    @classmethod
    def get_state(cls, tag_name, display_type, closing_type):
        key = (tag_name, display_type, closing_type)
        if key not in cls._states:
            cls._states[key] = ElementNodeState(tag_name, display_type, closing_type)
        return cls._states[key]

class FlyweightLightElementNode(LightNode):
    """ Composite element that leverages shared intrinsic state (Flyweight) """
    __slots__ = ['state', 'css_classes', 'children']
    def __init__(self, tag_name, display_type, closing_type, css_classes=None):
        """ Fetch shared intrinsic state """
        self.state = NodeStateFactory.get_state(tag_name, display_type, closing_type)
        
        """ Setup extrinsic state """
        self.css_classes = css_classes if css_classes else []
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def get_inner_html(self):
        return "".join([child.get_outer_html() for child in self.children])

    def get_outer_html(self):
        class_attr = ""
        if self.css_classes:
            class_attr = " class=\"" + " ".join(self.css_classes) + "\""

        if self.state.closing_type == 'single':
            return "<" + self.state.tag_name + class_attr + " />"
        else:
            inner = self.get_inner_html()
            return "<" + self.state.tag_name + class_attr + ">" + inner + "</" + self.state.tag_name + ">"

def calculate_memory_usage(node, seen_ids=None):
    """ Utility to calculate exact memory footprint excluding duplicate/shared object pointers """
    if seen_ids is None:
        seen_ids = set()

    node_id = id(node)
    if node_id in seen_ids:
        return 0
    seen_ids.add(node_id)

    size = sys.getsizeof(node)

    if isinstance(node, LightTextNode):
        if id(node.text) not in seen_ids:
            seen_ids.add(id(node.text))
            size += sys.getsizeof(node.text)

    elif isinstance(node, LightElementNode) or isinstance(node, FlyweightLightElementNode):
        if id(node.children) not in seen_ids:
            seen_ids.add(id(node.children))
            size += sys.getsizeof(node.children)

        if id(node.css_classes) not in seen_ids:
            seen_ids.add(id(node.css_classes))
            size += sys.getsizeof(node.css_classes)

        for child in node.children:
            size += calculate_memory_usage(child, seen_ids)

    """ Flyweight specific state counting (shows benefits of shared state) """
    if isinstance(node, FlyweightLightElementNode):
        if id(node.state) not in seen_ids:
            seen_ids.add(id(node.state))
            size += sys.getsizeof(node.state)
            size += sys.getsizeof(node.state.tag_name)
            size += sys.getsizeof(node.state.display_type)
            size += sys.getsizeof(node.state.closing_type)

    """ Regular Element specific state counting (duplicates take full memory) """
    if isinstance(node, LightElementNode):
        if id(node.tag_name) not in seen_ids:
            seen_ids.add(id(node.tag_name))
            size += sys.getsizeof(node.tag_name)
        if id(node.display_type) not in seen_ids:
            seen_ids.add(id(node.display_type))
            size += sys.getsizeof(node.display_type)
        if id(node.closing_type) not in seen_ids:
            seen_ids.add(id(node.closing_type))
            size += sys.getsizeof(node.closing_type)

    return size


""" ========================================== """
""" MAIN EXECUTION                             """
""" ========================================== """
def main():
    print("--- Task 1: Adapter ---")
    console_logger = Logger()
    console_logger.log("Console message")
    console_logger.error("Console error")
    console_logger.warn("Console warn")

    file_writer = FileWriter("log.txt")
    file_logger = FileLoggerAdapter(file_writer)
    file_logger.warn("This goes to file (simulated interface compatibility)")
    print("Written warning to log.txt")
    if os.path.exists("log.txt"):
        os.remove("log.txt")

    print("\n--- Task 2: Decorator ---")
    mage = Mage()
    print(mage.get_description() + " | Power: " + str(mage.get_power()))

    """ Using multiple decorators around one concrete Hero object """
    mage_with_weapon = Weapon(mage)
    print(mage_with_weapon.get_description() + " | Power: " + str(mage_with_weapon.get_power()))

    fully_equipped_mage = Artifact(Clothing(Weapon(Mage())))
    print(fully_equipped_mage.get_description() + " | Power: " + str(fully_equipped_mage.get_power()))

    print("\n--- Task 3: Bridge ---")
    vector_renderer = VectorRenderer()
    raster_renderer = RasterRenderer()

    triangle = Triangle(raster_renderer)
    triangle.draw()
    circle = Circle(vector_renderer)
    circle.draw()

    print("\n--- Task 4: Proxy ---")
    test_file = "test_proxy.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("Hello World!\nPattern testing.")

    reader = SmartTextReader()
    checker = SmartTextChecker(reader)
    checker.read_file(test_file)

    print("\nTesting restricted file access...")
    locker = SmartTextReaderLocker(reader, r"restricted.*\.txt")
    restricted_file = "restricted_test.txt"
    with open(restricted_file, 'w', encoding='utf-8') as f:
        f.write("Secret data")

    locker.read_file(test_file)
    locker.read_file(restricted_file)

    os.remove(test_file)
    os.remove(restricted_file)

    print("\n--- Task 5: Composite ---")
    table = LightElementNode("table", "block", "closing")
    tr = LightElementNode("tr", "block", "closing")
    td = LightElementNode("td", "inline", "closing", ["bg-dark", "text-white"])
    td.add_child(LightTextNode("Hello Composite!"))
    tr.add_child(td)
    table.add_child(tr)
    print(table.get_outer_html())

    print("\n--- Task 6: Flyweight ---")
    book_lines = [
        "Romeo and Juliet",
        "ACT V",
        "Scene I. Mantua. A Street.",
        "Scene II. Friar Lawrence's Cell.",
        "Scene III. A churchyard; in it a Monument belonging to the Capulets",
        " Dramatis Personae",
        "ESCALUS, Prince of Verona.",
        "MERCUTIO, kinsman to the Prince, and friend to Romeo."
    ] * 1000 

    """ Non-Flyweight Approach """
    root_regular = LightElementNode("div", "block", "closing")
    for i, line in enumerate(book_lines):
        if i == 0:
            node = LightElementNode("h1", "block", "closing")
        elif len(line) < 20:
            node = LightElementNode("h2", "block", "closing")
        elif line.startswith(" "):
            node = LightElementNode("blockquote", "block", "closing")
        else:
            node = LightElementNode("p", "block", "closing")
        node.add_child(LightTextNode(line))
        root_regular.add_child(node)

    mem_regular = calculate_memory_usage(root_regular)
    print("Memory used WITHOUT Flyweight: " + str(mem_regular) + " bytes")

    """ Flyweight Approach """
    root_flyweight = FlyweightLightElementNode("div", "block", "closing")
    for i, line in enumerate(book_lines):
        if i == 0:
            node = FlyweightLightElementNode("h1", "block", "closing")
        elif len(line) < 20:
            node = FlyweightLightElementNode("h2", "block", "closing")
        elif line.startswith(" "):
            node = FlyweightLightElementNode("blockquote", "block", "closing")
        else:
            node = FlyweightLightElementNode("p", "block", "closing")
        node.add_child(LightTextNode(line))
        root_flyweight.add_child(node)

    mem_flyweight = calculate_memory_usage(root_flyweight)
    print("Memory used WITH Flyweight:    " + str(mem_flyweight) + " bytes")
    print("\nSample Output (Outer HTML root preview):")
    print(root_flyweight.get_outer_html()[:250] + "...")


if __name__ == '__main__':
    main()