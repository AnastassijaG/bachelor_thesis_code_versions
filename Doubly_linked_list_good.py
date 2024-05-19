"""GOOD CODE"""
class Node:
    def __init__(self, data):
        self.data = data
        self.previous = None
        self.next = None

    def __str__(self):
        return str(self.data)


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __str__(self):
        return "->".join(str(item) for item in self)

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def insert_at_head(self, data):
        self.insert_at_index(0, data)

    def insert_at_tail(self, data):
        self.insert_at_index(len(self), data)

    def insert_at_index(self, index: int, data):
        length = len(self)
        if not 0 <= index <= length:
            raise IndexError("list index out of range")

        new_node = Node(data)
        if length == 0:
            self.head = self.tail = new_node
        elif index == 0:
            new_node.next = self.head
            self.head.previous = new_node
            self.head = new_node
        elif index == length:
            self.tail.next = new_node
            new_node.previous = self.tail
            self.tail = new_node
        else:
            current = self.head
            for _ in range(index):
                current = current.next
            new_node.next = current
            new_node.previous = current.previous
            current.previous.next = new_node
            current.previous = new_node

    def delete_head(self):
        return self.delete_at_index(0)

    def delete_tail(self):
        return self.delete_at_index(len(self) - 1)

    def delete_at_index(self, index: int):
        length = len(self)
        if not 0 <= index < length:
            raise IndexError("list index out of range")

        current = self.head
        if length == 1:
            self.head = self.tail = None
        elif index == 0:
            self.head = self.head.next
            self.head.previous = None
        elif index == length - 1:
            current = self.tail
            self.tail = self.tail.previous
            self.tail.next = None
        else:
            for _ in range(index):
                current = current.next
            current.previous.next = current.next
            current.next.previous = current.previous

        return current.data

    def delete(self, data):
        current = self.head
        while current:
            if current.data == data:
                if current == self.head:
                    self.delete_head()
                elif current == self.tail:
                    self.delete_tail()
                else:
                    current.previous.next = current.next
                    current.next.previous = current.previous
                return data
            current = current.next
        raise ValueError("No data matching given value")

    def is_empty(self):
        return self.head is None

def test_doubly_linked_list():
    linked_list = DoublyLinkedList()
    assert linked_list.is_empty() is True
    assert str(linked_list) == ""

    try:
        linked_list.delete_head()
        raise AssertionError  # This should not happen.
    except IndexError:
        assert True  # This should happen.

    try:
        linked_list.delete_tail()
        raise AssertionError  # This should not happen.
    except IndexError:
        assert True  # This should happen.

    for i in range(10):
        assert len(linked_list) == i
        linked_list.insert_at_index(i, i + 1)
    assert str(linked_list) == "->".join(str(i) for i in range(1, 11))

    linked_list.insert_at_head(0)
    linked_list.insert_at_tail(11)
    assert str(linked_list) == "->".join(str(i) for i in range(12))

    assert linked_list.delete_head() == 0
    assert linked_list.delete_at_index(9) == 10
    assert linked_list.delete_tail() == 11
    assert len(linked_list) == 9
    assert str(linked_list) == "->".join(str(i) for i in range(1, 10))


def main():
    # Create a new doubly linked list
    linked_list = DoublyLinkedList()

    # Insert elements at different positions
    linked_list.insert_at_tail(1)
    print("After inserting 1 at tail:", linked_list)

    linked_list.insert_at_head(2)
    print("After inserting 2 at head:", linked_list)

    linked_list.insert_at_tail(3)
    print("After inserting 3 at tail:", linked_list)

    linked_list.insert_at_index(2, 4)
    print("After inserting 4 at index 2:", linked_list)

    # Delete elements at different positions
    deleted_element = linked_list.delete_at_index(1)
    print("Deleted element at index 1:", deleted_element)
    print("After deleting element at index 1:", linked_list)

    deleted_element = linked_list.delete_head()
    print("Deleted head:", deleted_element)
    print("After deleting head:", linked_list)

    deleted_element = linked_list.delete_tail()
    print("Deleted tail:", deleted_element)
    print("After deleting tail:", linked_list)

    deleted_element = linked_list.delete(4)
    print("Deleted element 4:", deleted_element)
    print("After deleting element 4:", linked_list)

    # Check if the list is empty
    print("Is the list empty?", linked_list.is_empty())


if __name__ == "__main__":
    main()
