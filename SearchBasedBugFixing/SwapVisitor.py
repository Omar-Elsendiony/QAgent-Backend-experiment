import ast
from random import choices
from .utils import parentify

def isInBody(node):
    parentBody = node.parent.body
    if (isinstance(parentBody, list)):
        for child in parentBody:
            if (child is node):
                return True
    else:
        if (parentBody is node):
            return True
    return False

class SwapVisitor(ast.NodeVisitor):
    countNodes = 0
    handleLst = [] # handles for candidates that can be swaped in the body of the parent node
    def visit(self, node):
        if (hasattr(node.parent, 'body') and node.__class__.__name__ != "FunctionDef" and node.__class__.__name__ != "Name"):  # check if it falls directly under a node that has body attr that can encompass it
            if (isInBody(node)):
                self.handleLst.append(node)
        return super().visit(node)







def swapNodes(parent_node):
    parentify(parent_node)
    changed = False
    upperLimit = 10
    u = 0
    SwapVisitor().visit(parent_node)
    candidates = SwapVisitor.handleLst
    while (not changed and u < upperLimit):
        u += 1
        cand_dash = choices(candidates, k=2)
        if (cand_dash[0].parent.__class__.__name__ == cand_dash[1].parent.__class__.__name__):
            try:
                cand_dash[0].parent.body[cand_dash[0].parent.body.index(cand_dash[0])], cand_dash[1].parent.body[cand_dash[1].parent.body.index(cand_dash[1])] = cand_dash[1], cand_dash[0]
                changed = True
            except: pass
    try:
        ast.unparse(parent_node)
    except:
        return False
    return True
        
