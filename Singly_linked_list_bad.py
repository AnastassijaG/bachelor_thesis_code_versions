"""BAD CODE"""

class N:
    def __init__(self, d: object) -> None:
        self.data = d
        self.nxt = None

    def __repr__(self) -> str:
        return f"N({self.data})"


class L:
    def __init__(self) -> None:
        self.h = None

    def __len__(self) -> int:
        c = 0
        t = self.h
        while t:
            c += 1
            t = t.nxt
        return c

    def __repr__(self) -> str:
        if not self.h:
            return ""
        t = self.h
        n = []
        while t:
            n.append(str(t.data))
            t = t.nxt
        return " -> ".join(n)

    def add_e(self, d: object) -> None:
        n = N(d)
        if not self.h:
            self.h = n
        else:
            c = self.h
            while c.nxt:
                c = c.nxt
            c.nxt = n

    def add_h(self, d: object) -> None:
        n = N(d)
        n.nxt = self.h
        self.h = n

    def rm_h(self) -> object:
        if not self.h:
            raise IndexError("List index out of range.")
        d = self.h.data
        self.h = self.h.nxt
        return d

    def rm_e(self) -> object:
        if not self.h:
            raise IndexError("List index out of range.")
        if not self.h.nxt:
            d = self.h.data
            self.h = None
            return d
        c = self.h
        while c.nxt.nxt:
            c = c.nxt
        d = c.nxt.data
        c.nxt = None
        return d

    def rv(self) -> None:
        p = None
        c = self.h
        while c:
            n = c.nxt
            c.nxt = p
            p = c
            c = n
        self.h = p

def main():
    # Creating an instance of the LinkedList class
    linked_list = L()

    # Adding elements at the head
    linked_list.add_h(1)
    linked_list.add_h(2)
    linked_list.add_h(3)

    # Printing the linked list
    print("Linked list after adding elements at the head:")
    print(linked_list)

    # Adding elements at the end
    linked_list.add_e(4)
    linked_list.add_e(5)
    linked_list.add_e(6)

    # Printing the linked list
    print("\nLinked list after adding elements at the end:")
    print(linked_list)

    # Reversing the linked list
    linked_list.rv()
    print("\nLinked list after reversing:")
    print(linked_list)

    # Removing the head
    removed_head = linked_list.rm_h()
    print("\nRemoved head:", removed_head)
    print("Linked list after removing the head:")
    print(linked_list)

    # Removing the end
    removed_end = linked_list.rm_e()
    print("\nRemoved end:", removed_end)
    print("Linked list after removing the end:")
    print(linked_list)

    # Deleting element at index 2
    deleted_element = linked_list.rm_h()
    print("\nDeleted element at index 2:", deleted_element)
    print("Linked list after deleting element at index 2:")
    print(linked_list)


if __name__ == "__main__":
    main()