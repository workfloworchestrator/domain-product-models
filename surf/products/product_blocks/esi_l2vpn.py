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

from surf.products.product_blocks.sap_sn8 import Sn8ServiceAttachPointBlock, Sn8ServiceAttachPointBlockInactive


class ListOfSaps(SubscriptionInstanceList[SI]):
    min_items = 1


class Sn8L2VpnEsiBlockInactive(ProductBlockModel, product_block_name="SN8 L2VPN ESI"):
    """Object model for a ESI as used by a L2VPN in SN8."""

    saps: ListOfSaps[Sn8ServiceAttachPointBlockInactive]


class Sn8L2VpnEsiBlock(
    Sn8L2VpnEsiBlockInactive,
    lifecycle=[SubscriptionLifecycle.ACTIVE, SubscriptionLifecycle.PROVISIONING],
):
    saps: ListOfSaps[Sn8ServiceAttachPointBlock]

    @serializable_property
    def title(self) -> str:
        nso_device_ids = ",".join(sap.node.nso_device_id for sap in self.saps)
        return f"{self.tag} {nso_device_ids} VLAN {self.saps[0].vlanrange}"
