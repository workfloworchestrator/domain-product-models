# Copyright 2019-2023 surf.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from enum import IntEnum

from orchestrator.types import strEnum


class Domain(strEnum):
    """Domain to distinguish between different classes of products."""

    DNS = "DNS"
    SURFNET7 = "SURFNET7"
    SURFNET8 = "SURFNET8"
    NETHERLIGHT8 = "NETHERLIGHT8"
    NFV = "NFV"
    SURFwireless = "SURFwireless"
    DIRECT_CLOUD_CONNECTIVITY = "Direct Cloud Connectivity"


class IpRoutingType(strEnum):
    """Type of routing used for an IP service, static or BGP."""

    BGP = "BGP"
    STATIC = "Static"


class PortSpeed(IntEnum):
    """Speed of physical port in Mbit/s."""

    _1000 = 1000
    _10000 = 10000
    _40000 = 40000
    _100000 = 100000
    _400000 = 400000


class ProtectionType(strEnum):
    """Redundancy type."""

    UNPROTECTED = "Unprotected"
    PROTECTED = "Protected"
    REDUNDANT = "Redundant"


class Size(IntEnum):
    """Capacity of the firewall in Mbit/s."""

    S1000 = 1000
    S2000 = 2000
    S3000 = 3000
    S4000 = 4000
    S5000 = 5000
    S6000 = 6000
    S7000 = 7000
    S8000 = 8000
    S9000 = 9000
    s10000 = 10000
    S11000 = 11000
    S12000 = 12000
    S13000 = 13000
    S14000 = 14000
    S15000 = 15000
    S16000 = 16000
