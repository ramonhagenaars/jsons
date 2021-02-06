from unittest import TestCase

import jsons


class TestFork(TestCase):
    def test_fork(self):
        f1 = jsons.fork()
        f2 = jsons.fork()
        f3 = jsons.fork(fork_inst=f1)

        jsons.set_serializer(lambda *_, **__: 'f1', str, fork_inst=f1)
        jsons.set_serializer(lambda *_, **__: 'f2', str, fork_inst=f2)
        jsons.set_serializer(lambda *_, **__: 3, int, fork_inst=f3)

        f4 = jsons.fork(fork_inst=f1)

        self.assertEqual('f1', jsons.dump('I wanted a fork on the table.',
                                          fork_inst=f1))
        self.assertEqual('f2', jsons.dump('I wanted a fork on the table.',
                                          fork_inst=f2))
        self.assertEqual('f3', jsons.dump('f3', fork_inst=f3))
        self.assertEqual(3, jsons.dump(42, fork_inst=f3))
        self.assertEqual('f1', jsons.dump('I wanted a fork on the table.',
                                          fork_inst=f4))
