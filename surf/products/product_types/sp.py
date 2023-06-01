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

from orchestrator.domain.base import SubscriptionModel, serializable_property
from orchestrator.types import SubscriptionLifecycle
from orchestrator.utils.vlans import VlanRanges

from surf.products.product_blocks.resource_type_types import PortMode
from surf.products.product_blocks.sp import (
    ServicePortBlock,
    ServicePortBlockInactive,
    ServicePortBlockProvisioning,
    Sn8ServicePortBlock,
    Sn8ServicePortBlockInactive,
    Sn8ServicePortBlockProvisioning,
)
from surf.products.product_types.fixed_input_types import Domain, PortSpeed
from surf.services import ims


class ServicePortInactive(SubscriptionModel):
    domain: Domain
    port: ServicePortBlockInactive | None = None

    @serializable_property
    def port_speed(self) -> int:
        return self.get_port_speed()

    def get_port_mode(self) -> PortMode:
        return PortMode.TAGGED

    def get_port_speed(self) -> int:
        # raise ValueError("SN7 subscriptions not supported")
        return 0

    def get_port_node_subscription_id(self) -> UUID:
        raise ValueError("No node subscription for SN7 subscriptions")

    def get_port_used_vlans(self) -> VlanRanges:
        raise ValueError("SN7 subscriptions not supported")


class ServicePortProvisioning(ServicePortInactive):
    domain: Domain
    port: ServicePortBlockProvisioning


class ServicePort(ServicePortProvisioning):
    domain: Domain
    port: ServicePortBlock


# Extra model for handling showing pre domain model wf subscriptions
class Sn8ServicePortInitial(
    ServicePortInactive, is_base=True, lifecycle=[SubscriptionLifecycle.INITIAL, SubscriptionLifecycle.TERMINATED]
):
    domain: Domain
    # Next variable allows combination of a property (calculated) and an actual class member with the same name
    aliased_port_speed: PortSpeed = Field(alias="port_speed")

    port: Sn8ServicePortBlockInactive | None = None


class Sn8ServicePortInactive(Sn8ServicePortInitial):
    domain: Domain
    aliased_port_speed: PortSpeed = Field(alias="port_speed")
    port: Sn8ServicePortBlockInactive

    def get_port_mode(self) -> PortMode:
        return self.port.get_port_mode()

    def get_port_speed(self) -> int:
        assert self.aliased_port_speed
        return self.aliased_port_speed.value

    def get_port_node_subscription_id(self) -> UUID:
        return self.port.get_port_node_subscription_id()

    def get_port_used_vlans(self) -> VlanRanges:
        return VlanRanges(ims.get_vlans_by_subscription_id(self.subscription_id))


class Sn8ServicePortProvisioning(
    Sn8ServicePortInactive, ServicePortProvisioning, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    domain: Domain
    aliased_port_speed: PortSpeed = Field(alias="port_speed")
    port: Sn8ServicePortBlockProvisioning


class Sn8ServicePort(Sn8ServicePortProvisioning, ServicePort, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    domain: Domain
    aliased_port_speed: PortSpeed = Field(alias="port_speed")
    port: Sn8ServicePortBlock
