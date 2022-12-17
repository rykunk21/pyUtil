from sqlite3 import connect
from cmath import exp
import gc
from symbol import continue_stmt
import time
from typing import TypeVar, List, Callable, Dict, Tuple
from random import randint, shuffle
from timeit import default_timer
#from matplotlib import pyplot as plt  # COMMENT OUT THIS LINE (and `plot_speed`) if you dont want matplotlib
import enum
from importlib.resources import files
from requests import delete

HashNode = TypeVar("HashNode")
HashTable = TypeVar("HashTable")
# Type Declarations
T = TypeVar('T')  # generic type
SLL = TypeVar('SLL')  # forward declared
Node = TypeVar('Node')  # forward declare `Node` type
DLL = TypeVar("DLL")

class SLLNode:
    """
    Node implementation
    Do not modify.
    """

    __slots__ = ['val', 'next']

    def __init__(self, value: T, next: Node = None) -> None:
        """
        Initialize an SLL Node
        :param value: value held by node
        :param next: reference to the next node in the SLL
        :return: None
        """
        self.val = value
        self.next = next

    def __str__(self) -> str:
        """
        Overloads `str()` method to cast nodes to strings
        return: string
        """
        return '(Node: ' + str(self.val) + ' )'

    def __repr__(self) -> str:
        """
        Overloads `repr()` method for use in debugging
        return: string
        """
        return '(Node: ' + str(self.val) + ' )'

    def __eq__(self, other: Node) -> bool:
        """
        Overloads `==` operator to compare nodes
        :param other: right operand of `==`
        :return: bool
        """
        return self is other if other is not None else False


class SinglyLinkedList:
    """
    Implementation of an SLL
    """

    __slots__ = ['head', 'tail']

    def __init__(self) -> None:
        """
        Initializes an SLL
        :return: None
        DO NOT MODIFY THIS FUNCTION
        """
        self.head = None
        self.tail = None

    def __repr__(self) -> str:
        """
        Represents an SLL as a string
        DO NOT MODIFY THIS FUNCTION
        """
        return self.to_string()

    def __eq__(self, other: SLL) -> bool:
        """
        Overloads `==` operator to compare SLLs
        :param other: right hand operand of `==`
        :return: `True` if equal, else `False`
        DO NOT MODIFY THIS FUNCTION
        """
        comp = lambda n1, n2: n1 == n2 and (comp(n1.next, n2.next) if (n1 and n2) else True)
        return comp(self.head, other.head)

    # ============ Modify below ============ #
    def push(self, value: T) -> None:
        """
        Pushes an SLLNode to the end of the list
        :param value: value to push to the list
        :return: None
        """
        end = SLLNode(value)
        if self.tail:
            self.tail.next = self.tail = end
        else:
            self.head = self.tail = end

    def to_string(self) -> str:
        """
        Converts an SLL to a string
        :return: string representation of the linked list
        """
        if self.head:
            current = self.head
            out = [current.val]
            while current.next:
                current = current.next
                out.append(current.val)
                #out.append(str(current.val))
            return ' --> '.join(out)
        else:
            return 'None'
        
    def length(self) -> int:
        """
        Determines number of nodes in the list
        :return: number of nodes in list
        """
        if self.head:
            current = self.head
            count = 1
            while current.next:
                current = current.next
                count += 1
            return count
        else:
            return 0

    def sum_list(self) -> T:
        """
        Sums the values in the list
        :return: sum of values in list
        """
        if self.head:
            current = self.head
            out = [current.val]
            while current.next:
                current = current.next
                out.append(current.val)
            if any([isinstance(val, str) for val in out]):
                return ''.join(out)
            else:
                return sum(out)
        else:
            return None

    def remove(self, value: T) -> bool:
        """
        Removes the first node containing `value` from the SLL
        :param value: value to remove
        :return: True if a node was removed, False otherwise
        """
    
        if self.head: # check that the list is Non empty

            if self.head.val == value: # if the value is the head

                if self.head is self.tail: # unless theres only one element
                    self.head = self.tail = None
                    return True

                self.head = self.head.next # Head equals second element
                return True
            else: # if the value is not the head

                current = self.head
                while current.next:
                    if current.next.val == value: # find the node with the value

                        if current.next is self.tail: # if the value is the tail
                            self.tail = current # reassign the tail

                        current.next = current.next.next # skip the node with the value
                        return True
                    current = current.next
                
                return False # if you didnt find the node, return false
        else:
            return False

    def remove_all(self, value: T) -> bool:
        """
        Removes all instances of a node containing `value` from the SLL
        :param value: value to remove
        :return: True if a node was removed, False otherwise
        """
        removed = False
        if self.head: # if the list is non empty

            while self.head.val == value: # while the value is the head
                self.head = self.head.next # skip the head
                removed = True
                if self.head is None:
                    self.tail = None
                    return True
                
            current = self.head
            while current.next: # look through the values
                if current.next.val == value: # if you find the value

                    if current.next is self.tail: # if the value is the tail
                        self.tail = current # reassign the tail

                    current.next = current.next.next # skip the node
                    removed = True
                if current.next is None:
                    break
                else:
                    current = current.next
            return removed

        else:
            return False

    def search(self, value: T) -> bool:
        """
        Searches the SLL for a node containing `value`
        :param value: value to search for
        :return: `True` if found, else `False`
        """
        if not self.head:
            return False
        current = self.head

        while current.next:
            if current.val == value:
                return True
            current = current.next

        return self.tail.val == value

    def count(self, value: T) -> int:
        """
        Returns the number of occurrences of `value` in this list
        :param value: value to count
        :return: number of times the value occurred
        """
        if not self.head:
            return 0
        count = 0
        current = self.head

        while current:
            if current.val == value:
                count += 1
            current = current.next
        
        return count


