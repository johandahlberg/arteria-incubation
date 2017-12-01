
import requests
import json

from st2actions.runners.pythonrunner import Action


class ArteriaBcl2FastqServiceAction(Action):

    START_COMMAND = "start"
    POLL_COMMAND = "poll"

    COMMANDS = [START_COMMAND, POLL_COMMAND]

    def _verify_command_valid(self, cmd):
        return cmd in self.COMMANDS

    def run(self, cmd, url, runfolder, bcl2fastq_body, status_url):

        if not self._verify_command_valid(cmd):
            self.logger.error("Command: {} is not valid. Valid commands are: {}".format(cmd, self.COMMANDS))
            return False, ""

        if cmd == self.START_COMMAND:
            return self.start_bcl2fastq(url, runfolder, bcl2fastq_body)
        else:
            return self.poll_bcl2fastq_instance(status_url)

    def start_bcl2fastq(self, url, runfolder, bcl2fastq_body):
        if not url:
            self.logger.error("You have to specify a url to start!")
            return False, ""

        if not runfolder:
            self.logger.error("You have to specify a runfolder to start!")
            return False, ""

        start_url = "{}/api/1.0/start/{}".format(url.strip("/"), runfolder)

        if not bcl2fastq_body:
            bcl2fastq_body = ""

        response = requests.post(start_url, data=json.dumps(bcl2fastq_body))
        if response.status_code == 201:
            return True, json.loads(response.text)
        else:
            return False, json.loads(response.text)

    def poll_bcl2fastq_instance(self, status_url):
        response = requests.get(status_url)
        if response.status_code == 200:
            return True, json.loads(response.text)
        else:
            return False, json.loads(response.text)




