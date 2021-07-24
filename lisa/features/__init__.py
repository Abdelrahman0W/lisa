# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from .disk_ephemeral import DiskEphemeral
from .disk_premium_lrs import DiskPremiumLRS
from .disk_standard_lrs import DiskStandardLRS
from .gpu import Gpu
from .nvme import Nvme
from .serial_console import SerialConsole
from .sriov import Sriov
from .startstop import StartStop

__all__ = [
    "DiskEphemeral",
    "DiskPremiumLRS",
    "DiskStandardLRS",
    "Gpu",
    "Nvme",
    "SerialConsole",
    "Sriov",
    "StartStop",
]
