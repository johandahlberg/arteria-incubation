
import json

import mock

from st2tests.base import BaseActionTestCase

from bcl2fastq_service import ArteriaBcl2FastqServiceAction


class FakeResponse(object):

    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = json.dumps(text)

    def json(self):
        return json.loads(self.text)

class Bcl2FastqServiceTest(BaseActionTestCase):
    action_cls = ArteriaBcl2FastqServiceAction

    def test_start_command(self):
        expected_data = {"foo": "bar"}
        with mock.patch('requests.post',
                        return_value=FakeResponse(status_code=202, text=expected_data)) as mock_post:
            exit_flag, result = self.get_action_instance().run(cmd="start",
                                                               url="http://foo/",
                                                               runfolder="my_fav_runfolder")            
            self.assertTrue(exit_flag)
            self.assertEqual(result, expected_data)

    def test_poll_command_done(self):
        expected_data = {"state": "done"}
        with mock.patch('requests.get',
                        return_value=FakeResponse(status_code=200, text=expected_data)) as mock_post:
            exit_flag, result = self.get_action_instance().run(cmd="poll",
                                                               url="http://foo/",
                                                               runfolder="my_fav_runfolder")
            self.assertTrue(exit_flag)
            self.assertEqual(result, expected_data)
