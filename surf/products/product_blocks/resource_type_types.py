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

"""Collection of types used for typing resource types in product blocks."""

from __future__ import annotations

from collections.abc import Generator

from pydantic.types import ConstrainedInt

from orchestrator.forms.validators import Choice
from orchestrator.types import strEnum


class PortMode(strEnum):
    """Valid port modes."""

    TAGGED = "tagged"
    UNTAGGED = "untagged"
    LINKMEMBER = "link_member"


class AggregatedPortMode(strEnum):
    """Valid port modes for aggregated ports."""

    TAGGED = PortMode.TAGGED
    UNTAGGED = PortMode.UNTAGGED


class Asn(ConstrainedInt):
    """Autonomous System Number."""

    ge = 1
    le = 4_294_967_294

    @classmethod
    def __get_validators__(cls) -> Generator:
        yield from super().__get_validators__()
        yield cls.valid_asn

    @classmethod
    def valid_asn(cls, asn: Asn) -> Asn:
        if asn == 65535:
            raise ValueError("RFC 7300 doesn't allow 65535 as ASN value")
        return asn


class BgpSessionPriority(strEnum):
    """Border Gateway Protocol session priority."""

    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"
    QUATERNARY = "quaternary"


class BgpHashAlgorithm(strEnum):
    """Border Gateway Protocol hash algorithm."""

    MD5 = "MD5"
    NO = "no"  # This value is also used in a mail template!


class BgpExportPolicy(strEnum):
    """Border Gateway Protocol export policy."""

    FULL = "full"
    DEFAULT = "default"


class BgpMetric(ConstrainedInt):
    """Border Gateway Protocol Metric value."""

    ge = 1
    le = 4_294_967_295


class SurfCertFilter(strEnum):
    DEFAULT = "default"


class PeerType(Choice):
    """Valid Peer Types for IP Peer Group."""

    RESEARCH = "research-network"
    COMMERCIAL = "commercial-network"


class InterconnectionType(Choice):
    """Interconnection type for IP Peer Group."""

    IX = "ix"
    PNI = "pni"
    TRANSIT = "transit"


class MetricOut(ConstrainedInt):
    """Metric Out value for IP Peer Group."""

    ge = 0
    le = 65536


class IpPeerPortType(strEnum):
    IX = "ix"
    PNI = "pni"
    TRANSIT = "transit"
    RESEARCH = "research"
    OTHER = "other"


class AsPrepend(ConstrainedInt):
    """AsPrepend value for IP Peer."""

    ge = 1
    le = 5


class MaxPrefix(ConstrainedInt):
    """Max Prefix length for IP Peer."""

    ge = 1
    le = 10_000_000


class FwDeployType(strEnum):
    PFW = "PFW"
    VFW = "VFW"
    RFW = "RFW"


class SpecificTemplateType(Choice):
    LHCOPN = "lhcopn"
    LHCONE = "lhcone"
    ADVANCED = "advanced"


class URPFType(Choice):
    disabled = "disabled"
    loose = "loose"
    strict = "strict"


class EndpointRoleType(Choice):
    customer = "customer"
    transit = "transit"
    special = "special"
