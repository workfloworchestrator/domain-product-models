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

from pydantic import Field

from orchestrator.domain.base import ProductBlockModel, serializable_property
from orchestrator.types import SubscriptionLifecycle

from surf.products.product_blocks.ip_prefix import IpPrefixBlock
from surf.products.product_blocks.resource_type_types import Asn, SurfCertFilter


class Sn8IpBgpServiceSettingsBlockInactive(ProductBlockModel, product_block_name="IP BGP Service Settings"):
    asn: Asn | None = None
    surfcert_filter_enabled: bool | None = None
    surfcert_filter: SurfCertFilter | None = None
    multicast: bool | None = None
    pin_prefix: list[IpPrefixBlock] = Field(default_factory=list)

    @property
    def internetpinnen_prefix_subscription_id(self) -> list[UUID]:
        return [prefix.owner_subscription_id for prefix in self.pin_prefix]


class Sn8IpBgpServiceSettingsBlock(
    Sn8IpBgpServiceSettingsBlockInactive, lifecycle=[SubscriptionLifecycle.ACTIVE, SubscriptionLifecycle.PROVISIONING]
):
    asn: Asn
    surfcert_filter_enabled: bool
    surfcert_filter: SurfCertFilter
    multicast: bool
    pin_prefix: list[IpPrefixBlock]

    @serializable_property
    def title(self) -> str:
        surfcert_filter_enabled = "enabled" if self.surfcert_filter_enabled else "disabled"
        return f"{self.tag} AS{self.asn} CERTfilter {surfcert_filter_enabled}"
