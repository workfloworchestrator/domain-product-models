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


from pydantic import ConstrainedInt

from orchestrator.domain.base import ProductBlockModel, serializable_property
from orchestrator.types import SubscriptionLifecycle


class DomainId(ConstrainedInt):
    ge = 1
    le = 2_147_483_647


class ZoneId(ConstrainedInt):
    ge = 1
    le = 2_147_483_647


class SurfDomainSettingsBlockInactive(ProductBlockModel, product_block_name="surf Domain Settings"):
    dns_name: str | None = None
    domain_id: DomainId | None = None
    zone_id: ZoneId | None = None
    dns_sec: bool | None = False
    dns_sec_in_transition: bool | None = False


class SurfDomainSettingsBlockProvisioning(
    SurfDomainSettingsBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    dns_name: str
    domain_id: DomainId | None = None
    zone_id: ZoneId | None = None
    dns_sec: bool
    dns_sec_in_transition: bool

    @serializable_property
    def title(self) -> str:
        return f"{self.name}"


class SurfDomainSettingsBlock(SurfDomainSettingsBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    dns_name: str
    domain_id: DomainId | None = None
    zone_id: ZoneId | None = None
    dns_sec: bool
    dns_sec_in_transition: bool
