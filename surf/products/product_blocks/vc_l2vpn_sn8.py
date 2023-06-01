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

from surf.products.product_blocks.esi_l2vpn import Sn8L2VpnEsiBlock, Sn8L2VpnEsiBlockInactive


class ListOfLeastPossibleEsis(SubscriptionInstanceList[SI]):
    min_items = 1


class ListOfEsis(ListOfLeastPossibleEsis, SubscriptionInstanceList[SI]):
    min_items = 2


class Sn8L2VpnVirtualCircuitBlockInactive(ProductBlockModel, product_block_name="SN8 L2VPN Virtual Circuit"):
    esis: ListOfLeastPossibleEsis[Sn8L2VpnEsiBlockInactive]

    service_speed: int | None = None
    speed_policer: bool | None = None
    vlan_retagging: bool | None = None
    bum_filter: bool | None = None
    ims_circuit_id: int | None = None
    nso_service_id: UUID | None = None


class Sn8L2VpnVirtualCircuitBlockProvisioning(
    Sn8L2VpnVirtualCircuitBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    esis: ListOfLeastPossibleEsis[Sn8L2VpnEsiBlock]

    service_speed: int
    speed_policer: bool
    vlan_retagging: bool
    bum_filter: bool
    ims_circuit_id: int | None = None
    nso_service_id: UUID | None = None

    @serializable_property
    def title(self) -> str:
        return f"{self.tag} {format_bandwidth(self.service_speed)}"


class Sn8L2VpnVirtualCircuitBlock(Sn8L2VpnVirtualCircuitBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    esis: ListOfEsis[Sn8L2VpnEsiBlock]

    service_speed: int
    speed_policer: bool
    vlan_retagging: bool
    bum_filter: bool
    ims_circuit_id: int
    nso_service_id: UUID
