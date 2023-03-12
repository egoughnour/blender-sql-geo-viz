import unittest
import re

class Testing(unittest.TestCase):
##
#
    def test_regex_capture_group_for_env_dict(self):
        env_dict = {}
        #TODO test that the regex returns the named capture from the control output text 
        regex = r"^INFO\[\d*?] socket: (?P<socket>.*?)$"
        control_text = ("INFO[0000] quux \n"
	"INFO[0000] something something \n"
	"INFO[0000] something else \n"
	"INFO[0000] socket: unix:///Users/theuser/.colima/default/docker.sock")
        matches = re.finditer(regex, control_text, re.MULTILINE)
        for _, match in enumerate(matches, start=1):
            env_dict["DOCKER_HOST"] = match.group('socket')
            if env_dict["DOCKER_HOST"]:
                break
        assert(env_dict["DOCKER_HOST"].startswith("unix:///"))

    def test_regex_capture_from_stderr_for_socket_dict(self):
        env_dict = {}
        control_text = b"""
time="2023-03-12T14:11:47-05:00" level=info msg="colima is running using QEMU"
time="2023-03-12T14:11:47-05:00" level=info msg="arch: aarch64"
time="2023-03-12T14:11:47-05:00" level=info msg="runtime: docker"
time="2023-03-12T14:11:47-05:00" level=info msg="mountType: sshfs"
time="2023-03-12T14:11:47-05:00" level=info msg="socket: unix:///Users/theuser/.colima/default/docker.sock"'"""
        regex = r"msg=\"socket: (?P<socket>.*?)\"'"
        matches = re.finditer(regex, control_text, re.MULTILINE)
        for _, match in enumerate(matches, start=1):
            env_dict["DOCKER_HOST"] = match.group('socket')
            if env_dict["DOCKER_HOST"]:
                break
        assert(env_dict["DOCKER_HOST"].startswith("unix:///"))
