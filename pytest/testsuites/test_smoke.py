"""Runs a 'smoke' test for an Azure Linux VM deployment."""
import logging
import platform
import socket

from invoke import UnexpectedExit
from invoke.runners import Result  # type: ignore
from paramiko import SSHException  # type: ignore

import pytest
from node_plugin import Node


@pytest.mark.deploy(setup="OneVM", vm_size="Standard_DS2_v2")
@pytest.mark.usefixtures("class_node")
class TestSmoke:
    """Check that a VM can be deployed and is responsive.

    1. Deploy the VM (via 'node' fixture) and log it.
    2. Ping the VM.
    3. Connect to the VM via SSH.
    4. Attempt to reboot via SSH, otherwise use the platform.
    5. Fetch the serial console logs.

    """

    n: Node

    # TODO: Move to ‘Node.ping()’
    ping_flag = "-c 1" if platform.system() == "Linux" else "-n 1"

    def test_ping_1(self) -> None:
        # TODO: Can’t ping by default, need to enable.
        logging.warn("Expecting ping to fail because it's not enabled yet")
        r: Result = self.n.local(f"ping {self.ping_flag} {self.n.host}", warn=True)
        assert r.ok, f"Pinging {self.n.host} failed"

    def test_ssh_1(self) -> None:
        self.n.run("uptime")

    def test_reboot(self) -> None:
        try:
            # If this succeeds, we should expect the exit code to be -1
            r: Result = self.n.sudo("reboot")
        except UnexpectedExit:
            assert r.exited == -1, "While SSH worked, reboot failed"
        except (TimeoutError, SSHException, socket.error) as e:
            logging.warn(f"SSH failed '{e}', using platform to reboot")
            self.n.platform_restart()

    def test_ping_2(self) -> None:
        # TODO: Can’t ping by default, need to enable.
        r: Result = self.n.local(f"ping {self.ping_flag} {self.n.host}", warn=True)
        assert r.ok, f"Pinging {self.n.host} failed"

    def test_ssh_2(self) -> None:
        self.n.run("uptime")

    def test_serial_log(self) -> None:
        self.n.get_boot_diagnostics()
