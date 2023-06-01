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

from orchestrator.domain.base import serializable_property
from orchestrator.types import SubscriptionLifecycle
from orchestrator.utils.speed import speed_humanize

from surf.products.product_blocks.irb import Sn8IrbServicePortBlock
from surf.products.product_blocks.node import NodeProductBlock
from surf.products.product_blocks.resource_type_types import PortMode
from surf.products.product_blocks.sn8_aggsp import Sn8AggregatedServicePortBlock
from surf.products.product_blocks.sp import (
    ServicePortBlock,
    ServicePortBlockInactive,
    ServicePortBlockProvisioning,
    Sn8ServicePortBlock,
)
from surf.products.product_types.sp import ServicePort


class Sn8MscBlockInactive(ServicePortBlockInactive, product_block_name="Service Port Multi Service Carrier SN8"):
    """Object model for a SN8 Multi Service Carrier product block."""

    port: Sn8ServicePortBlock | Sn8AggregatedServicePortBlock | Sn8IrbServicePortBlock | None = None

    @property
    def port_subscription_id(self) -> UUID | None:
        return self.port.owner_subscription_id if self.port else None

    service_tag: int | None = None
    ims_circuit_id: int | None = None

    def get_port_mode(self) -> PortMode:
        return PortMode.TAGGED

    def get_port_speed(self) -> int:
        if not self.port_subscription_id:
            return 0
        # check if it's an MSC based on normal SP's or on aggregated SP's
        return ServicePort.from_subscription(self.port_subscription_id).get_port_speed()

    def get_port_node_subscription_id(self) -> UUID:
        assert self.port_subscription_id
        # check if it's an MSC based on normal SP's or on aggregated SP's
        return ServicePort.from_subscription(self.port_subscription_id).get_port_node_subscription_id()


class Sn8MscBlockProvisioning(
    Sn8MscBlockInactive, ServicePortBlockProvisioning, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    """Object model for a SN8 Multi Service Carrier product block in provisioning state."""

    port: Sn8ServicePortBlock | Sn8AggregatedServicePortBlock | Sn8IrbServicePortBlock

    @property
    def port_subscription_id(self) -> UUID:
        return self.port.owner_subscription_id

    service_tag: int
    ims_circuit_id: int | None = None

    @property
    def node(self) -> NodeProductBlock:
        match self.port:
            case Sn8AggregatedServicePortBlock() as aggsp:
                return aggsp.node
            case Sn8ServicePortBlock() as sp:
                return sp.node
            case Sn8IrbServicePortBlock() as irbsp:
                return irbsp.node

    @serializable_property
    def title(self) -> str:
        speed = speed_humanize(self.get_port_speed(), short=True)
        return f"{self.tag} {self.node.nso_device_id} {speed} {self.get_port_mode()}"


class Sn8MscBlock(Sn8MscBlockProvisioning, ServicePortBlock, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """Object model for a SN8 Multi Service Carrier product block in active state."""

    port: Sn8ServicePortBlock | Sn8AggregatedServicePortBlock | Sn8IrbServicePortBlock
    service_tag: int
    ims_circuit_id: int
