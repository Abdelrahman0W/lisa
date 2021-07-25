# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
from typing import Any

from lisa.executable import Tool


class Service(Tool):
    @property
    def command(self) -> str:
        return "service"

    @property
    def can_install(self) -> bool:
        return False

    def _check_exists(self) -> bool:
        return True

    def _check_service_running(self, name: str) -> bool:
        cmd_result = self.run(f"{name} status", shell=True, sudo=True, force_run=True)
        return cmd_result.exit_code == 0

    def stop_service(self, name: str) -> None:
        if self._check_service_running(name):
            cmd_result = self.run(f"{name} stop", shell=True, sudo=True, force_run=True)
            cmd_result.assert_exit_code()

    def restart_service(self, name: str) -> None:
        cmd_result = self.run(f"{name} restart", shell=True, sudo=True, force_run=True)
        cmd_result.assert_exit_code()


class Systemctl(Tool):
    @property
    def command(self) -> str:
        return "systemctl"

    @property
    def can_install(self) -> bool:
        return False

    def _check_exists(self) -> bool:
        return True

    def is_active(self, name: str) -> bool:
        cmd_result = self.run(
            f"is-active {name}", shell=True, sudo=True, force_run=True
        )
        return "active" == cmd_result.stdout

    def stop_service(self, name: str) -> None:
        if self.is_active(name):
            cmd_result = self.run(f"stop {name}", shell=True, sudo=True, force_run=True)
            cmd_result.assert_exit_code()

    def restart_service(self, name: str) -> None:
        cmd_result = self.run(f"restart {name}", shell=True, sudo=True, force_run=True)
        cmd_result.assert_exit_code()


class Servicectl(Tool):
    @property
    def command(self) -> str:
        return "systemctl"

    @property
    def can_install(self) -> bool:
        return False

    def _check_exists(self) -> bool:
        return True

    def initialize_tool(self) -> Any:
        cmd_result = self.node.execute(
            "ls -lt /run/systemd/system", shell=True, sudo=True
        )
        if 0 == cmd_result.exit_code:
            return self.node.tools[Systemctl]
        else:
            return self.node.tools[Service]
