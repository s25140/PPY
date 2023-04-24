class MyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __str__(self):
        elements = [self.head]
        for i in range(self.size-1):
            element = element.nextE
            elements.append(element)
        return ", ".join(elements)

    def get(self, e):
        curElement = self.head
        for i in range(self.size):
            if i == e:
                return curElement
            curElement = curElement.nextE
        return None

    def delete(self, e):
        if e == 0:
            self.head = self.head.nextE
            return
        prevElement = self.head
        for i in range(1, self.size):
            if i == e:
                prevElement.nextE = prevElement.nextE.nextE
            prevElement = prevElement.nextE

    def append (self, e, func=None):
        el1 = self.head
        el2 = self.head.nextE
        if func(el1, el2):
            self.head = el2
            el1.nextE = el2.nextE
            self.head.nextE = el1
        for i in range(self.size):
            el1 = el2
            el2 = el2.nextE
            func(el1, el2)

class Element:
    def __init__(self, data=None, nextE=None):
        self.data = data
        self.nextE = nextE
