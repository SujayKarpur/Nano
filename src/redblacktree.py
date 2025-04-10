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


    def direction(self):
        return 0 if self.parent.left is self else 1
    
    def dirchild(self, dir) -> 'Node':
        return self.left if not dir else self.right 



class RedBlackTree:
    
    def __init__(self, root:Node = None):
        self.root: Node = root   
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
        
    

    def delete_helper(self, node: Node) -> None:
        
        if node.left and node.right:
            succ = self._inorder_successor(node)
            node.attrcopy(succ)
            self.delete_helper(succ)

        elif node.left:
            par = node.parent 
            if node == par.left:
                par.left = node.left 
            else:
                par.right = node.left 
            node.left.parent = par 
        
        elif node.right:
            par = node.parent 
            if node == par.left:
                par.left = node.right 
            else:
                par.right = node.right 
            node.right.parent = par 
            node.right.color = Color.BLACK 


        else:

            if self.root == node: 
                return None 
            
            if node.color == Color.RED: 
                if node == node.parent.left:
                    node.parent.left = None 
                else:
                    node.parent.right = None 
            

            else:
    
                parent = node.parent

                dir = node.direction()
                if dir == 0:
                    parent.left = None 
                else:
                    parent.right = None 

                state = "start_balance"
                
                while True:
                    if state == "start_balance":
                        dir = node.direction()
                        sibling = parent.dirchild(1-dir)
                        distant_nephew = sibling.dirchild(1-dir)
                        close_nephew   = sibling.dirchild(dir)
                        
                        if sibling.color == Color.RED:
                            self.rotate(Side.RIGHT if dir else Side.LEFT, parent)
                            parent.color = Color.RED
                            sibling.color = Color.BLACK 
                            sibling = close_nephew
                            
                            distant_nephew = sibling.dirchild(1-dir)
                            if distant_nephew and distant_nephew.color == Color.RED:
                                state = "case_6"
                                continue  # Jump to case_6
                            close_nephew = sibling.child[dir]
                            if close_nephew and close_nephew.color == Color.RED:
                                state = "case_5"
                                continue 
                            
                            sibling.color = Color.RED
                            parent.color = Color.BLACK 
                            return
                        
                        if distant_nephew and distant_nephew.color == Color.RED:
                            state = "case_6"
                            continue
                        
                        if close_nephew and close_nephew.color == Color.RED:
                            state = "case_5"
                            continue
                        
                        if parent.color == Color.RED:
                            sibling.color = Color.RED
                            parent.color = Color.BLACK 
                            return
                        
                        if parent is None:
                            return
                        
                        sibling.color = "RED"
                        node = parent
                        parent = node.parent  
                        continue
                    
                    elif state == "case_5":
                        self.rotate(Side.LEFT if dir else Side.RIGHT,sibling) 
                        sibling.color = Color.RED
                        close_nephew.color = Color.BLACK 
                        distant_nephew = sibling
                        sibling = close_nephew
                        state = "case_6"
                        continue
                    
                    elif state == "case_6":
                        self.rotate(Side.RIGHT if dir else Side.LEFT,parent)
                        sibling.color = parent.color
                        parent.color = Color.BLACK 
                        distant_nephew.color = Color.BLACK 
                        return
 



    def delete(self, key: str) -> None:

        if key not in self: 
            return 
        
        node = self.get(key)
        self.delete_helper(node)
        
        if self.root:
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