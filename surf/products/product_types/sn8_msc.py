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

from surf.products.product_blocks.resource_type_types import PortMode
from surf.products.product_blocks.sp_msc_sn8 import Sn8MscBlock, Sn8MscBlockInactive, Sn8MscBlockProvisioning
from surf.products.product_types.fixed_input_types import Domain
from surf.products.product_types.sp import ServicePort, ServicePortInactive, ServicePortProvisioning


class Sn8MscInactive(ServicePortInactive, is_base=True):
    """Object model for a SN8 Multi Service Carrier product."""

    domain: Domain
    port: Sn8MscBlockInactive

    def get_port_mode(self) -> PortMode:
        return self.port.get_port_mode()

    def get_port_speed(self) -> int:
        return self.port.get_port_speed()

    def get_port_node_subscription_id(self) -> UUID:
        return self.port.get_port_node_subscription_id()


class Sn8MscProvisioning(Sn8MscInactive, ServicePortProvisioning, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """Object model for a SN8 Multi Service Carrier product."""

    domain: Domain
    port: Sn8MscBlockProvisioning


class Sn8Msc(Sn8MscProvisioning, ServicePort, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """Object model for a SN8 Multi Service Carrier product."""

    domain: Domain
    port: Sn8MscBlock
