# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from lisa.feature import Feature

FEATURE_NAME_DISK = "DiskPremiumLRS"


class DiskPremiumLRS(Feature):
    @classmethod
    def name(cls) -> str:
        return FEATURE_NAME_DISK

    @classmethod
    def can_disable(cls) -> bool:
        return True

    def _switch(self, enable: bool) -> None:
        raise NotImplementedError()

    def disable(self) -> None:
        self._switch(False)

    def enable(self) -> None:
        self._switch(True)

    def enabled(self) -> bool:
        return True

    @staticmethod
    def get_disk_id() -> str:
        raise NotImplementedError
