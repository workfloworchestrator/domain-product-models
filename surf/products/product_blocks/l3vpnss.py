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


from orchestrator.domain.base import ProductBlockModel, serializable_property
from orchestrator.types import SubscriptionLifecycle

from surf.products.product_blocks.resource_type_types import Asn


class Sn8L3VpnServiceSettingsBlockInactive(ProductBlockModel, product_block_name="L3VPN Service Settings"):
    asn: Asn | None = None


class Sn8L3VpnServiceSettingsBlock(
    Sn8L3VpnServiceSettingsBlockInactive, lifecycle=[SubscriptionLifecycle.ACTIVE, SubscriptionLifecycle.PROVISIONING]
):
    asn: Asn

    @serializable_property
    def title(self) -> str:
        return f"{self.tag} AS{self.asn}"
