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


from pydantic import Field

from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SubscriptionLifecycle


class FirewallServiceSettingsBlockInactive(ProductBlockModel, product_block_name="Firewall Service Settings"):
    customer_asn: int | None = None
    customer_ptp_ipv4_ipam_id: list[int] = Field(default_factory=list)
    customer_ptp_ipv6_ipam_id: list[int] = Field(default_factory=list)


class FirewallServiceSettingsBlockProvisioning(
    FirewallServiceSettingsBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    customer_asn: int
    customer_ptp_ipv4_ipam_id: list[int] = Field(default_factory=list)
    customer_ptp_ipv6_ipam_id: list[int] = Field(default_factory=list)


class FirewallServiceSettingsBlock(FirewallServiceSettingsBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    customer_asn: int
    customer_ptp_ipv4_ipam_id: list[int]
    customer_ptp_ipv6_ipam_id: list[int]
