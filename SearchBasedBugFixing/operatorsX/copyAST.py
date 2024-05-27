import ast

class copyMutation(ast.NodeTransformer):

    def visit_Module(self, node):
        return ast.copy_location(ast.Module(body=[self.visit(x) for x in node.body]), node)

    def visit_Num(self, node):
        return ast.copy_location(ast.Constant(n=node.n), node)
    
    def visit_Expression(self, node):
        return ast.copy_location(ast.Expression(body=self.visit(node.body)), node)

    def visit_Expr(self, node):
        return ast.copy_location(ast.Expr(value=self.visit(node.value)), node)
    
    def visit_NamedExpr(self, node):
        return ast.copy_location(ast.NamedExpr(target=self.visit(node.target), value=self.visit(node.value)), node)

    def visit_Constant(self, node):
        return ast.copy_location(ast.Constant(n=node.n), node)

    def visit_Str(self, node):
        return ast.copy_location(ast.Constant(s=node.s), node)

    def visit_Name(self, node):
        return ast.copy_location(ast.Name(id=node.id, ctx=node.ctx), node)

    def visit_List(self, node):
        return ast.copy_location(ast.List(elts=[self.visit(x) for x in node.elts], ctx=node.ctx), node)

    def visit_Tuple(self, node):
        return ast.copy_location(ast.Tuple(elts=[self.visit(x) for x in node.elts], ctx=node.ctx), node)

    def visit_Set(self, node):
        return ast.copy_location(ast.Set(elts=[self.visit(x) for x in node.elts], ctx=node.ctx), node)

    def visit_Dict(self, node):
        return ast.copy_location(ast.Dict(keys=[self.visit(x) for x in node.keys], values=[self.visit(x) for x in node.values]), node)

    def visit_Attribute(self, node):
        return ast.copy_location(ast.Attribute(value=self.visit(node.value), attr=node.attr, ctx=node.ctx), node)

    def visit_Subscript(self, node):
        return ast.copy_location(ast.Subscript(value=self.visit(node.value), slice=self.visit(node.slice), ctx=node.ctx), node)

    def visit_Index(self, node):
        return ast.copy_location(ast.Index(value=self.visit(node.value)), node)

    def visit_Slice(self, node):
        lower = None if node.lower is None else self.visit(node.lower)
        upper = None if node.upper is None else self.visit(node.upper)
        step = None if node.step is None else self.visit(node.step)
        return ast.copy_location(ast.Slice(lower=lower, upper=upper, step=step), node)

    def visit_ExtSlice(self, node):
        return ast.copy_location(ast.ExtSlice(dims=[self.visit(x) for x in node.dims]), node)

    def visit_IfExp(self, node):
        return ast.copy_location(ast.IfExp(test=self.visit(node.test), body=self.visit(node.body), orelse=self.visit(node.orelse)), node)

    def visit_Compare(self, node):
        ops = [self.visit(op) for op in node.ops]
        return ast.copy_location(ast.Compare(left=self.visit(node.left), ops=ops, comparators=[self.visit(x) for x in node.comparators]), node)

    def visit_Call(self, node):
        return ast.copy_location(ast.Call(func=self.visit(node.func), args=[self.visit(x) for x in node.args], keywords=[self.visit(x) for x in node.keywords]), node)
    
    def visit_keyword(self, node):
        return ast.copy_location(ast.keyword(arg=node.arg, value=self.visit(node.value)), node)
    
    def visit_Starred(self, node):
        return ast.copy_location(ast.Starred(value=self.visit(node.value), ctx=node.ctx), node)
    
    def visit_NameConstant(self, node):
        return ast.copy_location(ast.Constant(value=node.value), node)
    
    def visit_UnaryOp(self, node):
        return ast.copy_location(ast.UnaryOp(op=node.op, operand=self.visit(node.operand)), node)
    
    def visit_BinOp(self, node):
        try:
            l = None if node.left is None else self.visit(node.left)
            r = None if node.right is None else self.visit(node.right)
        except:
            return node
        return ast.copy_location(ast.BinOp(left=l, op=node.op, right=r), node)
    
    def visit_BoolOp(self, node):
        return ast.copy_location(ast.BoolOp(op=node.op, values=[self.visit(x) for x in node.values]), node)
    
    def visit_If(self, node):
        return ast.copy_location(ast.If(test=self.visit(node.test), body=[self.visit(x) for x in node.body], orelse=[self.visit(x) for x in node.orelse]), node)
    
    def visit_For(self, node):
        return ast.copy_location(ast.For(target=self.visit(node.target), iter=self.visit(node.iter), body=[self.visit(x) for x in node.body], orelse=[self.visit(x) for x in node.orelse]), node)
    
    def visit_While(self, node):
        return ast.copy_location(ast.While(test=self.visit(node.test), body=[self.visit(x) for x in node.body], orelse=[self.visit(x) for x in node.orelse]), node)
    
    def visit_With(self, node):
        return ast.copy_location(ast.With(items=[self.visit(x) for x in node.items], body=[self.visit(x) for x in node.body]), node)
    
    def visit_withitem(self, node):
        return ast.copy_location(ast.withitem(context_expr=self.visit(node.context_expr), optional_vars=self.visit(node.optional_vars)), node)
    
    def visit_FunctionDef(self, node):
        returns = None if node.returns is None else self.visit(node.returns)
        args = None if node.args is None else self.visit(node.args)
        return ast.copy_location(ast.FunctionDef(name=node.name, args=args, body=[self.visit(x) for x in node.body], decorator_list=[self.visit(x) for x in node.decorator_list], returns=returns), node)
    
    def visit_Lambda(self, node):
        return ast.copy_location(ast.Lambda(args=self.visit(node.args), body=self.visit(node.body)), node)
    
    def visit_arguments(self, node):
        vararg = None if node.vararg is None else self.visit(node.vararg)
        kwarg = None if node.kwarg is None else self.visit(node.kwarg)
        return ast.copy_location(ast.arguments(posonlyargs=[self.visit(x) for x in node.posonlyargs], args=[self.visit(x) for x in node.args], vararg=vararg, kwonlyargs=[self.visit(x) for x in node.kwonlyargs], kw_defaults=[self.visit(x) for x in node.kw_defaults], kwarg=kwarg, defaults=[self.visit(x) for x in node.defaults]), node)
    
    def visit_arg(self, node):
        if node is None:
            return None
        annotation = None if node.annotation is None else self.visit(node.annotation)
        return ast.copy_location(ast.arg(arg=node.arg, annotation=annotation), node)
    
    def visit_Return(self, node):
        val = None if (node.value is None) else self.visit(node.value)
        return ast.copy_location(ast.Return(value=val), node)
    
    def visit_Delete(self, node):
        return ast.copy_location(ast.Delete(targets=[self.visit(x) for x in node.targets]), node)
    
    def visit_Assign(self, node):
        return ast.copy_location(ast.Assign(targets=[self.visit(x) for x in node.targets], value=self.visit(node.value)), node)
    
    def visit_AnnAssign(self, node):
        return ast.copy_location(ast.AnnAssign(target=self.visit(node.target), annotation=self.visit(node.annotation), value=self.visit(node.value), simple=node.simple), node)
    
    def visit_AugAssign(self, node):
        return ast.copy_location(ast.AugAssign(target=self.visit(node.target), op=node.op, value=self.visit(node.value)), node)
    
    def visit_Print(self, node):
        return ast.copy_location(ast.Print(dest=self.visit(node.dest), values=[self.visit(x) for x in node.values], nl=node.nl), node)
    
    def visit_Raise(self, node):
        return ast.copy_location(ast.Raise(exc=self.visit(node.exc), cause=self.visit(node.cause)), node)
    
    def visit_Assert(self, node):
        return ast.copy_location(ast.Assert(test=self.visit(node.test), msg=self.visit(node.msg)), node)
    
    def visit_Import(self, node):
        return ast.copy_location(ast.Import(names=[self.visit(x) for x in node.names]), node)
    
    def visit_ImportFrom(self, node):
        return ast.copy_location(ast.ImportFrom(module=node.module, names=[self.visit(x) for x in node.names], level=node.level), node)
    
    def visit_alias(self, node):
        return ast.copy_location(ast.alias(name=node.name, asname=node.asname), node)
    
    def visit_Exec(self, node):
        return ast.copy_location(ast.Exec(body=self.visit(node.body), globals=self.visit(node.globals), locals=self.visit(node.locals)), node)
    
    def visit_Global(self, node):
        return ast.copy_location(ast.Global(names=[self.visit(x) for x in node.names]), node)
    
    def visit_Nonlocal(self, node):
        return ast.copy_location(ast.Nonlocal(names=[self.visit(x) for x in node.names]), node)
    
    def visit_Pass(self, node):
        return ast.copy_location(ast.Pass(), node)
    
    def visit_Break(self, node):
        return ast.copy_location(ast.Break(), node)
    
    def visit_Continue(self, node):
        return ast.copy_location(ast.Continue(), node)
    
    def visit_Try(self, node):
        return ast.copy_location(ast.Try(body=[self.visit(x) for x in node.body], handlers=[self.visit(x) for x in node.handlers], orelse=[self.visit(x) for x in node.orelse], finalbody=[self.visit(x) for x in node.finalbody]), node)
    
    def visit_ExceptHandler(self, node):
        return ast.copy_location(ast.ExceptHandler(type=self.visit(node.type), name=node.name, body=[self.visit(x) for x in node.body]), node)
    
    def visit_ClassDef(self, node):
        return ast.copy_location(ast.ClassDef(name=node.name, bases=[self.visit(x) for x in node.bases], keywords=[self.visit(x) for x in node.keywords], body=[self.visit(x) for x in node.body], decorator_list=[self.visit(x) for x in node.decorator_list]), node)
    
    def visit_keyword(self, node):
        return ast.copy_location(ast.keyword(arg=node.arg, value=self.visit(node.value)), node)
    
    def visit_BitAnd(self, node: ast.BitAnd):
        return ast.copy_location(ast.BitAnd(), node)
    
    def visit_BitOr(self, node: ast.BitOr):
        return ast.copy_location(ast.BitOr(), node)
    
    def visit_BitXor(self, node: ast.BitXor):
        return ast.copy_location(ast.BitXor(), node)
    
    def visit_Invert(self, node: ast.Invert):
        return ast.copy_location(ast.Invert(), node)
    
    def visit_LShift(self, node: ast.LShift):
        return ast.copy_location(ast.LShift(), node)
    
    def visit_RShift(self, node: ast.RShift):
        return ast.copy_location(ast.RShift(), node)
    
    def visit_UAdd(self, node: ast.UAdd):
        return ast.copy_location(ast.UAdd(), node)
    
    def visit_USub(self, node: ast.USub):
        return ast.copy_location(ast.USub(), node)
    
    def visit_And(self, node: ast.And):
        return ast.copy_location(ast.And(), node)
    
    def visit_Or(self, node: ast.Or):
        return ast.copy_location(ast.Or(), node)
    
    def visit_Add(self, node: ast.Add):
        return ast.copy_location(ast.Add(), node)
    
    def visit_Div(self, node: ast.Div):
        return ast.copy_location(ast.Div(), node)
    
    def visit_FloorDiv(self, node: ast.FloorDiv):
        return ast.copy_location(ast.FloorDiv(), node)
    
    def visit_Mod(self, node: ast.Mod):
        return ast.copy_location(ast.Mod(), node)
    
    def visit_Mult(self, node: ast.Mult):
        return ast.copy_location(ast.Mult(), node)
    
    def visit_Pow(self, node: ast.Pow):
        return ast.copy_location(ast.Pow(), node)
    
    def visit_Sub(self, node: ast.Sub):
        return ast.copy_location(ast.Sub(), node)
    
    def visit_Eq(self, node: ast.Eq):
        return ast.copy_location(ast.Eq(), node)
    
    def visit_Gt(self, node: ast.Gt):
        return ast.copy_location(ast.Gt(), node)
    
    def visit_GtE(self, node: ast.GtE):
        return ast.copy_location(ast.GtE(), node)
    
    def visit_Lt(self, node: ast.Lt):
        return ast.copy_location(ast.Lt(), node)
    
    def visit_LtE(self, node: ast.LtE):
        return ast.copy_location(ast.LtE(), node)
    
    def visit_NotEq(self, node: ast.NotEq):
        return ast.copy_location(ast.NotEq(), node)
    
    def visit_Is(self, node: ast.Is):
        return ast.copy_location(ast.Is(), node)
    
    def visit_IsNot(self, node: ast.IsNot):
        return ast.copy_location(ast.IsNot(), node)
    
    def visit_In(self, node: ast.In):
        return ast.copy_location(ast.In(), node)
    
    def visit_NotIn(self, node: ast.NotIn):
        return ast.copy_location(ast.NotIn(), node)
    
    def visit_comprehension(self, node: ast.comprehension):
        return ast.copy_location(ast.comprehension(target=self.visit(node.target), iter=self.visit(node.iter), ifs=[self.visit(x) for x in node.ifs]), node)
    
    def visit_MatchAs(self, node: ast.MatchAs):
        return ast.copy_location(ast.MatchAs(), node)
    
    def visit_MatchMapping(self, node: ast.MatchMapping):
        return ast.copy_location(ast.MatchMapping(), node)
    
    def visit_MatchSequence(self, node: ast.MatchSequence):
        return ast.copy_location(ast.MatchSequence(), node)
    
    def visit_MatchStar(self, node: ast.MatchStar):
        return ast.copy_location(ast.MatchStar(), node)
    
    def visit_MatchValue(self, node: ast.MatchValue):
        return ast.copy_location(ast.MatchValue(), node)
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        return ast.copy_location(ast.AsyncFunctionDef(), node)
    
    def visit_AsyncFor(self, node: ast.AsyncFor):
        return ast.copy_location(ast.AsyncFor(), node)
    
    def visit_AsyncWith(self, node: ast.AsyncWith):
        return ast.copy_location(ast.AsyncWith(), node)
    
    def visit_Yield(self, node: ast.Yield):
        return ast.copy_location(ast.Yield(), node)
    
    def visit_YieldFrom(self, node: ast.YieldFrom):
        return ast.copy_location(ast.YieldFrom(), node)
    
    