def reverse(data: SLL) -> None:
    """
    Reverses the data
    :param data: an SLL
    :return: None
    """

    "Algorithm: https://media.geeksforgeeks.org/wp-content/cdn-uploads/RGIF2.gif"
    
    prev = None
    current = data.tail = data.head 
    
    while current:
        next = current.next
        current.next = prev
        prev = current
        current = next

    data.head = prev
        

class DLLNode:
    """
    Implementation of a doubly linked list node.
    Do not modify.
    """
    __slots__ = ["value", "next", "prev"]

    def __init__(self, value: T, next: Node = None, prev: Node = None) -> None:
        """
        Construct a doubly linked list node.

        :param value: value held by the Node.
        :param next: reference to the next Node in the linked list.
        :param prev: reference to the previous Node in the linked list.
        :return: None.
        """
        self.next = next
        self.prev = prev
        self.value = value

    def __repr__(self) -> str:
        """
        Represents the Node as a string.

        :return: string representation of the Node.
        """
        return f"Node({str(self.value)})"

    def __eq__(self, other: Node):
        return self.value == other.value

    __str__ = __repr__


class DLL:
    """
    Implementation of a doubly linked list without padding nodes.
    Modify only below indicated line.
    """
    __slots__ = ["head", "tail", "size"]

    def __init__(self) -> None:
        """
        Construct an empty doubly linked list.

        :return: None.
        """
        self.head = self.tail = None
        self.size = 0

    def __repr__(self) -> str:
        """
        Represent the DLL as a string.

        :return: string representation of the DLL.
        """
        result = []
        node = self.head
        while node is not None:
            result.append(str(node))
            node = node.next
            if node is self.head:
                break
        return " <-> ".join(result)

    def __str__(self) -> str:
        """
        Represent the DLL as a string.

        :return: string representation of the DLL.
        """
        return repr(self)

    def __eq__(self, other: DLL) -> bool:
        """
        :param other: compares equality with this List
        :return: True if equal otherwise False
        """
        cur_node = self.head
        other_node = other.head
        while True:
            if cur_node != other_node:
                return False
            if cur_node is None and other_node is None:
                return True
            if cur_node is None or other_node is None:
                return False
            cur_node = cur_node.next
            other_node = other_node.next
            if cur_node is self.head and other_node is other.head:
                return True
            if cur_node is self.head or other_node is other.head:
                return False

    # MODIFY BELOW #
    # Refer to the classes provided to understand the problems better#

    def empty(self) -> bool:
        """
        Determines if the list is empty
        :param: none
        :return: True if the list is empty else False
        """
        return not self.head


    def push(self, val: T, back: bool = True) -> None:
        """
        Adds an elemet to the front or back of a DLL
        :param val: the value to be added
        :param bacK: boolean indicacting weather to add the item to the back of the DLL
        :return: None 
        """
        
        if not self.head:
            toAdd = Node(val, None, None)
            self.head = self.tail = toAdd
            return

        if back:
            toAdd = Node(val, None, self.tail)
            self.tail.next = toAdd
            self.tail = toAdd
        else:
            toAdd = Node(val, self.head, None)
            self.head.prev = toAdd
            self.head = toAdd
            

    def pop(self, back: bool = True) -> None:
        """
        Removes a single element from the front or back of the DLL
        :param back: indicates weather to remove from the back
        :return: none
        """
        if not self.head:
            return
        
        if back:
            if self.tail is self.head:
                self.head = self.tail = None
                return
            
            self.tail = self.tail.prev
            self.tail.next = None
            self.size -= 1

        else:
            if self.tail is self.head:
                self.head = self.tail = None
                return
            self.head = self.head.next
            self.head.prev = None


    def list_to_dll(self, source: List[T]) -> None:
        """
        constructs an instance of a DLL from a python list
        :param source: the list to construct with
        :return: None
        """
        self.head = self.tail = None
        for _, val in enumerate(source):
            self.push(val)
        

    def dll_to_list(self) -> List[T]:
        """
        converts a DLL to a python list
        :return: python list representation of the DLL
        """
        out = []
        curr = self.head
        while curr:
            out.append(curr.value)
            curr = curr.next
        return out


    def _find_nodes(self, val: T, find_first: bool = False) -> List[Node]:
        """
        Find all the nodes in a DLL with a particular value
        :param val: the value to be found
        :param find_first: If true only return one element
        :return: a list of nodes containing the value
        """
        out = []
        curr = self.head
        while curr:
            if curr.value == val:
                out.append(curr)
                if find_first:
                    return out
                
            curr = curr.next
        return out


    def find(self, val: T) -> Node:
        """
        Finds first node in the DLL with value val
        :param val: the value to find
        :return: the first node containing the value
        """
        try:
            return self._find_nodes(val,True)[0]
        except IndexError:
            return None
         

    def find_all(self, val: T) -> List[Node]:
        """
        finds all instances of a node with a particular value
        :param val: the value to be found
        :return: a list of nodes containing the value
        """
        return self._find_nodes(val)


    def _remove_node(self, to_remove: Node) -> None:
        """
        removes a node from the list
        :param to_remove: the node to remove
        :return: None
        """
        prev = to_remove.prev
        next = to_remove.next
        if (prev is next is None) or (not self.head):
            self.head = self.tail = None
            return
        
        elif not prev:
            self.head = self.head.next
            self.head.prev = None
        
        elif not next:
            self.tail = self.tail.prev
            self.tail.next = None

        else:
            prev.next = next
            next.prev = prev
            return
            

    def remove(self, val: T) -> bool:
        """
        Removes the first instance of a node with a particular value
        :param val: the value to be removed
        :return: True if value was removed else False
        """
        curr = self.head
        while curr:
            if curr.value == val:
                self._remove_node(curr)
                return True
            curr = curr.next
        return False


    def remove_all(self, val: T) -> int:
        """
        removes all instances of a node with a particular value
        :param val: the val to be removed
        :return: the number of nodes removed
        """
        count = 0
        for node in self.find_all(val):
            self._remove_node(node)
            count += 1

        return count
        
        
    def reverse(self) -> None:
        """
        reverses the DLL
        :return: None
        """
        curr = self.tail = self.head
        temp = None

        while curr:
            temp = curr.prev
            curr.prev = curr.next
            curr.next = temp
            curr = curr.prev

        if temp:
            self.head = temp.prev 


