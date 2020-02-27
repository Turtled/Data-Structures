from doubly_linked_list import DoublyLinkedList
from collections import OrderedDict 

class LRUCache:
    """
    Our LRUCache class keeps track of the max number of nodes it
    can hold, the current number of nodes it is holding, a doubly-
    linked list that holds the key-value entries in the correct
    order, as well as a storage dict that provides fast access
    to every node stored in the cache.
    """
    def __init__(self, limit=10):
        self.limit = limit
        #where we keep the actual cached nodes
        self.cached_nodes = DoublyLinkedList()
        #a dictionary to help grab nodes out of the dll cache, so we don't have to "next" through the cache to find specific nodes 
        self.cache_lookup = OrderedDict()
        self.count = 0


    """
    Retrieves the value associated with the given key. Also
    needs to move the key-value pair to the end of the order
    such that the pair is considered most-recently used.
    Returns the value associated with the key or None if the
    key-value pair doesn't exist in the cache.
    """
    def get(self, key):
        if key in self.cache_lookup:
            node = self.cache_lookup[key]
            self.cached_nodes.move_to_end(node)#most recently used
            #update the order of our OrderedDict too by deleting and re-adding at end
            del self.cache_lookup[key]
            self.cache_lookup[key] = node
            return node.value
        else:
            return None

    """
    Adds the given key-value pair to the cache. The newly-
    added pair should be considered the most-recently used
    entry in the cache. If the cache is already at max capacity
    before this entry is added, then the oldest entry in the
    cache needs to be removed to make room. Additionally, in the
    case that the key already exists in the cache, we simply
    want to overwrite the old value associated with the key with
    the newly-specified value.
    """
    def set(self, key, value):

        self.count += 1
        if self.count > self.limit:
            self.count = self.limit

        if key in self.cache_lookup:
            #the key already exists in the cache, lets just update the value
            self.cache_lookup[key].value = value
            return

        print("ATTEMPTING TO ADD " + value + " TO CACHE: " + str(self.cached_nodes))

        if len(self.cached_nodes) >= self.limit:


            print("ADDING TO CACHE WHILE FULL")

            self.cached_nodes.remove_from_head()#head is the last used

            #Is there some way to remove our cache lookup without looping over it? If we don't old cache values are just going 
            #to pile up and not get garbage collected since cache_lookup still contains the ListNode, but there must be a better way to remove the least used... OrderedDict?
            # nodeToDelete
            # for node in self.cache_lookup:
            #     #print(self.cache_lookup[node].value + " == " + removedNode + "?")
            #     if self.cache_lookup[node] == removedNode:
            #         nodesToDelete.append(node)

            # del self.cache_lookup[nodeToDelete]
            self.cache_lookup.popitem(False)#will remove index 0 which is the oldest

            newNode = self.cached_nodes.add_to_tail(value)
            self.cache_lookup[key] = newNode

        else:
            #add key to our cache lookup, and set its value to the new node created and added to the tail (tail is most recently used) of the dll
            self.cache_lookup[key] = self.cached_nodes.add_to_tail(value)


        print("RESULT: " + str(self.cached_nodes))
        for i in self.cache_lookup:
            print("Cache lookup: " + self.cache_lookup[i].value)

        
