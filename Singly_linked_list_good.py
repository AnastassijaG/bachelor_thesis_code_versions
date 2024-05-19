"""GOOD CODE"""
from __future__ import annotations
from typing import Any, Optional

class Node:
    def __init__(self, data: Any) -> None:
        self.data = data
        self.next: Optional[Node] = None

    def __repr__(self) -> str:
        return f"Node({self.data})"


class LinkedList:
    def __init__(self) -> None:
        self.head: Optional[Node] = None

    def __len__(self) -> int:
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __repr__(self) -> str:
        if not self.head:
            return ""
        current = self.head
        nodes = []
        while current:
            nodes.append(str(current.data))
            current = current.next
        return " -> ".join(nodes)

    def insert_tail(self, data: Any) -> None:
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def insert_head(self, data: Any) -> None:
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete_head(self) -> Any:
        if not self.head:
            raise IndexError("List index out of range.")
        data = self.head.data
        self.head = self.head.next
        return data

    def delete_tail(self) -> Any:
        if not self.head:
            raise IndexError("List index out of range.")
        if not self.head.next:
            data = self.head.data
            self.head = None
            return data
        current = self.head
        while current.next.next:
            current = current.next
        data = current.next.data
        current.next = None
        return data

    def reverse(self) -> None:
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

def main():
    # Creating an instance of the LinkedList class
    linked_list = LinkedList()

    # Adding elements at the head
    linked_list.insert_head(1)
    linked_list.insert_head(2)
    linked_list.insert_head(3)

    # Printing the linked list
    print("Linked list after adding elements at the head:")
    print(linked_list)

    # Adding elements at the end
    linked_list.insert_tail(4)
    linked_list.insert_tail(5)
    linked_list.insert_tail(6)

    # Printing the linked list
    print("\nLinked list after adding elements at the end:")
    print(linked_list)

    # Reversing the linked list
    linked_list.reverse()
    print("\nLinked list after reversing:")
    print(linked_list)

    # Removing the head
    removed_head = linked_list.delete_head()
    print("\nRemoved head:", removed_head)
    print("Linked list after removing the head:")
    print(linked_list)

    # Removing the end
    removed_end = linked_list.delete_tail()
    print("\nRemoved end:", removed_end)
    print("Linked list after removing the end:")
    print(linked_list)


if __name__ == "__main__":
    main()