def fix_playlist(lst: DLL) -> bool:
    """
    Given a DLL, determine if it fits the accurate form for a playlist
    https://apollo-media.codio.com/media%2F1%2Fe16e3603c996eeac9bacdc796839e415-8101e47f4fe50f52.webp
    :param lst: the DLL to operate on
    :return: True if lst is in broken or proper state, else False
    """
    def connect_list(node: Node) -> bool:
        """
        Connectst the head and tail at a particular node
        :param node: the node to begin the looped linked list with
        :return: True after successful linking
        """
        lst.head = node
        node.prev = lst.tail
        lst.tail.next = node
        return True

    def fix_playlist_helper(slow: Node, fast: Node) -> bool:
        """
        Iterates Floyds algorithm and determines if the linked list is in a loop state
        :param slow: the node to increment slow
        :param fast: the node to increment fast
        :return: True if the the DLL is cyclic else False
        """
        while fast and fast.next and slow:
            if fast == slow:
                # cycle
                return True
            fast = fast.next.next
            slow = slow.next
        # no cycle     
        return False
    
    if not lst.head:
        # empty list is proper
        return True

    if not fix_playlist_helper(lst.head, lst.head.next):
        # broken
        connect_list(lst.head)
        return True
    else:
        # if true, proper, if false, improper
        if (lst.head.prev is lst.tail) and (lst.tail.next is lst.head):
            return True
        else:
            # fix the improper list
            return False
            

