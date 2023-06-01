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

from orchestrator.domain.base import ProductBlockModel, SubscriptionModel, serializable_property
from orchestrator.types import SubscriptionLifecycle

from surf.products.product_blocks.resource_type_types import Asn, InterconnectionType, MetricOut, PeerType


class IpPeerGroupBlockInactive(ProductBlockModel, product_block_name="IP Peer Group Block"):
    peer_group_name: str | None = None
    peer_type: PeerType | None = None
    peer_community: Asn | None = None
    route_servers: list[str] = Field(default_factory=list)
    interconnection_type: InterconnectionType | None = None
    nso_service_id: UUID | None = None
    metric_out: MetricOut | None = None


class IpPeerGroupBlockProvisioning(IpPeerGroupBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    peer_group_name: str
    peer_type: PeerType
    peer_community: Asn | None
    route_servers: list[str]
    interconnection_type: InterconnectionType
    nso_service_id: UUID
    metric_out: MetricOut | None = None

    @serializable_property
    def title(self) -> str:
        subscription = SubscriptionModel.from_subscription(self.owner_subscription_id)
        return f"{subscription.description}"


class IpPeerGroupBlock(IpPeerGroupBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    peer_group_name: str
    peer_type: PeerType
    peer_community: Asn | None
    route_servers: list[str]
    interconnection_type: InterconnectionType
    nso_service_id: UUID
    metric_out: MetricOut | None = None
