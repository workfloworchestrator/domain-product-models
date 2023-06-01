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

from enum import Enum, auto
from uuid import UUID

from orchestrator.types import SubscriptionLifecycle

from surf.products.product_blocks.resource_type_types import PortMode
from surf.products.product_blocks.sn8_aggsp import (
    Sn8AggregatedServicePortBlock,
    Sn8AggregatedServicePortBlockInactive,
    Sn8AggregatedServicePortBlockProvisioning,
)
from surf.products.product_types.fixed_input_types import Domain
from surf.products.product_types.sp import ServicePort, ServicePortInactive, ServicePortProvisioning


class Sn8AggregatedServicePortPart(Enum):
    AGG = auto()
    PTP = auto()


class Sn8AggregatedServicePortInactive(ServicePortInactive, is_base=True):
    domain: Domain
    port: Sn8AggregatedServicePortBlockInactive

    def get_port_mode(self) -> PortMode:
        return self.port.get_port_mode()

    def get_port_speed(self) -> int:
        return self.port.get_port_speed()

    def get_port_node_subscription_id(self) -> UUID:
        return self.port.get_port_node_subscription_id()


class Sn8AggregatedServicePortProvisioning(
    Sn8AggregatedServicePortInactive, ServicePortProvisioning, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    domain: Domain
    port: Sn8AggregatedServicePortBlockProvisioning


class Sn8AggregatedServicePort(
    Sn8AggregatedServicePortProvisioning, ServicePort, lifecycle=[SubscriptionLifecycle.ACTIVE]
):
    domain: Domain
    port: Sn8AggregatedServicePortBlock
