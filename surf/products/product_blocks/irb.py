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

from surf.products.product_blocks.node import NodeProductBlock
from surf.products.product_blocks.sp import ServicePortBlock, ServicePortBlockInactive, ServicePortBlockProvisioning


class Sn8IrbServicePortBlockInactive(ServicePortBlockInactive, product_block_name="SN8 IRB Service Port"):
    """Object model for a SN8 IRB Service Port product block."""

    nso_service_id: UUID | None = None
    ims_circuit_id: int | None = None
    node: NodeProductBlock | None = None


class Sn8IrbServicePortBlockProvisioning(
    Sn8IrbServicePortBlockInactive, ServicePortBlockProvisioning, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    """Object model for a SN8 IRB Service Port product block in provisioning state."""

    nso_service_id: UUID
    ims_circuit_id: int | None = None
    node: NodeProductBlock

    @serializable_property
    def title(self) -> str:
        return f"{self.tag} {self.node.nso_device_id}"


class Sn8IrbServicePortBlock(
    Sn8IrbServicePortBlockProvisioning, ServicePortBlock, lifecycle=[SubscriptionLifecycle.ACTIVE]
):
    """Object model for a SN8 IRB Service Port product block in active state."""

    nso_service_id: UUID
    ims_circuit_id: int
    node: NodeProductBlock
