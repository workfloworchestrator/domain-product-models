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

from orchestrator.domain.base import SI, ProductBlockModel, SubscriptionInstanceList, serializable_property
from orchestrator.types import SubscriptionLifecycle

from surf.products.product_blocks.peer import PeerBlock, PeerBlockInactive, PeerBlockProvisioning
from surf.products.product_blocks.resource_type_types import Asn, AsPrepend, MaxPrefix

# some sensible default max
MAX_NUMBER_OF_PEERINGS = 20


class ListOfPeers(SubscriptionInstanceList[SI]):
    min_items = 0
    max_items = MAX_NUMBER_OF_PEERINGS


class IpPeerBlockInactive(ProductBlockModel, product_block_name="IP Peer Block"):
    peers: ListOfPeers[PeerBlockInactive]
    peer_name: str | None = None
    asn: Asn | None = None
    nso_service_id: UUID | None = None
    community_list_out: list[str] = Field(default_factory=list)

    multipath: bool | None = False
    as_prepend: AsPrepend | None = None
    blackhole_community: str | None = None
    peer_community: Asn | None = None
    ipv4_max_prefix: MaxPrefix | None = None
    ipv6_max_prefix: MaxPrefix | None = None


class IpPeerBlockProvisioning(IpPeerBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    peers: ListOfPeers[PeerBlockProvisioning]
    peer_name: str
    asn: Asn
    nso_service_id: UUID
    community_list_out: list[str]

    multipath: bool | None = False
    as_prepend: AsPrepend | None = None
    blackhole_community: str | None = None
    peer_community: Asn | None = None
    ipv4_max_prefix: MaxPrefix | None = None
    ipv6_max_prefix: MaxPrefix | None = None

    @serializable_property
    def title(self) -> str:
        return f"{self.tag} {self.peer_name} AS{self.asn}"


class IpPeerBlock(IpPeerBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    peers: ListOfPeers[PeerBlock]
    peer_name: str
    asn: Asn
    nso_service_id: UUID
    community_list_out: list[str]

    multipath: bool | None = False
    as_prepend: AsPrepend | None = None
    blackhole_community: str | None = None
    peer_community: Asn | None = None
    ipv4_max_prefix: MaxPrefix | None = None
    ipv6_max_prefix: MaxPrefix | None = None
