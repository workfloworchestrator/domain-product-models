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

from surf.products.product_blocks.l3vpnss import Sn8L3VpnServiceSettingsBlock, Sn8L3VpnServiceSettingsBlockInactive
from surf.products.product_blocks.resource_type_types import SpecificTemplateType
from surf.products.product_blocks.sap_settings_l3vpn_sn8 import (
    Sn8L3VpnServiceAttachPointSettingsBlock,
    Sn8L3VpnServiceAttachPointSettingsBlockInactive,
)


class ListOfL3VpnSapsProvisioning(SubscriptionInstanceList[SI]):
    min_items = 0


class ListOfL3VpnSaps(ListOfL3VpnSapsProvisioning[SI]):
    min_items = 1


class Sn8L3VpnVirtualCircuitBlockInactive(ProductBlockModel, product_block_name="SN8 L3VPN Virtual Circuit"):
    settings: Sn8L3VpnServiceSettingsBlockInactive
    saps: ListOfL3VpnSapsProvisioning[Sn8L3VpnServiceAttachPointSettingsBlockInactive]

    service_speed: int | None = None
    speed_policer: bool | None = None
    ims_circuit_id: int | None = None
    nso_service_id: UUID | None = None
    specific_template: SpecificTemplateType | None = None


class Sn8L3VpnVirtualCircuitBlockProvisioning(
    Sn8L3VpnVirtualCircuitBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    settings: Sn8L3VpnServiceSettingsBlock
    saps: ListOfL3VpnSapsProvisioning[Sn8L3VpnServiceAttachPointSettingsBlock]

    service_speed: int
    speed_policer: bool
    ims_circuit_id: int | None = None
    nso_service_id: UUID | None = None
    specific_template: SpecificTemplateType | None = None

    @serializable_property
    def title(self) -> str:
        return f"{self.tag} {format_bandwidth(self.service_speed)}"


class Sn8L3VpnVirtualCircuitBlock(Sn8L3VpnVirtualCircuitBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """Virtual Circuit data."""

    settings: Sn8L3VpnServiceSettingsBlock
    saps: ListOfL3VpnSaps[Sn8L3VpnServiceAttachPointSettingsBlock]

    service_speed: int
    speed_policer: bool
    ims_circuit_id: int
    nso_service_id: UUID
    specific_template: SpecificTemplateType | None
