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
from orchestrator.utils.speed import speed_humanize

from surf.products.product_blocks.node import NodeProductBlock
from surf.products.product_blocks.resource_type_types import PortMode


class ServicePortBlockInactive(ProductBlockModel):
    """Base object model for all Inactive SN8 Service Port product blocks.

    This class is being used for functionality that is generic to all Sn8 Service Ports. By design this domain model
    is READ ONLY, at least for now. It provides a generic interface to attributes you can find on all service ports.
    """

    ims_circuit_id: int | None = None


class ServicePortBlockProvisioning(ServicePortBlockInactive):
    """Base object model for all Provisioning SN8 Service Port product blocks.

    This class is being used for functionality that is generic to all Sn8 Service Ports. By design this domain model
    is READ ONLY, at least for now. It provides a generic interface to attributes you can find on all service ports.
    """

    ims_circuit_id: int | None = None


class ServicePortBlock(ServicePortBlockProvisioning):
    """Base object model for all Active SN8 Service Port product blocks.

    This class is being used for functionality that is generic to all Sn8 Service Ports. By design this domain model
    is READ ONLY, at least for now. It provides a generic interface to attributes you can find on all service ports.
    """

    ims_circuit_id: int


class Sn8ServicePortBlockInactive(ServicePortBlockInactive, product_block_name="SN8 Service Port"):
    """Object model for a SN8 Service Port product block."""

    nso_service_id: UUID | None = None
    port_mode: PortMode | None = None
    lldp: bool | None = None
    ims_circuit_id: int | None = None
    auto_negotiation: bool | None = None
    ignore_l3_incompletes: bool | None = None
    node: NodeProductBlock | None = None
    native_vlan: int | None = None

    def get_port_mode(self) -> PortMode:
        assert self.port_mode
        return self.port_mode

    def get_port_node_subscription_id(self) -> UUID:
        assert self.node
        return self.node.owner_subscription_id


class Sn8ServicePortBlockProvisioning(
    Sn8ServicePortBlockInactive, ServicePortBlockProvisioning, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    """Object model for a SN8 Service Port product block in provisioning state."""

    nso_service_id: UUID
    port_mode: PortMode
    lldp: bool
    ims_circuit_id: int | None = None
    auto_negotiation: bool | None = None
    ignore_l3_incompletes: bool | None = None
    node: NodeProductBlock
    native_vlan: int | None = None

    @serializable_property
    def title(self) -> str:
        from surf.products.product_types.sp import ServicePort

        port_speed = ServicePort.from_subscription(self.owner_subscription_id).get_port_speed()
        speed = speed_humanize(port_speed, short=True)

        return f"{self.tag} {self.node.nso_device_id} {speed} {self.port_mode}"


class Sn8ServicePortBlock(Sn8ServicePortBlockProvisioning, ServicePortBlock, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """Object model for a SN8 Service Port product block in active state."""

    nso_service_id: UUID
    port_mode: PortMode
    lldp: bool
    ims_circuit_id: int
    auto_negotiation: bool | None = None
    ignore_l3_incompletes: bool
    node: NodeProductBlock
    native_vlan: int | None = None
