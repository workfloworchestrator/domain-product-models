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

from orchestrator.domain.base import ProductBlockModel, serializable_property
from orchestrator.types import SubscriptionLifecycle


class NodeProductBlockInactive(ProductBlockModel, product_block_name="Node"):
    ims_node_id: int | None = None
    node_location: str | None = None
    nso_device_id: str | None = None
    nso_service_id: UUID | None = None
    sr_node_segment_id: int | None = None
    node_ipv4_ipam_id: int | None = None
    node_ipv6_ipam_id: int | None = None
    bgp_full_table: bool | None = None


class NodeProductBlockProvisioning(NodeProductBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    ims_node_id: int
    node_location: str
    nso_device_id: str
    nso_service_id: UUID
    sr_node_segment_id: int
    node_ipv4_ipam_id: int | None = None
    node_ipv6_ipam_id: int | None = None
    bgp_full_table: bool

    @serializable_property
    def title(self) -> str:
        return f"{self.tag} {self.nso_device_id}"


class NodeProductBlock(NodeProductBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    ims_node_id: int
    node_location: str
    nso_device_id: str
    nso_service_id: UUID
    sr_node_segment_id: int
    node_ipv4_ipam_id: int
    node_ipv6_ipam_id: int
    bgp_full_table: bool
