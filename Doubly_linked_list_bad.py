"""BAD CODE"""
class Node:
     def __init__(self, data):
         self.data = data
         self.previous = None
         self.next = None

     def __str__(self):
         return f"{self.data}"

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
         result = ""
         current = self.head
         while current:
             result += str(current.data) + "->"
             current = current.next
         return result[:-2]

     def __len__(self):
         count = 0
         current = self.head
         while current:
             count += 1
             current = current.next
         return count

     def insert_at_head(self, data):
         length = len(self)
         new_node = Node(data)
         if length == 0:
             self.head = self.tail = new_node
         else:
             new_node.next = self.head
             self.head.previous = new_node
             self.head = new_node

     def insert_at_tail(self, data):
         length = self.__len__()
         new_node = Node(data)
         if length == 0:
             self.head = self.tail = new_node
         else:
             self.tail.next = new_node
             new_node.previous = self.tail
             self.tail = new_node

     def insert_at_nth(self, index: int, data):
         length = self.__len__()
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
         length = self.__len__()
         if length == 0:
             raise IndexError("list index out of range")
         data = self.head.data
         if length == 1:
             self.head = self.tail = None
         else:
             self.head = self.head.next
             self.head.previous = None
         return data

     def delete_tail(self):
         length = self.__len__()
         if length == 0:
             raise IndexError("list index out of range")
         data = self.tail.data
         if length == 1:
             self.head = self.tail = None
         else:
             self.tail = self.tail.previous
             self.tail.next = None
         return data

     def delete_at_nth(self, index: int):
         length = self.__len__()
         if not 0 <= index < length:
             raise IndexError("list index out of range")
         current = self.head
         if length == 1:
             self.head = self.tail = None
         elif index == 0:
             data = self.head.data
             self.head = self.head.next
             self.head.previous = None
         elif index == length - 1:
             current = self.tail
             data = current.data
             self.tail = self.tail.previous
             self.tail.next = None
         else:
             for _ in range(index):
                 current = current.next
             data = current.data
             current.previous.next = current.next
             current.next.previous = current.previous
         return data

     def delete(self, data) -> str:
         current = self.head
         while current:
             if current.data == data:
                 if current == self.head:
                     return self.delete_head()
                 elif current == self.tail:
                     return self.delete_tail()
                 else:
                     current.previous.next = current.next
                     current.next.previous = current.previous
                     return data
             current = current.next
         raise ValueError("No data matching given value")

     def is_empty(self):
         return len(self) == 0

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
         linked_list.insert_at_nth(i, i + 1)
     assert str(linked_list) == "->".join(str(i) for i in range(1, 11))

     linked_list.insert_at_head(0)
     linked_list.insert_at_tail(11)
     assert str(linked_list) == "->".join(str(i) for i in range(12))

     assert linked_list.delete_head() == 0
     assert linked_list.delete_at_nth(9) == 10
     assert linked_list.delete_tail() == 11
     assert len(linked_list) == 9
     assert str(linked_list) == "->".join(str(i) for i in range(1, 10))


def main():
     # Create a new doubly linked list
     linked_list = DoublyLinkedList()

     # Insert elements at different positions
     linked_list.insert_at_tail(1)
     linked_list.insert_at_head(2)
     linked_list.insert_at_tail(3)
     linked_list.insert_at_tail(4)

     # Print the doubly linked list
     print("Doubly Linked List:", linked_list)

     # Delete element at nth position
     deleted_element = linked_list.delete_at_nth(2)
     print("Deleted element at index 2:", deleted_element)

     # Print the updated doubly linked list
     print("Updated Doubly Linked List:", linked_list)

     deleted_element = linked_list.delete_tail()
     print("Deleted tail:", deleted_element)

     print("Updated Doubly Linked List:", linked_list)

     # Check if the list is empty
     print("Is the list empty?", linked_list.is_empty())


if __name__ == "__main__":
     main()