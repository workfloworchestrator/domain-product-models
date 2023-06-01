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

from orchestrator.domain.base import SubscriptionInstanceList, serializable_property
from orchestrator.types import SubscriptionLifecycle
from orchestrator.utils.speed import speed_humanize

from surf.products.product_blocks.irb import Sn8IrbServicePortBlock
from surf.products.product_blocks.node import NodeProductBlock
from surf.products.product_blocks.resource_type_types import AggregatedPortMode, PortMode
from surf.products.product_blocks.sp import (
    ServicePortBlock,
    ServicePortBlockInactive,
    ServicePortBlockProvisioning,
    Sn8ServicePortBlock,
)
from surf.products.product_types.sp import Sn8ServicePort

MAX_LINK_MEMBER_PORTS = 8


class ListOfPortsInactive(SubscriptionInstanceList[Sn8ServicePortBlock | Sn8IrbServicePortBlock]):
    max_items = MAX_LINK_MEMBER_PORTS


class Sn8AggregatedServicePortBlockInactive(ServicePortBlockInactive, product_block_name="SN8 Aggregated Service Port"):
    """ServiceAttachPointLightpathSN8 with optional fields to use in the initial lifecycle state."""

    port_mode: AggregatedPortMode | None = None
    port: ListOfPortsInactive = Field(default_factory=list)  # type: ignore
    nso_service_id: UUID | None = None
    ims_circuit_id: int | None = None

    @property
    def port_subscription_id(self) -> list[UUID]:
        return [port.owner_subscription_id for port in self.port]

    def get_port_mode(self) -> PortMode:
        assert self.port_mode
        return self.port_mode.value

    def get_port_speed(self) -> int:
        return sum(Sn8ServicePort.from_subscription(sub).get_port_speed() for sub in self.port_subscription_id)

    def get_port_node_subscription_id(self) -> UUID:
        assert self.port_subscription_id
        port_subscription_lm = Sn8ServicePort.from_subscription(self.port_subscription_id[0])
        assert port_subscription_lm.port.node
        return port_subscription_lm.port.node.owner_subscription_id


class Sn8AggregatedServicePortBlockProvisioning(
    Sn8AggregatedServicePortBlockInactive, ServicePortBlockProvisioning, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    """Object model for a Service Attach Point as used by a Lightpath in SN8."""

    port_mode: AggregatedPortMode
    port: ListOfPortsInactive

    @property
    def port_subscription_id(self) -> list[UUID]:
        return [port.owner_subscription_id for port in self.port]

    nso_service_id: UUID | None = None
    ims_circuit_id: int | None = None

    @property
    def node(self) -> NodeProductBlock:
        # All ports on same node, get the first one
        port_subscription_lm = Sn8ServicePort.from_subscription(self.port_subscription_id[0])
        return port_subscription_lm.port.node

    @serializable_property
    def title(self) -> str:
        speed = speed_humanize(self.get_port_speed(), short=True)
        return f"{self.tag} {self.node.nso_device_id} {speed} {self.get_port_mode()}"


class ListOfPorts(ListOfPortsInactive):
    min_items = 1


class Sn8AggregatedServicePortBlock(
    Sn8AggregatedServicePortBlockProvisioning, ServicePortBlock, lifecycle=[SubscriptionLifecycle.ACTIVE]
):
    """Object model for a Service Attach Point as used by a Lightpath in SN8."""

    port_mode: AggregatedPortMode
    port: ListOfPorts

    @property
    def port_subscription_id(self) -> list[UUID]:
        return [port.owner_subscription_id for port in self.port]

    nso_service_id: UUID
    ims_circuit_id: int
