import unittest

from stackedqueue import Queue, QueueOverflow


class TestQueue(unittest.TestCase):
    def test_deq_empty_queue(self):
        q = Queue()
        self.assertRaises(IndexError, q.dequeue)

    def test_enq_overflow(self):
        q = Queue()
        for i in xrange(q.cap):
            q.enqueue(i)
        self.assertRaises(QueueOverflow, q.enqueue, 99)

    def test_enq_deq_full(self):
        q = Queue()
        for i in xrange(q.cap):
            q.enqueue(i)
        for i in xrange(q.cap):
            self.assertEqual(q.dequeue(), i)

    def test_enq_deq_half_enq_deq(self):
        q = Queue()
        for i in xrange(q.cap):
            q.enqueue(i)
        for i in xrange(q._stack_cap):
            self.assertEqual(q.dequeue(), i)
        for i in xrange(q._stack_cap):
            q.enqueue(i + q.cap)
        for i in xrange(q.cap):
            self.assertEqual(q.dequeue(), i + q._stack_cap)


if __name__ == "__main__":
    unittest.main()
