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

from orchestrator.domain.base import SI, ProductBlockModel, SubscriptionInstanceList, serializable_property
from orchestrator.types import SubscriptionLifecycle

from surf.products.product_blocks.vc_lp_sn8 import (
    Sn8LightPathVirtualCircuitBlock,
    Sn8LightPathVirtualCircuitBlockInactive,
    Sn8LightPathVirtualCircuitBlockProvisioning,
)


class ListOfVcs(SubscriptionInstanceList[SI]):
    min_items = 2
    max_items = 2


class Sn8LightPathRedundantServiceSettingsBlockInactive(ProductBlockModel, product_block_name="LR Service Settings"):
    vcs: ListOfVcs[Sn8LightPathVirtualCircuitBlockInactive]

    ims_protection_circuit_id: int | None = None

    @serializable_property
    def title(self) -> str:
        return f"{self.name}"


class Sn8LightPathRedundantServiceSettingsBlockProvisioning(
    Sn8LightPathRedundantServiceSettingsBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    vcs: ListOfVcs[Sn8LightPathVirtualCircuitBlockProvisioning]

    ims_protection_circuit_id: int | None = None


class Sn8LightPathRedundantServiceSettingsBlock(
    Sn8LightPathRedundantServiceSettingsBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]
):
    vcs: ListOfVcs[Sn8LightPathVirtualCircuitBlock]

    ims_protection_circuit_id: int