class CircularDeque:
    """
    Representation of a Circular Deque using an underlying python list
    """

    __slots__ = ['capacity', 'size', 'queue', 'front', 'back']

    def __init__(self, data: List[T] = None, front: int = 0, capacity: int = 4):
        """
        Initializes an instance of a CircularDeque
        :param data: starting data to add to the deque, for testing purposes
        :param front: where to begin the insertions, for testing purposes
        :param capacity: number of slots in the Deque
        """
        if data is None and front != 0:
            data = ['Start']  # front will get set to 0 by a front enqueue if the initial data is empty
        elif data is None:
            data = []

        self.capacity: int = capacity
        self.size: int = len(data)
        self.queue: List[T] = [None] * capacity
        self.back: int = (self.size + front - 1) % self.capacity if data else None
        self.front: int = front if data else None

        for index, value in enumerate(data):
            self.queue[(index + front) % capacity] = value

    def __str__(self) -> str:
        """
        Provides a string representation of a CircularDeque
        'F' indicates front value
        'B' indicates back value
        :return: the instance as a string
        """
        if self.size == 0:
            return "CircularDeque <empty>"

        str_list = ["CircularDeque <"]
        for i in range(self.capacity):
            str_list.append(f"{self.queue[i]}")
            if i == self.front:
                str_list.append('(F)')
            elif i == self.back:
                str_list.append('(B)')
            if i < self.capacity - 1:
                str_list.append(',')

        str_list.append(">")
        return "".join(str_list)

    __repr__ = __str__

    #
    # Your code goes here!
    #
    def __len__(self) -> int:
        """
        Dunder method for returning the length of the circular deque
        :return: int representing the length of the circular deque
        """
        return self.size

    def is_empty(self) -> bool:
        """
        determines if the list is empty
        :return: bool representing if the list is empty
        """
        return self.size == 0

    def front_element(self) -> T:
        """
        returns the first elemet of the circular deque
        :return: the first element of the circular deque
        """
        return self.queue[self.front] if not (self.front is None) else None

    def back_element(self) -> T:
        """
        returns the back element of the circular deque
        :return: the last element of the circular deque
        """
        return self.queue[self.back] if not (self.back is None) else None

    def enqueue(self, value: T, front: bool = True) -> None:
        """
        enqueues an element to either side of the circular queue
        :param value: the value to add to the queue
        :param front: if true, add to the front of the queue else add to the end
        :return: None
        """
        if front: # add to front

            self.size += 1
            if self.front is None:
                self.front = 0
                self.back = 0
            else:
                self.front = (self.front - 1) % self.capacity

            self.queue[self.front] = value # set the element

            if self.size == self.capacity: # grow if maxed out
                self.grow()
            
        else: # add to back
            
            self.size += 1
            if self.back is None:
                self.front = 0
                self.back = 0
            else:
                self.back = (self.back + 1) % self.capacity
            self.queue[self.back] = value

            if self.size == self.capacity:
                self.grow()

    def dequeue(self, front: bool = True) -> T:
        """
        dequeues an element from either side of the circular deque

        Calls shrink() If the current size is less than or equal to 1/4 the 
        current capacity, and 1/2 the current capacity is greater than or 
        equal to 4, halves the capacity.

        :param front: Bool indicating return from the front
        :return: element that was dequed from the CD
        """
        if front: # dequeue from front

            if self.front is None or self.is_empty():
                return None
            else:
                # decrememnt size 
                self.size -= 1
                element = self.queue[self.front] # find the element

                # fix front
                self.front = (self.front + 1) % self.capacity
                
        else: # dequeue from back
            if self.back is None or self.is_empty():
                return None
            else:
                # decrement size
                self.size -= 1
                element = self.queue[self.back] # find the element

                # fix back
                self.back = (self.back - 1) % self.capacity

        # determine shrink
        if self.size <= self.capacity / 4 and self.capacity / 2 >= 4:
            self.shrink()

        return element
                
    def grow(self) -> None:
        """
        Doubles the size of the CD and unrolls it
        :return: None
        """
        # check for non empty list
        front = self.front if self.front else 0
        back = self.back if self.back else 0
        
        # get the data
        newQueue: List[T] = self.queue[front:]
        if back < front:
            newQueue += self.queue[:back+1]
        
        newQueue += [None] * self.capacity

        # fix front and back
        self.front = 0 if not self.front is None else None
        self.back = (self.size - 1) if not self.back is None else None

        # reset queue
        self.queue = newQueue
        self.capacity *= 2

    def shrink(self) -> None:
        """
        cuts the capacity in half and unrolls the CD
        :return: None
        """
        # check for non empty list
        front = self.front if self.front else 0
        back = self.back if self.back else 0
        
        # get the data
        newQueue: List[T] = self.queue[front: back + 1]
        if back < front:
            newQueue += self.queue[back: front + 1]

        # fix front and back
        self.front = 0 if not self.front is None else None
        self.back = (self.size - 1) if not self.back is None else None

        # reset the queue
        self.capacity = self.capacity // 2 if ((self.capacity // 2 )> 4) else 4
        newQueue += [None] * (self.capacity - len(newQueue))
        self.queue = newQueue[:self.capacity]
        

