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
from ipaddress import IPv4Address, IPv6Address
from uuid import UUID

from orchestrator.domain import SubscriptionModel
from orchestrator.domain.base import ProductBlockModel, serializable_property
from orchestrator.types import SubscriptionLifecycle

from surf.products.product_blocks.ip_peer_group import (
    IpPeerGroupBlock,
    IpPeerGroupBlockInactive,
    IpPeerGroupBlockProvisioning,
)
from surf.products.product_blocks.ip_peer_port import IpPeerPortBlock
from surf.products.product_blocks.resource_type_types import AsPrepend, BgpSessionPriority, MetricOut


class PeerBlockInactive(ProductBlockModel, product_block_name="IP Peering Block"):
    port: IpPeerPortBlock | None

    @property
    def port_subscription_id(self) -> UUID | None:
        return self.port.owner_subscription_id if self.port else None

    peer_group: IpPeerGroupBlockInactive | None = None
    bgp_import_reject_all: bool | None = None
    bgp_export_reject_all: bool | None = None
    bfd: bool | None = None

    ipv4_remote_address: IPv4Address | None = None
    ipv6_remote_address: IPv6Address | None = None
    as_prepend: AsPrepend | None = None
    metric_out: MetricOut | None = None
    auth_key: str | None = None
    bgp_session_priority: BgpSessionPriority | None = None
    bfd_minimum_interval: int | None = None
    bfd_multiplier: int | None = None


class PeerBlockProvisioning(PeerBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    port: IpPeerPortBlock

    @property
    def port_subscription_id(self) -> UUID:
        return self.port.owner_subscription_id

    peer_group: IpPeerGroupBlockProvisioning
    bgp_import_reject_all: bool
    bgp_export_reject_all: bool
    bfd: bool

    ipv4_remote_address: IPv4Address | None = None
    ipv6_remote_address: IPv6Address | None = None
    as_prepend: AsPrepend | None = None
    metric_out: MetricOut | None = None
    auth_key: str | None = None
    bgp_session_priority: BgpSessionPriority | None = None
    bfd_minimum_interval: int | None = None
    bfd_multiplier: int | None = None

    @serializable_property
    def title(self) -> str:
        sap = self.port.sap
        subscription = SubscriptionModel.from_subscription(sap.owner_subscription_id)
        return f"{subscription.description}{sap.vlanrange}"


class PeerBlock(PeerBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    port: IpPeerPortBlock

    @property
    def port_subscription_id(self) -> UUID:
        return self.port.owner_subscription_id

    peer_group: IpPeerGroupBlock
    bgp_import_reject_all: bool = False
    bgp_export_reject_all: bool = False
    bfd: bool

    ipv4_remote_address: IPv4Address | None = None
    ipv6_remote_address: IPv6Address | None = None
    as_prepend: AsPrepend | None = None
    metric_out: MetricOut | None = None
    auth_key: str | None = None
    bgp_session_priority: BgpSessionPriority | None = None
    bfd_minimum_interval: int | None = None
    bfd_multiplier: int | None = None
