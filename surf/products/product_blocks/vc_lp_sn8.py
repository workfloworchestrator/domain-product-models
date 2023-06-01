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

from orchestrator.domain.base import SI, ProductBlockModel, SubscriptionInstanceList, serializable_property
from orchestrator.types import SubscriptionLifecycle
from orchestrator.utils.speed import speed_humanize

from surf.products.product_blocks.sap_sn8 import Sn8ServiceAttachPointBlock, Sn8ServiceAttachPointBlockInactive


class ListOfSaps(SubscriptionInstanceList[SI]):
    min_items = 2
    max_items = 2


class Sn8LightPathVirtualCircuitBlockInactive(ProductBlockModel, product_block_name="SN8 Light Path Virtual Circuit"):
    saps: ListOfSaps[Sn8ServiceAttachPointBlockInactive]

    service_speed: int | None = None
    speed_policer: bool | None = None
    remote_port_shutdown: bool | None = None
    ims_circuit_id: int | None = None
    nso_service_id: UUID | None = None


class Sn8LightPathVirtualCircuitBlockProvisioning(
    Sn8LightPathVirtualCircuitBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    saps: ListOfSaps[Sn8ServiceAttachPointBlock]

    service_speed: int
    speed_policer: bool
    remote_port_shutdown: bool
    ims_circuit_id: int | None = None
    nso_service_id: UUID | None = None

    @serializable_property
    def title(self) -> str:
        return f"{self.tag} {speed_humanize(self.service_speed)}"


class Sn8LightPathVirtualCircuitBlock(
    Sn8LightPathVirtualCircuitBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]
):
    saps: ListOfSaps[Sn8ServiceAttachPointBlock]

    service_speed: int
    speed_policer: bool
    remote_port_shutdown: bool
    ims_circuit_id: int
    nso_service_id: UUID