class HashNode:
    """
    DO NOT EDIT
    """
    __slots__ = ["key", "value", "deleted"]

    def __init__(self, key: str, value: T, deleted: bool = False) -> None:
        self.key = key
        self.value = value
        self.deleted = deleted

    def __str__(self) -> str:
        return f"HashNode({self.key}, {self.value})"

    __repr__ = __str__

    def __eq__(self, other: HashNode) -> bool:
        return self.key == other.key and self.value == other.value

    def __iadd__(self, other: T) -> None:
        self.value += other


class HashTable:
    """
    Hash Table Class
    """
    __slots__ = ['capacity', 'size', 'table', 'prime_index']

    primes = (
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
        109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
        233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359,
        367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491,
        499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641,
        643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787,
        797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
        947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061, 1063, 1069,
        1087, 1091, 1093, 1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163, 1171, 1181, 1187, 1193, 1201, 1213,
        1217, 1223, 1229, 1231, 1237, 1249, 1259, 1277, 1279, 1283, 1289, 1291, 1297, 1301, 1303, 1307, 1319, 1321,
        1327, 1361, 1367, 1373, 1381, 1399, 1409, 1423, 1427, 1429, 1433, 1439, 1447, 1451, 1453, 1459, 1471, 1481,
        1483, 1487, 1489, 1493, 1499, 1511, 1523, 1531, 1543, 1549, 1553, 1559, 1567, 1571, 1579, 1583, 1597, 1601,
        1607, 1609, 1613, 1619, 1621, 1627, 1637, 1657, 1663, 1667, 1669, 1693, 1697, 1699, 1709, 1721, 1723, 1733,
        1741, 1747, 1753, 1759, 1777, 1783, 1787, 1789, 1801, 1811, 1823, 1831, 1847, 1861, 1867, 1871, 1873, 1877,
        1879, 1889, 1901, 1907, 1913, 1931, 1933, 1949, 1951, 1973, 1979, 1987, 1993, 1997, 1999, 2003, 2011, 2017,
        2027, 2029, 2039, 2053, 2063, 2069, 2081, 2083, 2087, 2089, 2099, 2111, 2113, 2129, 2131, 2137, 2141, 2143,
        2153, 2161, 2179, 2203, 2207, 2213, 2221, 2237, 2239, 2243, 2251, 2267, 2269, 2273, 2281, 2287, 2293, 2297,
        2309, 2311, 2333, 2339, 2341, 2347, 2351, 2357, 2371, 2377, 2381, 2383, 2389, 2393, 2399, 2411, 2417, 2423,
        2437, 2441, 2447, 2459, 2467, 2473, 2477, 2503, 2521, 2531, 2539, 2543, 2549, 2551, 2557, 2579, 2591, 2593,
        2609, 2617, 2621, 2633, 2647, 2657, 2659, 2663, 2671, 2677, 2683, 2687, 2689, 2693, 2699, 2707, 2711, 2713,
        2719, 2729, 2731, 2741, 2749, 2753, 2767, 2777, 2789, 2791, 2797, 2801, 2803, 2819, 2833, 2837, 2843, 2851,
        2857, 2861, 2879, 2887, 2897, 2903, 2909, 2917, 2927, 2939, 2953, 2957, 2963, 2969, 2971, 2999, 3001, 3011,
        3019, 3023, 3037, 3041, 3049, 3061, 3067, 3079, 3083, 3089, 3109, 3119, 3121, 3137, 3163, 3167, 3169, 3181,
        3187, 3191, 3203, 3209, 3217, 3221, 3229, 3251, 3253, 3257, 3259, 3271, 3299, 3301, 3307, 3313, 3319, 3323,
        3329, 3331, 3343, 3347, 3359, 3361, 3371, 3373, 3389, 3391, 3407, 3413, 3433, 3449, 3457, 3461, 3463, 3467,
        3469, 3491, 3499, 3511, 3517, 3527, 3529, 3533, 3539, 3541, 3547, 3557, 3559, 3571, 3581, 3583, 3593, 3607,
        3613, 3617, 3623, 3631, 3637, 3643, 3659, 3671, 3673, 3677, 3691, 3697, 3701, 3709, 3719, 3727, 3733, 3739,
        3761, 3767, 3769, 3779, 3793, 3797, 3803, 3821, 3823, 3833, 3847, 3851, 3853, 3863, 3877, 3881, 3889, 3907,
        3911, 3917, 3919, 3923, 3929, 3931, 3943, 3947, 3967, 3989, 4001, 4003, 4007, 4013, 4019, 4021, 4027, 4049,
        4051, 4057, 4073, 4079, 4091, 4093, 4099, 4111, 4127, 4129, 4133, 4139, 4153, 4157, 4159, 4177, 4201, 4211,
        4217, 4219, 4229, 4231, 4241, 4243, 4253, 4259, 4261, 4271, 4273, 4283, 4289, 4297, 4327, 4337, 4339, 4349,
        4357, 4363, 4373, 4391, 4397, 4409, 4421, 4423, 4441, 4447, 4451, 4457, 4463, 4481, 4483, 4493, 4507, 4513,
        4517, 4519, 4523, 4547, 4549, 4561, 4567, 4583, 4591, 4597, 4603, 4621, 4637, 4639, 4643, 4649, 4651, 4657,
        4663, 4673, 4679, 4691, 4703, 4721, 4723, 4729, 4733, 4751, 4759, 4783, 4787, 4789, 4793, 4799, 4801, 4813,
        4817, 4831, 4861, 4871, 4877, 4889, 4903, 4909, 4919, 4931, 4933, 4937, 4943, 4951, 4957, 4967, 4969, 4973,
        4987, 4993, 4999, 5003, 5009, 5011, 5021, 5023, 5039, 5051, 5059, 5077, 5081, 5087, 5099, 5101, 5107, 5113,
        5119, 5147, 5153, 5167, 5171, 5179, 5189, 5197, 5209, 5227, 5231, 5233, 5237, 5261, 5273, 5279, 5281, 5297,
        5303, 5309, 5323, 5333, 5347, 5351, 5381, 5387, 5393, 5399, 5407, 5413, 5417, 5419, 5431, 5437, 5441, 5443,
        5449, 5471, 5477, 5479, 5483, 5501, 5503, 5507, 5519, 5521, 5527, 5531, 5557, 5563, 5569, 5573, 5581, 5591,
        5623, 5639, 5641, 5647, 5651, 5653, 5657, 5659, 5669, 5683, 5689, 5693, 5701, 5711, 5717, 5737, 5741, 5743,
        5749, 5779, 5783, 5791, 5801, 5807, 5813, 5821, 5827, 5839, 5843, 5849, 5851, 5857, 5861, 5867, 5869, 5879,
        5881, 5897, 5903, 5923, 5927, 5939, 5953, 5981, 5987, 6007, 6011, 6029, 6037, 6043, 6047, 6053, 6067, 6073,
        6079, 6089, 6091, 6101, 6113, 6121, 6131, 6133, 6143, 6151, 6163, 6173, 6197, 6199, 6203, 6211, 6217, 6221,
        6229, 6247, 6257, 6263, 6269, 6271, 6277, 6287, 6299, 6301, 6311, 6317, 6323, 6329, 6337, 6343, 6353, 6359,
        6361, 6367, 6373, 6379, 6389, 6397, 6421, 6427, 6449, 6451, 6469, 6473, 6481, 6491, 6521, 6529, 6547, 6551,
        6553, 6563, 6569, 6571, 6577, 6581, 6599, 6607, 6619, 6637, 6653, 6659, 6661, 6673, 6679, 6689, 6691, 6701,
        6703, 6709, 6719, 6733, 6737, 6761, 6763, 6779, 6781, 6791, 6793, 6803, 6823, 6827, 6829, 6833, 6841, 6857,
        6863, 6869, 6871, 6883, 6899, 6907, 6911, 6917, 6947, 6949, 6959, 6961, 6967, 6971, 6977, 6983, 6991, 6997,
        7001, 7013, 7019, 7027, 7039, 7043, 7057, 7069, 7079, 7103, 7109, 7121, 7127, 7129, 7151, 7159, 7177, 7187,
        7193, 7207, 7211, 7213, 7219, 7229, 7237, 7243, 7247, 7253, 7283, 7297, 7307, 7309, 7321, 7331, 7333, 7349,
        7351, 7369, 7393, 7411, 7417, 7433, 7451, 7457, 7459, 7477, 7481, 7487, 7489, 7499, 7507, 7517, 7523, 7529,
        7537, 7541, 7547, 7549, 7559, 7561, 7573, 7577, 7583, 7589, 7591, 7603, 7607, 7621, 7639, 7643, 7649, 7669,
        7673, 7681, 7687, 7691, 7699, 7703, 7717, 7723, 7727, 7741, 7753, 7757, 7759, 7789, 7793, 7817, 7823, 7829,
        7841, 7853, 7867, 7873, 7877, 7879, 7883, 7901, 7907, 7919)

    def __init__(self, capacity: int = 8) -> None:
        """
        DO NOT EDIT
        Initializes hash table
        :param capacity: capacity of the hash table
        """
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity

        i = 0
        while HashTable.primes[i] <= self.capacity:
            i += 1
        self.prime_index = i - 1

    def __eq__(self, other: HashTable) -> bool:
        """
        DO NOT EDIT
        Equality operator
        :param other: other hash table we are comparing with this one
        :return: bool if equal or not
        """
        if self.capacity != other.capacity or self.size != other.size:
            return False
        for i in range(self.capacity):
            if self.table[i] != other.table[i]:
                return False
        return True

    def __str__(self) -> str:
        """
        DO NOT EDIT
        Represents the table as a string
        :return: string representation of the hash table
        """
        represent = ""
        bin_no = 0
        for item in self.table:
            represent += "[" + str(bin_no) + "]: " + str(item) + '\n'
            bin_no += 1
        return represent

    __repr__ = __str__

    def _hash_1(self, key: str) -> int:
        """
        ---DO NOT EDIT---
        Converts a string x into a bin number for our hash table
        :param key: key to be hashed
        :return: bin number to insert hash item at in our table, None if key is an empty string
        """
        if not key:
            return None
        hashed_value = 0

        for char in key:
            hashed_value = 181 * hashed_value + ord(char)
        return hashed_value % self.capacity

    def _hash_2(self, key: str) -> int:
        """
        ---DO NOT EDIT---
        Converts a string x into a hash
        :param key: key to be hashed
        :return: a hashed value
        """
        if not key:
            return None
        hashed_value = 0

        for char in key:
            hashed_value = 181 * hashed_value + ord(char)

        prime = HashTable.primes[self.prime_index]

        hashed_value = prime - (hashed_value % prime)
        if hashed_value % 2 == 0:
            hashed_value += 1
        return hashed_value

    def __len__(self) -> int:
        """
        returns the size of the hash table
        :returns: int denoting size of the hash table
        """
        return self.size

    def __setitem__(self, key: str, value: T) -> None:
        """
        sets a value at the keys hashed index
        :param key: string indicating the key
        :param value: the value to set to the key
        :return: None
        """
        self._insert(key, value)

    def __getitem__(self, key: str) -> T:
        """
        gets the value from a key, raises KeyError if the key doesnt exist
        :param key: the key to search
        :returns: the value found at the keys hashed index
        """
        pair = self._get(key)
        if pair is None:
            raise KeyError(f'KeyError: {key}')
        return pair.value

    def __delitem__(self, key: str) -> None:
        """
        deletes a key from the hash map
        :param key: the key to be deleted
        :return none:
        """
        self[key]
        self._delete(key)

    def __contains__(self, key: str) -> bool:
        """
        determines if a certain key is in the hash table
        :param key: the key to find
        :return: bool indicating weather the key is in the table
        """
        return not self._get(key) is None

    def _hash(self, key: str, inserting: bool = False) -> int:
        """
        convert a string key into an integer index
        :param key: the key to be hashed
        :param inserting: bool indicating insertion of element
        :return: int indicating the index to insert
        """
        hashedIndex = self._hash_1(key)
        i=1
        while not self.table[hashedIndex] is None:
            
            if self.table[hashedIndex].deleted and inserting: # guarentee its not none
                break
            if self.table[hashedIndex].key == key:
                break
            hashedIndex = (self._hash_1(key) + i * self._hash_2(key)) % self.capacity
            i += 1
        return hashedIndex

    def _insert(self, key: str, value: T) -> None:
        """
        inserts a key value pair into the hashTable
        :param key: the key to be mapped to a hash table index
        :param value: the value to be added at that index
        :reutrn: None
        """
        if not key in self:
            self.size += 1

        if self.size / self.capacity >= .5:
            self._grow()

        self.table[self._hash(key, True)] = HashNode(key,value)
      
    def _get(self, key: str) -> HashNode:
        """
        find the HashNode with the given key
        :param key: the key of the hashNode to find
        :return: HashNode if found, else None
        """
        return self.table[self._hash(key)]

    def _delete(self, key: str) -> None:
        """
        Deletes a node from a hash table if it exists
        :param key: the key of the node to delete
        :return: None 
        """
        if not self[key] is None:
            node = self.table[self._hash(key)]
            node.deleted = True
            node.value = node.key = None
            self.size -= 1

    def _grow(self) -> None:
        """
        Doubles the capacity of the existing hash table
        :return: None
        """
        self.capacity *= 2 # double the value of capacity
        newTable = HashTable(self.capacity)

        # find new prime for hash 2
        i=0
        while HashTable.primes[i] <= self.capacity:
            i += 1
        self.prime_index = i - 1

        
        # rehash the elements to the new table
        # use hash as static method?
        for pair in self.table:
            if pair is None or pair.deleted:
                continue
            
            newTable[pair.key] = pair.value

        self.table = newTable.table

    def update(self, pairs: List[Tuple[str, T]] = []) -> None:
        """
        updates the key value pairs using an iterable
        :param pairs: the iterable in pairs
        :return: None
        """
        for key, val in pairs:
            self[key] = val

    def keys(self) -> List[str]:
        """
        Makes a list of all the keys in the table
        :return: a list of str keys in the table
        """
        return [pair.key for pair in self.table if not pair is None]
            
    def values(self) -> List[T]:
        """
        Makes a list of all the values in the table
        :return: a list of values in the table
        """
        return [pair.value for pair in self.table if not pair is None]

    def items(self) -> List[Tuple[str, T]]:
        """
        Makes a list of tuples of key value pairs in the table
        :return: a list of tuples containing the key value pairs in the table
        """
        return [(pair.key, pair.value) for pair in self.table if not pair is None]

    def clear(self) -> None:
        """
        Clears the table of HashNodes completely
        :returns: None
        """
        self.table = HashTable(self.capacity).table
        self.size = 0



   
