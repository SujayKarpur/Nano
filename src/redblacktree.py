from enum import Enum 
from typing import Optional
from collections import deque 
from functools import total_ordering
from copy import deepcopy 



Maybe_node = Optional['Node']

class Color(Enum):
    RED = 0 
    BLACK = 1 

class Side(Enum):
    LEFT = 0 
    RIGHT = 1 

class TraversalType(Enum):
    PREORDER = 1 
    INORDER = 2 
    POSTORDER = 3 
    LEVELORDER = 4 


@total_ordering
class Node:
    
    def __init__(self, color: Color, key: str, value: str, parent: 'Node', left: Maybe_node = None, right: Maybe_node = None) -> None:
        self.color = color  
        self.key = key 
        self.value = value 
        self.parent = parent
        self.left = left 
        self.right = right  

    def __repr__(self) -> str:
        return f"{self.key}: {self.value}   ({self.color.name})"

    def __eq__(self, other: 'Node'):
        if self and not other:
            return False 
        if other and not self:
            return False 
        if not other and not self:
            return True 
        return self.key == other.key 

    def __lt__(self, other: 'Node'):
        return str.__lt__(self.key, other.key)
    


class RedBlackTree:
    
    def __init__(self):
        self.root: Node = None  
        self.size: int = 0 

    def insert(self, key: str, value: str):
        new = Node(Color.RED, key, value, None)

        if self.size == 0:
            new.color = Color.BLACK
            self.root = new 
        elif self.size == 1:
            if new > self.root:
                self.root.right = new 
                new.parent = self.root 
            elif new < self.root: 
                self.root.left = new 
                new.parent = self.root 
            else:
                self.root.value = value 
        else:
            
            current: Node = self.root 

            while not (not current.left and new < current) and not (not current.right and new > current):
                if new > current:
                    current = current.right 
                elif new < current:
                    current = current.left 
                else:
                    current.value = new.value 
                    return  
            
            if new > current:
                current.right = new 
                new.parent = current 
            else: 
                current.left = new 
                new.parent = current 

            x: Node = new 
            if not self.uncle(x) or self.uncle(x).color == Color.BLACK:
                if x.parent == self.grandparent(x).left: 
                    self.rotate(Side.LEFT, x)
                    if x == x.parent.right:
                        self.rotate(Side.RIGHT, x) 
                else:
                    self.rotate(Side.LEFT, self.grandparent(x))
                    if x == x.parent.left:
                        self.rotate(Side.LEFT, x)  
            else:
                while x != self.root and x.parent.color != Color.BLACK:
                    x.parent.color = self.uncle(x).color = Color.BLACK 
                    self.grandparent(x).color = Color.RED
                    x = self.grandparent(x) 
        
        self.size += 1 



    def __contains__(self, key: str) -> bool:
        current: Node = self.root 
        while current and current.key != key:
            if current.key > key:
                current = current.left 
            elif current.key < key:
                current = current.right 
            else: 
                return True 
        return False  

    def delete(self, key: str):
        pass  

    #helper methods 

    def parent(self, node: Node) -> Maybe_node:
        return node.parent  

    def sibling(self, node: Node) -> Maybe_node:
        if node.parent:
            if node.parent.left and node.parent.left == node:
                return node.right 
            else:
                return node.left 
        else:
            return None 

    def grandparent(self, node: Node) -> Maybe_node:
        if node.parent:
            return node.parent.parent 
        return None  

    def uncle(self, node: Node) -> Maybe_node:
        return self.sibling(node.parent) 


    def rotate(self, side: Side, pivot: Node) -> None:
        
        if side == Side.RIGHT:
            old_parent = pivot.parent 
            old_right = pivot.right 
            pivot.parent = self.grandparent(pivot)
            pivot.right = old_parent
            old_parent.parent = pivot 
            old_parent.left = old_right 

        else:       
            old_parent = pivot.right 
            pivot.right = old_parent.left 
            pivot.parent = old_parent
            old_parent.left = pivot 

            if pivot == self.root:
                self.root = old_parent

    def traverse(self, type: TraversalType):
        match type:
            case TraversalType.PREORDER:
                return self._preorder_traversal_helper(self.root)
            case TraversalType.INORDER:
                return self._inorder_traversal_helper(self.root)
            case TraversalType.POSTORDER:
                return self._postorder_traversal_helper(self.root)
            case TraversalType.LEVELORDER:
                return self._levelorder_traversal_helper(self.root)
    

    def _preorder_traversal_helper(self, root: Node):
        if not root:
            return [] 
        return [root] + self._preorder_traversal_helper(root.left) + self._preorder_traversal_helper(root.right)

    def _inorder_traversal_helper(self, root: Node):
        if not root:
            return []
        return self._inorder_traversal_helper(root.left) + [root] + self._inorder_traversal_helper(root.right)

    def _postorder_traversal_helper(self, root: Node):
        if not root:
            return []
        return self._postorder_traversal_helper(root.left) + self._postorder_traversal_helper(root.right) + [root] 

    def _levelorder_traversal_helper(self, root: Node):
        if not root:
            return []
        queue = [root]
        future = []
        traversal = [[]]
        while queue:
            x = queue.pop(0)
            traversal[-1].append(x)
            if x.left:
                future.append(x.left)
            if x.right:
                future.append(x.right)
            
            if not queue:
                queue = future 
                traversal.append([])

        return traversal
    

    def __repr__(self) -> str:
        s = ""
        for x in self._levelorder_traversal_helper(self.root):
            s += ' '.join(map(str,x)) + '\n'
        return s 