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


from more_itertools import only

from orchestrator.db.models import ProductBlockTable
from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SubscriptionLifecycle

from surf.products.product_blocks.node import NodeProductBlock, NodeProductBlockInactive, NodeProductBlockProvisioning
from surf.products.product_types.sn8_corelink import Sn8Corelink
from surf.products.product_types.sn8_irbsp import Sn8IrbServicePort
from surf.products.product_types.sp import Sn8ServicePort
from surf.utils.helpers import is_active_sub


# Extra model for handling showing pre domain model wf subscriptions
class NodeInitial(
    SubscriptionModel, is_base=True, lifecycle=[SubscriptionLifecycle.INITIAL, SubscriptionLifecycle.TERMINATED]
):
    node: NodeProductBlockInactive | None = None

    def get_corelinks(self) -> list[Sn8Corelink]:
        assert self.node
        block_id = ProductBlockTable.find_by_tag("CA").product_block_id
        corelinks = [
            Sn8Corelink.from_subscription(in_use_by_block.subscription_id)
            for in_use_by_block in self.node.in_use_by
            if in_use_by_block.product_block_id == block_id
        ]
        return corelinks

    def get_ports(self) -> list[Sn8ServicePort]:
        assert self.node
        block_id = ProductBlockTable.find_by_name("SN8 Service Port").product_block_id
        ports = [
            Sn8ServicePort.from_subscription(block_relation.subscription_id)
            for block_relation in self.node.in_use_by
            if block_relation.product_block_id == block_id
        ]
        return ports

    def get_ports_in_use(self) -> list[Sn8ServicePort]:
        ports = self.get_ports()
        return [port for port in ports if is_active_sub(port)]

    @property
    def irb_port(self) -> Sn8IrbServicePort | None:
        assert self.node
        block_id = ProductBlockTable.find_by_name("SN8 IRB Service Port").product_block_id
        ports = [
            Sn8IrbServicePort.from_subscription(in_use_by_block.subscription_id)
            for in_use_by_block in self.node.in_use_by
            if in_use_by_block.product_block_id == block_id
        ]
        ports = [port for port in ports if port.status != SubscriptionLifecycle.TERMINATED]
        return only(ports)


class NodeInactive(NodeInitial):
    node: NodeProductBlockInactive


class NodeProvisioning(NodeInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    node: NodeProductBlockProvisioning


class Node(NodeProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    node: NodeProductBlock
