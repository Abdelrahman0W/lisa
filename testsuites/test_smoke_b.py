from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from target import Azure
    from _pytest.logging import LogCaptureFixture

import logging
import socket
import time

from invoke.runners import CommandTimedOut, Result, UnexpectedExit  # type: ignore
from paramiko import SSHException  # type: ignore

from lisa import LISA


@LISA(
    platform="Azure",
    category="Functional",
    area="deploy",
    priority=0,
)
def test_smoke(target: Azure, caplog: LogCaptureFixture) -> None:
    """Check that an Azure Linux VM can be deployed and is responsive.

    This example uses exactly one function for the entire test, which
    means we have to catch failures that don't fail the test, and
    instead emit warnings. It works, and it's closer to how LISAv2
    would have implemented it, but it's less Pythonic. For a more
    "modern" example, see `test_smoke_a.py`.

    1. Deploy the VM (via `target` fixture).
    2. Ping the VM.
    3. Connect to the VM via SSH.
    4. Attempt to reboot via SSH, otherwise use the platform.
    5. Fetch the serial console logs AKA boot diagnostics.

    SSH failures DO NOT fail this test.

    """
    # Capture INFO and above logs for this test.
    caplog.set_level(logging.INFO)

    logging.info("Pinging before reboot...")
    ping1 = Result()
    try:
        ping1 = target.ping()
    except UnexpectedExit:
        logging.warning(f"Pinging {target.host} before reboot failed")

    ssh_errors = (TimeoutError, CommandTimedOut, SSHException, socket.error)

    try:
        logging.info("SSHing before reboot...")
        target.conn.open()
    except ssh_errors as e:
        logging.warning(f"SSH before reboot failed: '{e}'")

    reboot_exit = 0
    try:
        logging.info("Rebooting...")
        # If this succeeds, we should expect the exit code to be -1
        reboot_exit = target.conn.sudo("reboot", timeout=5).exited
    except ssh_errors as e:
        logging.warning(f"SSH failed, using platform to reboot: '{e}'")
        target.platform_restart()
    except UnexpectedExit:
        # TODO: How do we differentiate reboot working and the SSH
        # connection disconnecting for other reasons?
        if reboot_exit != -1:
            logging.warning("While SSH worked, 'reboot' command failed")

    # TODO: We should check something more concrete here instead of
    # sleeping an arbitrary amount of time.
    logging.info("Sleeping for 10 seconds after reboot...")
    time.sleep(10)

    logging.info("Pinging after reboot...")
    ping2 = Result()
    try:
        ping2 = target.ping()
    except UnexpectedExit:
        logging.warning(f"Pinging {target.host} after reboot failed")

    try:
        logging.info("SSHing after reboot...")
        target.conn.open()
    except ssh_errors as e:
        logging.warning(f"SSH after reboot failed: '{e}'")

    logging.info("Retrieving boot diagnostics...")
    try:
        target.get_boot_diagnostics()
    except UnexpectedExit:
        logging.warning("Retrieving boot diagnostics failed.")
    else:
        logging.info("See full report for boot diagnostics.")

    # NOTE: The test criteria is to fail only if ping fails.
    assert ping1.ok
    assert ping2.ok
