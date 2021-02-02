import warnings
from unittest import TestCase

import jsons


class TestSuppressWarnings(TestCase):
    def test_suppress_warning(self):
        fork_inst = jsons.fork()
        jsons.suppress_warning('some-warning', fork_inst)

        with warnings.catch_warnings(record=True) as w:
            fork_inst._warn('Some warning', 'some-warning')
            fork_inst._warn('Another warning', 'another-warning')

        self.assertEqual(1, len(w))
        self.assertIn('Another warning', str(w[0]))

    def test_suppress_warnings(self):
        fork_inst = jsons.fork()
        jsons.suppress_warnings(True, fork_inst)

        with warnings.catch_warnings(record=True) as w:
            fork_inst._warn('Some warning', 'some-warning')
        self.assertEqual(0, len(w))

        jsons.suppress_warnings(False, fork_inst)

        with warnings.catch_warnings(record=True) as w:
            fork_inst._warn('Some warning', 'some-warning')
        self.assertEqual(1, len(w))
