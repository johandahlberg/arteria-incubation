
from st2tests.base import BaseActionTestCase

from bcl2fastq_service import ArteriaBcl2FastqServiceAction

class Bcl2FastqServiceTest(BaseActionTestCase):
    action_cls = ArteriaBcl2FastqServiceAction

    def test_nothing(self):
        self.assertTrue(True)