"""
File: linkedbst.py
Author: Ken Lambert
"""


import random
from math import log
from time import time
from copy import deepcopy
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            _string = ""
            if node is not None:
                _string += recurse(node.right, level + 1)
                _string += "| " * level
                _string += str(node.data) + "\n"
                _string += recurse(node.left, level + 1)
            return _string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return lyst

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right is None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if item not in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while current_node.right is not None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while current_node is not None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if current_node.left is not None \
                and current_node.right is not None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self, cur=None):
        '''
        Return the height of tree
        :return: int
        '''

        if cur is None:
            if self._root is not None:
                cur = self._root
            else:
                return 0

        def _height1(cur):
            '''
            Helper function
            :param top:
            :return:
            '''
            children = []
            if cur.left is not None:
                children.append(cur.left)
            if cur.right is not None:
                children.append(cur.right)
            if self.is_leaf(cur):
                return 0
            else:
                return 1 + max(_height1(child) for child in children)

        return _height1(cur)

    def is_leaf(self, item):
        """Function that check whether it is a leaf."""
        if item.right is None and item.left is None:
            return True

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        amount_of_node = len(self.inorder())
        height_tree = self.height()
        if height_tree == 0:
            return True
        return height_tree < ((2 * log(amount_of_node + 1, 2)) - 1)

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        correct_elems = []
        elements = self.inorder()
        for item in elements:
            if low <= item <= high:
                correct_elems.append(item)
        return correct_elems

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        elements = self.inorder()
        self.clear()

        def recurse(elems):
            if len(elems) == 0:
                return
            mid = len(elems) // 2
            self.add(elems[mid])
            recurse(elems[:mid])
            recurse(elems[mid + 1:])
        recurse(elements)
        return

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        elems = self.inorder()
        for each in elems:
            if each > item:
                return each
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        elems = reversed(self.inorder())
        for each in elems:
            if each < item:
                return each
        return None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        all_words = self.reading_file(path)
        random_words = self.finding_random(all_words)
        copied_words = deepcopy(all_words)
        shuffled_words = random.shuffle(copied_words)
        shuffled_tree = self.creating_tree_shuffled(shuffled_words)
        time_1 = self.time_sorted_lst(random_words, all_words)
        time_2 = self.time_from_sorted_tree(self.creating_tree_sorted(all_words), random_words)
        time_3 = self.time_from_shuffled_tree(shuffled_tree, random_words)
        time_4 = self.time_from_shuffled_tree(shuffled_tree, random_words)
        print("")
        print(f"Finding 10000 random words in sorted lst: {time_1}", "\n")
        print(f"Finding 10000 random words in tree based on sorted list: {time_2}", "\n")
        print(f"Finding 10000 random words in tree based on shuffled list: {time_3}", "\n")
        shuffled_tree.rebalance()
        print(f"Finding 10000 random words in tree, that was balanced and based on \
shuffled list: {time_4}", "\n")
    
    def reading_file(self, path: str):
        """
        Function that reads the file and returns list of the words.
        Args:
            path (str)

        Returns:
            List
        """
        all_words = []
        with open(path, "r") as file:
            for item in file:
                all_words.append(item.split())
        return all_words

    def finding_random(self, lst: list):
        """
        Function for finding random words from the list.
        Args:
            lst (list)

        Returns:
            List of random words.
        """
        random_words = []
        for item in range(10000):
            random_words.append(random.choice(lst))
        return random_words

    def time_sorted_lst(self, random_lst: list, general_lst: list):
        """
        Function that finds random words in sorted list and time of execution.
        Args:
            random_lst (list)
            general_lst (list)

        Returns:
            Time for which it finds random words in the sorted list.
        """
        time1 = time()
        for item in random_lst:
            general_lst.index(item)
        time2 = time()
        return time2 - time1
    
    def creating_tree_sorted(self, all_words: list):
        """
        Function for creating tree from sorted list of words.
        Args:
            all_words (list)

        Returns:
            object LinkedBST
        """
        return LinkedBST(all_words[:1000])
    
    def time_from_sorted_tree(self, other: object, random_lst: list):
        """
        Function that finds random words in tree, which is created from
        sorted list of words, and time of execution.
        Args:
            other (object): LinkedBST
            random_lst (list)

        Returns:
            Time of the execution.
        """
        time1 = time()
        for item in random_lst:
            other.find(item)
        time2 = time()
        return (time2 - time1) * 240
    
    def creating_tree_shuffled(self, shuffled_words: list):
        """
        Function that creates tree which values based on shuffled list.
        Args:
            shuffled_words (list)

        Returns:
            object LinkedBST
        """
        return LinkedBST(shuffled_words)
    
    def time_from_shuffled_tree(self, other: object, random_lst: list):
        """
        Function that finds random words in tree, which is created from
        shuffled list of words and was balanced, and time of execution. 
        Args:
            other (object):
            random_lst (list):

        Returns:
            Time of the execution.
        """
        time1 = time()
        for item in random_lst:
            other.find(item)
        time2 = time()
        return time2 - time1
