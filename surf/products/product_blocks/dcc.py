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

from surf.products.product_blocks.sn8_aggsp import Sn8AggregatedServicePortBlock
from surf.products.product_blocks.sp import Sn8ServicePortBlock
from surf.products.product_blocks.sp_msc_sn8 import Sn8MscBlock


class ListOfPorts(SubscriptionInstanceList[SI]):
    min_items = 1


class DirectCloudConnectivityBlockInactive(ProductBlockModel, product_block_name="Direct Cloud Connectivity"):
    """Object model for a Direct Cloud Connectivity product block in initial state."""

    service_key: str | None = None
    ports: list[Sn8ServicePortBlock | Sn8MscBlock | Sn8AggregatedServicePortBlock] = []
    zone_name: str | None = None


class DirectCloudConnectivityBlockProvisioning(
    DirectCloudConnectivityBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    """Object model for a Direct Cloud Connectivity product block."""

    service_key: str | None = None
    ports: ListOfPorts[Sn8ServicePortBlock | Sn8MscBlock | Sn8AggregatedServicePortBlock]
    zone_name: str | None = None


class DirectCloudConnectivityBlock(DirectCloudConnectivityBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """Object model for a Direct Cloud Connectivity product block."""

    service_key: str | None = None
    ports: ListOfPorts[Sn8ServicePortBlock | Sn8MscBlock | Sn8AggregatedServicePortBlock]
    zone_name: str

    @serializable_property
    def title(self) -> str:
        return f"{self.name}"
