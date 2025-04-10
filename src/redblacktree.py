from enum import Enum 
from typing import Optional, List 
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
    
    def attrcopy(self, other: 'Node') -> None:
        self.key = other.key 
        self.value = other.value 
        #self.color = other.color 



class RedBlackTree:
    
    def __init__(self, root:Node = None):
        self.root: Node = root   
        self.size: int = 0 


    def _bstinsert(self, key: str, value: str):
        pass 



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
                print(x.parent, x.parent.parent, x.parent.parent.left, self.uncle(x))
                if x.parent == self.grandparent(x).left: 
                    if x == x.parent.right:
                        self.rotate(Side.LEFT, x.parent)
                        self.rotate(Side.RIGHT, self.grandparent(x)) 
                    else:
                        self.rotate(Side.LEFT, self.grandparent(x))
                else:
                    if x == x.parent.left:
                        self.rotate(Side.RIGHT, x.parent)
                        self.rotate(Side.LEFT, self.grandparent(x))  
                    else:
                        self.rotate(Side.LEFT, self.grandparent(x))
            else:
                print('red uncle!!')
                while x != self.root and x.parent.color != Color.BLACK:
                    x.parent.color = Color.BLACK; self.uncle(x).color = Color.BLACK 
                    self.grandparent(x).color = Color.RED
                    x = self.grandparent(x) 
                self.root.color = Color.BLACK 
        
        self.size += 1 



    def __contains__(self, key: str) -> bool:
        current: Node = self.root 
        while current:
            if current.key > key:
                current = current.left 
            elif current.key < key:
                current = current.right 
            else: 
                return True 
        return False  
    
    def get(self, key: str) -> Node:
        current: Node = self.root 
        while current:
            if current.key > key:
                current = current.left 
            elif current.key < key:
                current = current.right 
            else: 
                return current  

    def _bst_delete(self, root: Node, node: Node) -> Node:
        
        if root == None:
            return None 
        
        if node > root:
            root.right = self._bst_delete(root.right, node)
            return root 

        elif node < root:
            root.left = self._bst_delete(root.left, node)
            return root  

        else:
            if not root.left and not root.right:
                return None 
            
            if not root.right:
                return root.left 
            
            if not root.left:
                return root.right 
            
            f = self._inorder_successor(root)
            root.attrcopy(f)
            f = self._bst_delete(f,f)

            return root 
        
    
    def blackblackfix(self, ):
        pass 

    def delete_helper(self, node: Node) -> None:
        
        if node.left and node.right:
            succ = self._inorder_successor(node)
            node.attrcopy(succ)
            self.delete_helper(succ)

        if node.left:
            node.left.color = 1

    def delete(self, key: str) -> None:

        if key not in self: 
            return 
        
        node = self.get(key)
        self.delete_helper(node)
        

        if node.left and node.right:
            succ = self._inorder_successor(node)
            node.attrcopy(succ)
            self.delete()

        if not node.left and not node.right:
            self.root = self._bst_delete(self.root, node) 
        elif not node.right:
            self.root = self._bst_delete(self.root, node) 
            if node.color == Color.BLACK:
                if node.left.color == Color.RED:
                    node.left.color = Color.BLACK 
                else:
                    pass 
        else:
            self.root = self._bst_delete(self.root, node)
            f = self._inorder_successor(node)
            if node.color == Color.BLACK:
                if f.color == Color.BLACK:
                    pass 
                else:
                    f.color = Color.RED  
        


        self.root.color = Color.BLACK
        self.size -= 1   

    #helper methods 

    def parent(self, node: Node) -> Maybe_node:
        current: Node = self.root 

        if node == current:
            return None 

        while current: 
            if (current.left and current.left == node) or (current.right and current.right == node):
                return current 
            if node > current:
                current = current.right 
            elif node < current:
                current = current.left 

        return None 

    def sibling(self, node: Node) -> Maybe_node:
        if self.parent(node):
            if self.parent(node).left and self.parent(node).left == node:
                return self.parent(node).right 
            else:
                return self.parent(node).left 
        else:
            return None 

    def grandparent(self, node: Node) -> Maybe_node:
        if self.parent(node):
            return self.parent(self.parent(node)) 
        return None  

    def uncle(self, node: Node) -> Maybe_node:
        return self.sibling(self.parent(node)) 


    def rotate(self, side: Side, pivot: Node) -> None:
        
        if side == Side.RIGHT:
            if pivot != self.root:
                skuh = pivot.parent 
            old_parent = pivot.left 
            pivot.left = old_parent.right  
            pivot.parent = old_parent
            old_parent.right = pivot 
            pivot.color, old_parent.color = old_parent.color, pivot.color

            
            if pivot == self.root:
                self.root = old_parent
            else:
                old_parent.parent = skuh 
                if skuh.right == pivot:
                    skuh.right = old_parent 
                else:
                    skuh.left = old_parent

        else:       
            if pivot != self.root:
                skuh = pivot.parent 
            old_parent = pivot.right 
            pivot.right = old_parent.left 
            pivot.parent = old_parent
            old_parent.left = pivot 
            pivot.color, old_parent.color = old_parent.color, pivot.color

            if pivot == self.root:
                self.root = old_parent
            else:
                old_parent.parent = skuh 
                if skuh.right == pivot:
                    skuh.right = old_parent
                else:
                    skuh.left = old_parent



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
    


    def _preorder_traversal_helper(self, root: Node) -> List[Node]:
        if not root:
            return [] 
        return [root] + self._preorder_traversal_helper(root.left) + self._preorder_traversal_helper(root.right)


    def _inorder_traversal_helper(self, root: Node) -> List[Node]:
        if not root:
            return []
        return self._inorder_traversal_helper(root.left) + [root] + self._inorder_traversal_helper(root.right)


    def _postorder_traversal_helper(self, root: Node) -> List[Node]:
        if not root:
            return []
        return self._postorder_traversal_helper(root.left) + self._postorder_traversal_helper(root.right) + [root] 


    def _levelorder_traversal_helper(self, root: Node) -> List[Node]:
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
                queue = future.copy() 
                traversal.append([])
                future = []

        return traversal
    



    def __repr__(self) -> str:
        s = ""
        for x in self._levelorder_traversal_helper(self.root):
            s += ' '.join(map(str,x)) + '\n'
        return s 
    


    def _inorder_successor(self, node: Node) -> Node:
        array = self._inorder_traversal_helper(self.root)
        try:
            i = array.index(node)
            if i == self.size-1:
                return None 
            else:
                return array[i+1]
        except:
            return None 

    def _inorder_predecessor(self, node: Node) -> Node:
        array = self._inorder_traversal_helper(self.root)
        try:
            i = array.index(node)
            if i == 0:
                return None 
            else:
                return array[i-1]
        except:
            return None 