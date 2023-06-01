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

from uuid import UUID

from pydantic import Field

from orchestrator.domain.base import ProductBlockModel, serializable_property
from orchestrator.forms.network_type_validators import MTU
from orchestrator.types import SubscriptionLifecycle

from surf.products.product_blocks.ip_prefix import IpPrefixBlock
from surf.products.product_blocks.resource_type_types import BgpExportPolicy, BgpHashAlgorithm, BgpSessionPriority
from surf.products.product_blocks.sap_sn8 import Sn8ServiceAttachPointBlock, Sn8ServiceAttachPointBlockInactive


class Sn8IpStaticServiceAttachPointSettingsBlockInactive(
    ProductBlockModel, product_block_name="IP Static Service Attach Point Settings"
):
    sap: Sn8ServiceAttachPointBlockInactive
    prefixes: list[IpPrefixBlock] = Field(default_factory=list)
    customer_ipv4_mtu: MTU | None = None
    ptp_ipv4_ipam_id: int | None = None
    customer_ipv6_mtu: MTU | None = None
    ptp_ipv6_ipam_id: int | None = None

    @property
    def ip_prefix_subscription_id(self) -> list[UUID]:
        return [prefix.owner_subscription_id for prefix in self.prefixes]

    @serializable_property
    def title(self) -> str:
        return f"{self.name}"


class Sn8IpStaticServiceAttachPointSettingsBlockProvisioning(
    Sn8IpStaticServiceAttachPointSettingsBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    sap: Sn8ServiceAttachPointBlock
    prefixes: list[IpPrefixBlock]
    customer_ipv4_mtu: MTU
    ptp_ipv4_ipam_id: int | None = None
    customer_ipv6_mtu: MTU | None = None
    ptp_ipv6_ipam_id: int | None = None

    @property
    def ip_prefix_subscription_id(self) -> list[UUID]:
        return [prefix.owner_subscription_id for prefix in self.prefixes]


class Sn8IpStaticServiceAttachPointSettingsBlock(
    Sn8IpStaticServiceAttachPointSettingsBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]
):
    sap: Sn8ServiceAttachPointBlock
    prefixes: list[IpPrefixBlock]
    customer_ipv4_mtu: MTU
    ptp_ipv4_ipam_id: int
    customer_ipv6_mtu: MTU | None = None
    ptp_ipv6_ipam_id: int | None = None

    @property
    def ip_prefix_subscription_id(self) -> list[UUID]:
        return [prefix.owner_subscription_id for prefix in self.prefixes]


class Sn8IpBgpServiceAttachPointSettingsBlockInactive(
    ProductBlockModel, product_block_name="IP BGP Service Attach Point Settings"
):
    sap: Sn8ServiceAttachPointBlockInactive
    prefixes: list[IpPrefixBlock] = Field(default_factory=list)

    customer_ipv4_mtu: MTU | None = None
    bfd: bool | None = None
    bgp_session_priority: BgpSessionPriority | None = None
    bgp_hash_algorithm: BgpHashAlgorithm | None = None
    bgp_export_policy: BgpExportPolicy | None = None
    ptp_ipv4_ipam_id: int | None = None
    customer_ipv6_mtu: MTU | None = None
    ptp_ipv6_ipam_id: int | None = None
    bgp_password: str | None = None
    bfd_minimum_interval: int | None = None
    bfd_multiplier: int | None = None
    enable_routing: bool = True

    @property
    def ip_prefix_subscription_id(self) -> list[UUID]:
        return [prefix.owner_subscription_id for prefix in self.prefixes]


class Sn8IpBgpServiceAttachPointSettingsBlockProvisioning(
    Sn8IpBgpServiceAttachPointSettingsBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    sap: Sn8ServiceAttachPointBlock
    prefixes: list[IpPrefixBlock]
    customer_ipv4_mtu: MTU
    bfd: bool
    bgp_session_priority: BgpSessionPriority
    bgp_hash_algorithm: BgpHashAlgorithm
    bgp_export_policy: BgpExportPolicy

    ptp_ipv4_ipam_id: int | None = None
    customer_ipv6_mtu: MTU | None = None
    ptp_ipv6_ipam_id: int | None = None
    bgp_password: str | None = None
    bfd_minimum_interval: int | None = None
    bfd_multiplier: int | None = None
    enable_routing: bool = True

    @property
    def ip_prefix_subscription_id(self) -> list[UUID]:
        return [prefix.owner_subscription_id for prefix in self.prefixes]

    @serializable_property
    def title(self) -> str:
        sap = self.sap
        return f"{self.tag} {sap.node.nso_device_id} VLAN {sap.vlanrange}"


class Sn8IpBgpServiceAttachPointSettingsBlock(
    Sn8IpBgpServiceAttachPointSettingsBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]
):
    sap: Sn8ServiceAttachPointBlock
    prefixes: list[IpPrefixBlock]
    customer_ipv4_mtu: MTU
    bfd: bool
    bgp_session_priority: BgpSessionPriority
    bgp_hash_algorithm: BgpHashAlgorithm
    bgp_export_policy: BgpExportPolicy

    ptp_ipv4_ipam_id: int
    ptp_ipv6_ipam_id: int | None = None

    customer_ipv6_mtu: MTU | None = None
    bgp_password: str | None = None
    bfd_minimum_interval: int | None = None
    bfd_multiplier: int | None = None
    enable_routing: bool = True

    @property
    def ip_prefix_subscription_id(self) -> list[UUID]:
        return [prefix.owner_subscription_id for prefix in self.prefixes]
