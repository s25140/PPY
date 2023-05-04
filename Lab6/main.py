class MyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __str__(self):
        elements = [str(self.head.data)]
        element = self.head
        for i in range(self.size-1):
            element = element.nextE
            elements.append(str(element.data))
        return ", ".join(elements)
        
    # get - zwraca element za wskazanym indeksem
    def get(self, e):
        curElement = self.head
        for i in range(self.size):
            if i == e:
                return curElement
            curElement = curElement.nextE
        return None
    # delete - usuwa element po indeksu
    def delete(self, e):
        if e == 0:
            self.head = self.head.nextE
            return True
        prevElement = self.head
        for i in range(1, self.size):
            if i == e:
                prevElement.nextE = prevElement.nextE.nextE
                self.size-=1
                return True
            prevElement = prevElement.nextE
        return False

    def append (self, e, func=None):
        if not self.head:
            self.head = Element(e)
            self.size+=1
            return
        if not func:
            func = lambda el1, el2 : el1>=el2
        if not func(e,self.head.data):
            self.head = Element(e,self.head)
            self.size+=1
            return
        prevEl = self.head
        el = self.head.nextE
        for i in range(self.size-1):
            if func(e,el.data):
                prevEl = el
                el = el.nextE
            else:
                prevEl.nextE = Element(e,el)
                self.size+=1
                return
        prevEl.nextE = Element(e,prevEl)
        self.size+=1
        return
        '''
        el1 = self.head
        el2 = self.head.nextE
        if func(el1, el2):
            self.head = el2
            el1.nextE = el2.nextE
            self.head.nextE = el1
            el1 = self.head
            el2 = self.head.nextE
        for i in range(self.size):
            elPrev = el1
            el1 = el2
            el2 = el2.nextE
            if func(el1, el2):
                elPrev.nextE = el2
                el1.nextE = el2.nextE
                el2.nextE = el1
                el1 = elPrev.nextE
                el2 = el2.nextE
        '''

class Element:
    def __init__(self, data=None, nextE=None):
        self.data = data
        self.nextE = nextE
    def __str__(self):
        return str(self.data)

if __name__ == "__main__":
    LinkedList = MyLinkedList()
    LinkedList.append(1)
    LinkedList.append(2)
    LinkedList.append(3)
    LinkedList.append(5)
    LinkedList.append(6,lambda x,y : x<y)
    LinkedList.append(4)
    LinkedList.delete(2)
    print(LinkedList.get(5))
    print(LinkedList)
    print(LinkedList.size)