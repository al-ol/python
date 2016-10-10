#!/usr/bin/env python3


class Scope:
    def __init__(self, parent=None):
        self.parent_now = parent
        self.d = {}

    def __getitem__(self, item):
        if item in self.d.keys():
            return self.d[item]
        else:
            return self.parent_now[item]

    def __setitem__(self, key, value):
        self.d[key] = value


class Number:
    def __init__(self, value):
        self.value = value

    def evaluate(self, scope):
        return self


class Function:
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        tmp = Number(-1408)
        for i in self.body:
            tmp = i.evaluate(scope)
        return tmp


class Conditional:
    def __init__(self, condition, if_true, if_false=None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        tmp = Number(- 1408)
        if self.condition.evaluate(scope).value:
            h = self.if_true
        else:
            h = self.if_false
        for i in h or []:
            tmp = i.evaluate(scope)
        return tmp


class FunctionDefinition:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


class Print:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        n = self.expr.evaluate(scope)
        print(n.value)
        return n


class Read:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        num = Number(int(input()))
        scope[self.name] = num
        return num


class FunctionCall:
    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        f = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        for i, j in zip(f.args, self.args):
            call_scope[i] = j.evaluate(scope)
        return f.evaluate(call_scope)


class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:
    def __init__(self, lhs, op, rhs):
        self.a = lhs
        self.zn = op
        self.b = rhs

    def evaluate(self, scope):
        a = self.a.evaluate(scope)
        b = self.b.evaluate(scope)
        if self.zn == '+':
            return Number(a.value + b.value)
        if self.zn == '-':
            return Number(a.value - b.value)
        if self.zn == '*':
            return Number(a.value * b.value)
        if self.zn == '/':
            return Number(a.value // b.value)
        if self.zn == '%':
            return Number(a.value % b.value)
        if self.zn == '==':
            return Number(int(a.value == b.value))
        if self.zn == '!=':
            return Number(int(a.value != b.value))
        if self.zn == '<':
            return Number(int(a.value < b.value))
        if self.zn == '>':
            return Number(int(a.value > b.value))
        if self.zn == '<=':
            return Number(int(a.value <= b.value))
        if self.zn == '>=':
            return Number(int(a.value >= b.value))
        if self.zn == '&&':
            return Number(a.value and b.value)
        if self.zn == '||':
            return Number(a.value or b.value)


class UnaryOperation:
    def __init__(self, op, expr):
        self.zn = op
        self.a = expr

    def evaluate(self, scope):
        a = self.a.evaluate(scope)
        if self.zn == '-':
            return Number(-a.value)
        else:
            return Number(int(not a.value))


def example():
    parent = Scope()
    parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'),
                                                    '+',
                                                    Reference('world')))])
    parent["bar"] = Number(10)
    scope = Scope(parent)
    assert 10 == scope["bar"].value
    scope["bar"] = Number(20)
    assert scope["bar"].value == 20
    print('It should print 2: ', end=' ')
    FunctionCall(FunctionDefinition('foo', parent['foo']),
                 [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)


def my_tests():
    alol = Scope()
    alol["DR"] = Number(1408)
    alol["foo"] = Number(95)
    Conditional([FunctionCall(
        FunctionDefinition("foo", Function(("a", "b"), [BinaryOperation(
            Reference("a"), "+",
            Reference("b"))])),
        [Reference("DR"), Reference("lol")])],
        BinaryOperation(UnaryOperation
                        ('-', alol["DR"]), '<',
                        Read("lol").evaluate(alol))
                )
    Print(alol["foo"]).evaluate(alol)
    alol["olya"] = Number(1408)
    Print(UnaryOperation("-",
                         Reference("olya"))).evaluate(alol)
    Read("al").evaluate(alol)
    Print(BinaryOperation(Reference("al"),
                          "/", Reference("olya"))).evaluate(alol)


if __name__ == '__main__':
    example()
    my_tests()
