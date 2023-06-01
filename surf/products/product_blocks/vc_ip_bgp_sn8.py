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
from orchestrator.utils.speed import format_bandwidth

from surf.products.product_blocks.ipss_bgp import Sn8IpBgpServiceSettingsBlock, Sn8IpBgpServiceSettingsBlockInactive
from surf.products.product_blocks.sap_ip_sn8 import (
    Sn8IpBgpServiceAttachPointSettingsBlock,
    Sn8IpBgpServiceAttachPointSettingsBlockInactive,
    Sn8IpBgpServiceAttachPointSettingsBlockProvisioning,
)


class ListOfIpBgpSapsProvisioning(SubscriptionInstanceList[SI]):
    min_items = 0
    max_items = 6


class ListOfIpBgpSaps(ListOfIpBgpSapsProvisioning[SI]):
    min_items = 1


class Sn8IpBgpVirtualCircuitBlockInactive(ProductBlockModel, product_block_name="IP BGP Virtual Circuit"):
    settings: Sn8IpBgpServiceSettingsBlockInactive
    saps: ListOfIpBgpSapsProvisioning[Sn8IpBgpServiceAttachPointSettingsBlockInactive]

    service_speed: int | None = None
    ims_circuit_id: int | None = None
    nso_service_id: UUID | None = None


class Sn8IpBgpVirtualCircuitBlockProvisioning(
    Sn8IpBgpVirtualCircuitBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    settings: Sn8IpBgpServiceSettingsBlock
    saps: ListOfIpBgpSapsProvisioning[Sn8IpBgpServiceAttachPointSettingsBlockProvisioning]

    service_speed: int
    ims_circuit_id: int | None = None
    nso_service_id: UUID | None = None

    @serializable_property
    def title(self) -> str:
        return f"{self.tag} {format_bandwidth(self.service_speed)}"


class Sn8IpBgpVirtualCircuitBlock(Sn8IpBgpVirtualCircuitBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    settings: Sn8IpBgpServiceSettingsBlock
    saps: ListOfIpBgpSaps[Sn8IpBgpServiceAttachPointSettingsBlock]

    service_speed: int
    ims_circuit_id: int
    nso_service_id: UUID
