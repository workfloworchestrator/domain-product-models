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


class WifiLocationInactive(ProductBlockModel, product_block_name="Wifi Location"):
    ap_vendor_name: str | None = None
    location_name: str | None = None
    jira_location_id: str | None = None

    @serializable_property
    def title(self) -> str:
        return f"{self.name}"


class WifiLocationProvisioning(WifiLocationInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    ap_vendor_name: str
    location_name: str | None
    jira_location_id: str | None


class WifiLocation(WifiLocationProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    ap_vendor_name: str
    location_name: str
    jira_location_id: str
