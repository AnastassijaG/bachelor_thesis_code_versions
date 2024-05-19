"""BAD CODE"""
import itertools

class PriorityQueueNode:
    def __init__(self, data, priority):
        self.data = data
        self.priority = priority

    def __repr__(self):
        return "{}: {}".format(self.data, self.priority)


class PriorityQueue:
    def __init__(self, items=None, priorities=None):
        self.priority_queue_list = []
        if items is None:
            return
        if priorities is None:
            priorities = itertools.repeat(None)
        for item, priority in zip(items, priorities):
            priority = item if priority is None else priority
            node = PriorityQueueNode(item, priority)
            for index, current in enumerate(self.priority_queue_list):
                if current.priority < node.priority:
                    self.priority_queue_list.insert(index, node)
                    return
            # when traversed complete queue
            self.priority_queue_list.append(node)


    def __repr__(self):
        return "PriorityQueue({!r})".format(self.priority_queue_list)

    def size(self):
        return len(self.priority_queue_list)

    def push(self, item, priority=None):
        priority = item if priority is None else priority
        node = PriorityQueueNode(item, priority)
        for index, current in enumerate(self.priority_queue_list):
            if current.priority < node.priority:
                self.priority_queue_list.insert(index, node)
                return
        # when traversed complete queue
        self.priority_queue_list.append(node)


    def pop(self):
        return self.priority_queue_list.pop().data

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