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
from orchestrator.utils.speed import format_bandwidth

from surf.products.product_blocks.ipss_static import (
    Sn8IpStaticServiceSettingsBlock,
    Sn8IpStaticServiceSettingsBlockInactive,
)
from surf.products.product_blocks.sap_ip_sn8 import (
    Sn8IpStaticServiceAttachPointSettingsBlock,
    Sn8IpStaticServiceAttachPointSettingsBlockInactive,
    Sn8IpStaticServiceAttachPointSettingsBlockProvisioning,
)


class Sn8IpStaticVirtualCircuitBlockInactive(ProductBlockModel, product_block_name="IP Static Virtual Circuit"):
    sap: Sn8IpStaticServiceAttachPointSettingsBlockInactive | None
    settings: Sn8IpStaticServiceSettingsBlockInactive

    service_speed: int | None = None
    ims_circuit_id: int | None = None
    nso_service_id: UUID | None = None


class Sn8IpStaticVirtualCircuitBlockProvisioning(
    Sn8IpStaticVirtualCircuitBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    sap: Sn8IpStaticServiceAttachPointSettingsBlockProvisioning | None
    settings: Sn8IpStaticServiceSettingsBlock

    service_speed: int
    ims_circuit_id: int | None = None
    nso_service_id: UUID | None = None

    @serializable_property
    def title(self) -> str:
        return f"{self.tag} {format_bandwidth(self.service_speed)}"


class Sn8IpStaticVirtualCircuitBlock(
    Sn8IpStaticVirtualCircuitBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]
):
    sap: Sn8IpStaticServiceAttachPointSettingsBlock
    settings: Sn8IpStaticServiceSettingsBlock

    service_speed: int
    ims_circuit_id: int
    nso_service_id: UUID
