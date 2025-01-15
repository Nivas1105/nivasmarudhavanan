class Node:
    def __init__(self, url):
        self.url = url
        self.prev = None
        self.next = None

class BrowserHistory:
    # Constructor to initialize object with homepage
    def __init__(self, homepage: str):
        self.current = Node(homepage)

    # Visit current url
    def visit(self, url: str):
        new_node = Node(url)
        new_node.prev = self.current
        self.current.next = new_node
        self.current = new_node

    # 'steps' move backward in history and return current page
    def back(self, steps: int):
        while self.current.prev is not None and steps > 0:
            self.current = self.current.prev
            steps -= 1
        return self.current.url

    # 'steps' move forward and return current page
    def forward(self, steps: int):
        while self.current.next is not None and steps > 0:
            self.current = self.current.next
            steps -= 1
        return self.current.url

# Input case
homepage = "gfg.org"
obj = BrowserHistory(homepage)

url = "google.com"
obj.visit(url)

url = "facebook.com"
obj.visit(url)

url = "youtube.com"
obj.visit(url)

print(obj.back(1))
print(obj.back(1))
print(obj.forward(1))

obj.visit("linkedin.com")
print(obj.forward(2))
print(obj.back(2))
print(obj.back(7))
