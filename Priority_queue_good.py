"""GOOD CODE"""
import itertools

class PriorityQueueNode:
    def __init__(self, data, priority):
        self.data = data
        self.priority = priority

    def __repr__(self):
        return "{}: {}".format(self.data, self.priority)

class PriorityQueue:
    def __init__(self, items=None, priorities=None):
        self.queue = []
        if items is not None:
            if priorities is None:
                priorities = itertools.repeat(None)
            for item, priority in zip(items, priorities):
                self.push(item, priority=priority)

    def size(self):
        return len(self.queue)

    def push(self, item, priority=None):
        priority = item if priority is None else priority
        node = PriorityQueueNode(item, priority)
        index_to_insert = next((i for i, current in enumerate(self.queue) if current.priority < node.priority), len(self.queue))
        self.queue.insert(index_to_insert, node)

    def pop(self):
        if self.queue:
            return self.queue.pop().data
        else:
            raise IndexError("pop from an empty priority queue")

    def peek(self):
        if self.queue:
            return self.queue[-1].data
        else:
            raise IndexError("peek from an empty priority queue")

    def __repr__(self):
        return "[" + ", ".join(repr(node) for node in self.queue) + "]"

# Example usage of the priority queue implementation
if __name__ == "__main__":
    # Create a priority queue instance
    pq = PriorityQueue()

    # Push some items into the priority queue with priorities
    pq.push('Task 1', priority=3)
    pq.push('Task 2', priority=1)
    pq.push('Task 3', priority=2)

    # Display the priority queue
    print("Priority Queue:", pq)

    # Get the size of the priority queue
    print("Size of Priority Queue:", pq.size())

    # Pop an item from the priority queue
    popped_item = pq.pop()
    print("Popped Item:", popped_item)

    # Display the priority queue after popping
    print("Priority Queue after popping:", pq)