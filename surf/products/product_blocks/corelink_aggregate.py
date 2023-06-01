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
from orchestrator.domain.base import ProductBlockModel, serializable_property
from orchestrator.types import SubscriptionLifecycle

from surf.products.product_blocks.node import NodeProductBlock


class Sn8CorelinkAggregateBlockInactive(ProductBlockModel, product_block_name="Corelink Aggregate"):
    corelink_ipv4_ipam_id: int | None = None
    corelink_ipv6_ipam_id: int | None = None
    ims_aggregate_port_id: int | None = None
    node: NodeProductBlock | None = None


class Sn8CorelinkAggregateBlockProvisioning(
    Sn8CorelinkAggregateBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    corelink_ipv4_ipam_id: int | None = None
    corelink_ipv6_ipam_id: int | None = None
    ims_aggregate_port_id: int | None = None
    node: NodeProductBlock

    @serializable_property
    def title(self) -> str:
        return f"{self.tag} {self.node.nso_device_id}"


class Sn8CorelinkAggregateBlock(Sn8CorelinkAggregateBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    corelink_ipv4_ipam_id: int
    corelink_ipv6_ipam_id: int
    ims_aggregate_port_id: int
    node: NodeProductBlock
