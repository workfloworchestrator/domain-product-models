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

from orchestrator.domain.base import ProductBlockModel, SubscriptionModel, serializable_property
from orchestrator.forms.network_type_validators import MTU
from orchestrator.types import SubscriptionLifecycle

from surf.products.product_blocks.resource_type_types import IpPeerPortType
from surf.products.product_blocks.sap_sn8 import Sn8ServiceAttachPointBlock, Sn8ServiceAttachPointBlockInactive


class IpPeerPortBlockInactive(ProductBlockModel, product_block_name="IP Peer Port Block"):
    sap: Sn8ServiceAttachPointBlockInactive
    nso_service_id: UUID | None = None
    peer_port_name: str | None = None
    peer_port_type: IpPeerPortType | None = None
    ipv4_mtu: MTU | None = None
    ipv6_mtu: MTU | None = None
    ims_circuit_id: int | None = None
    ipv4_ipam_address_id: int | None = None
    ipv6_ipam_address_id: int | None = None
    ptp_ipv4_ipam_id: int | None = None
    ptp_ipv6_ipam_id: int | None = None


class IpPeerPortBlockProvisioning(IpPeerPortBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    sap: Sn8ServiceAttachPointBlock
    nso_service_id: UUID
    peer_port_name: str
    peer_port_type: IpPeerPortType
    ipv4_mtu: MTU
    ipv6_mtu: MTU
    ims_circuit_id: int | None = None
    ipv4_ipam_address_id: int | None = None
    ipv6_ipam_address_id: int | None = None
    ptp_ipv4_ipam_id: int | None = None
    ptp_ipv6_ipam_id: int | None = None

    @serializable_property
    def title(self) -> str:
        subscription = SubscriptionModel.from_subscription(self.owner_subscription_id)
        return f"{subscription.description}"


class IpPeerPortBlock(IpPeerPortBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    sap: Sn8ServiceAttachPointBlock
    nso_service_id: UUID
    peer_port_name: str
    peer_port_type: IpPeerPortType
    ipv4_mtu: MTU
    ipv6_mtu: MTU
    ims_circuit_id: int
    ipv4_ipam_address_id: int | None = None
    ipv6_ipam_address_id: int | None = None
    ptp_ipv4_ipam_id: int | None = None
    ptp_ipv6_ipam_id: int | None = None
