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

from surf.products.product_blocks.esi_l2vpn import Sn8L2VpnEsiBlock, Sn8L2VpnEsiBlockInactive


class ListOfEsis(SubscriptionInstanceList[SI]):
    min_items = 1


class FwL2EndpointBlockInactive(ProductBlockModel, product_block_name="FW L2 Endpoint"):
    endpoint_description: str | None = None
    customer_ptp_ipv4_primary_ipam_id: int | None = None
    customer_ptp_ipv4_secondary_ipam_ids: list[int] = []
    customer_ptp_ipv6_primary_ipam_id: int | None = None
    customer_ptp_ipv6_secondary_ipam_ids: list[int] = []
    esis: list[Sn8L2VpnEsiBlockInactive] = []


class FwL2EndpointBlockProvisioning(FwL2EndpointBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    endpoint_description: str
    customer_ptp_ipv4_primary_ipam_id: int | None = None
    customer_ptp_ipv4_secondary_ipam_ids: list[int]
    customer_ptp_ipv6_primary_ipam_id: int | None = None
    customer_ptp_ipv6_secondary_ipam_ids: list[int]
    esis: ListOfEsis[Sn8L2VpnEsiBlock]

    @serializable_property
    def title(self) -> str:
        return f"{self.name} {self.description}"


class FwL2EndpointBlock(FwL2EndpointBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    endpoint_description: str
    customer_ptp_ipv4_primary_ipam_id: int | None = None
    customer_ptp_ipv4_secondary_ipam_ids: list[int]
    customer_ptp_ipv6_primary_ipam_id: int | None = None
    customer_ptp_ipv6_secondary_ipam_ids: list[int]
    esis: ListOfEsis[Sn8L2VpnEsiBlock]
