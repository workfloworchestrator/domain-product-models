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

from orchestrator.types import SubscriptionLifecycle

from surf.config import MAX_SPEED_POSSIBLE
from surf.products.product_blocks.irb import (
    Sn8IrbServicePortBlock,
    Sn8IrbServicePortBlockInactive,
    Sn8IrbServicePortBlockProvisioning,
)
from surf.products.product_blocks.resource_type_types import PortMode
from surf.products.product_types.fixed_input_types import Domain
from surf.products.product_types.sp import ServicePort, ServicePortInactive, ServicePortProvisioning


class Sn8IrbServicePortInactive(ServicePortInactive, is_base=True):
    """Object model for a SN8 IRB Service Port product."""

    domain: Domain
    port: Sn8IrbServicePortBlockInactive

    def get_port_mode(self) -> PortMode:
        return PortMode.TAGGED

    def get_port_speed(self) -> int:
        return MAX_SPEED_POSSIBLE

    def get_port_node_subscription_id(self) -> UUID:
        assert self.port.node
        return self.port.node.owner_subscription_id


class Sn8IrbServicePortProvisioning(
    Sn8IrbServicePortInactive, ServicePortProvisioning, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    """Object model for a SN8 IRB Service Port product."""

    domain: Domain
    port: Sn8IrbServicePortBlockProvisioning


class Sn8IrbServicePort(Sn8IrbServicePortProvisioning, ServicePort, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """Object model for a SN8 IRB Service Port product."""

    domain: Domain
    port: Sn8IrbServicePortBlock
