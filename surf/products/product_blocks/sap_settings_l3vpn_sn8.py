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

from ipaddress import IPv4Address, IPv4Interface, IPv6Address, IPv6Interface

from orchestrator.domain.base import ProductBlockModel, serializable_property
from orchestrator.forms.network_type_validators import MTU
from orchestrator.types import SubscriptionLifecycle

from surf.products.product_blocks.resource_type_types import Asn, BgpMetric, EndpointRoleType, MaxPrefix, URPFType
from surf.products.product_blocks.sap_sn8 import Sn8ServiceAttachPointBlock, Sn8ServiceAttachPointBlockInactive


class Sn8L3VpnServiceAttachPointSettingsBlockInactive(
    ProductBlockModel, product_block_name="SN8 L3VPN Service Attach Point Settings"
):
    """Object model for a Service Attach Point settings as used by a L3VPN in SN8."""

    sap: Sn8ServiceAttachPointBlockInactive | None = None

    ipv4_max_prefix: MaxPrefix | None = None
    ipv6_max_prefix: MaxPrefix | None = None

    ipv4_address: IPv4Interface | None = None
    ipv6_address: IPv6Interface | None = None

    ipv4_remote_address: IPv4Address | None = None
    ipv6_remote_address: IPv6Address | None = None

    customer_ipv4_mtu: MTU | None = None
    customer_ipv6_mtu: MTU | None = None

    bfd: bool | None = None
    bfd_minimum_interval: int | None = None
    bfd_multiplier: int | None = None

    bgp_password: str | None = None
    asn: Asn | None = None
    bgp_metric: BgpMetric | None = None

    enable_routing: bool = True

    urpf: URPFType = URPFType.disabled
    endpoint_role: EndpointRoleType | None = None


class Sn8L3VpnServiceAttachPointSettingsBlock(
    Sn8L3VpnServiceAttachPointSettingsBlockInactive,
    lifecycle=[SubscriptionLifecycle.ACTIVE, SubscriptionLifecycle.PROVISIONING],
):
    """ServiceAttachPointSettingsL3VpnSN8 with optional fields to use in the active lifecycle state."""

    sap: Sn8ServiceAttachPointBlock

    ipv4_max_prefix: MaxPrefix | None = None
    ipv6_max_prefix: MaxPrefix | None = None

    ipv4_address: IPv4Interface | None = None
    ipv6_address: IPv6Interface | None = None

    ipv4_remote_address: IPv4Address | None = None
    ipv6_remote_address: IPv6Address | None = None

    customer_ipv4_mtu: MTU | None = None
    customer_ipv6_mtu: MTU | None = None

    bfd: bool
    bfd_minimum_interval: int | None = None
    bfd_multiplier: int | None = None

    bgp_password: str | None = None
    asn: Asn
    bgp_metric: BgpMetric | None = None

    enable_routing: bool = True

    urpf: URPFType
    endpoint_role: EndpointRoleType | None = None

    @serializable_property
    def title(self) -> str:
        sap = self.sap
        return f"{self.tag} {sap.node.nso_device_id} VLAN {sap.vlanrange}"
