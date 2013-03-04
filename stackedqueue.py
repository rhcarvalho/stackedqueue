"""stackedqueue -- a demo of how to implement queues using stacks.

The problem was proposed by my friend Bertie Liu (github.com/aceisScope).

Author: Rodolfo Carvalho (github.com/rhcarvalho)
"""

from cStringIO import StringIO


class Queue(object):
    """A queue data structure built on top of stacks."""
    def __init__(self, stack_cap=2, n_stacks=2):
        self._stack_cap = stack_cap
        self._n_stacks = n_stacks
        self._stacks = [Stack(cap=stack_cap) for i in xrange(n_stacks)]
        self._helper_stack = Stack(cap=stack_cap)
        self._rptr = 0 # pointer to stack for reading
        self._wptr = 0 # pointer to stack for writing

    def __str__(self):
        b = StringIO()
        b.write("Queue(stack_cap={}, n_stacks={}, cap={}<{}>, stacks=[".format(
                self._stack_cap, self._n_stacks, self.cap, len(self)))
        for i, s in enumerate(self._stacks):
            b.write("\n {}:{},".format(i, s))
        b.write("\n *helper{}\n])".format(self._helper_stack))
        return b.getvalue()

    @property
    def cap(self):
        return self._stack_cap * self._n_stacks

    def __len__(self):
        return sum(len(s) for s in self._stacks)

    @property
    def full(self):
        return len(self) >= self.cap

    @property
    def empty(self):
        return len(self) == 0

    def enqueue(self, item):
        for i in xrange(self._n_stacks):
            if not self._stacks[self._wptr].full:
                return self._stacks[self._wptr].append(item)
            self._inc_wptr()
        raise QueueOverflow("Too many items in the queue.")

    def dequeue(self):
        if self._helper_stack.empty:
            self._invert_stack(self._stacks[self._rptr], self._helper_stack)
            self._inc_rptr()
        return self._helper_stack.pop()

    def _invert_stack(self, from_stack, to_stack):
        while not from_stack.empty:
            to_stack.append(from_stack.pop())

    def _inc_wptr(self):
        self._wptr = (self._wptr + 1) % self._n_stacks

    def _inc_rptr(self):
        self._rptr = (self._rptr + 1) % self._n_stacks


class Stack(object):
    """A limited stack data structure."""
    def __init__(self, cap):
        self._cap = cap
        self._list = []

    def __str__(self):
        return "Stack({}<{}>, {})".format(self._cap, len(self), self._list)

    @property
    def cap(self):
        return self._cap

    def __len__(self):
        return len(self._list)

    @property
    def full(self):
        return len(self) >= self.cap

    @property
    def empty(self):
        return len(self) == 0

    def append(self, item):
        if self.full:
            raise StackOverflow("Too many items in the stack.")
        return self._list.append(item)

    def pop(self):
        return self._list.pop()


class StackOverflow(Exception):
    pass

class QueueOverflow(Exception):
    pass


def print_some_queues():
    q = Queue(10, 16)
    for i in xrange(q.cap):
        q.enqueue(i)
    print q
    q.dequeue()
    print q
    print Queue(n_stacks=0)


if __name__ == "__main__":
    print_some_queues()
