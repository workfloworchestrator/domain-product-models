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

from surf.products.product_blocks.fw_ip_gw_endpoint import (
    FwIpGwEndpointBlock,
    FwIpGwEndpointBlockInactive,
    FwIpGwEndpointBlockProvisioning,
)
from surf.products.product_blocks.fw_l2_endpoint import (
    FwL2EndpointBlock,
    FwL2EndpointBlockInactive,
    FwL2EndpointBlockProvisioning,
)
from surf.products.product_blocks.fw_l3_endpoint import (
    FwL3EndpointBlock,
    FwL3EndpointBlockInactive,
    FwL3EndpointBlockProvisioning,
)
from surf.products.product_blocks.resource_type_types import FwDeployType


class ListOfL2Endpoints(SubscriptionInstanceList[SI]):
    min_items = 0


class ListOfL3Endpoints(SubscriptionInstanceList[SI]):
    min_items = 0


class ListOfFwIpGwEndpoints(SubscriptionInstanceList[SI]):
    min_items = 0
    max_items = 1


class FwBlockInactive(ProductBlockModel, product_block_name="FW"):
    asn: int | None = None
    nfv_service_id: str | None = None
    customer_asn: int | None = None
    availability_zone_name: str | None = None
    l2_endpoints: ListOfL2Endpoints[FwL2EndpointBlockInactive]
    l3_endpoints: ListOfL3Endpoints[FwL3EndpointBlockInactive]
    ip_gw_endpoint: FwIpGwEndpointBlockInactive | None
    deploy_type: FwDeployType | None = None


class FwBlockProvisioning(FwBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    asn: int
    nfv_service_id: str
    customer_asn: int
    availability_zone_name: str
    l2_endpoints: ListOfL2Endpoints[FwL2EndpointBlockProvisioning]
    l3_endpoints: ListOfL3Endpoints[FwL3EndpointBlockProvisioning]
    ip_gw_endpoint: FwIpGwEndpointBlockProvisioning | None
    deploy_type: FwDeployType


class FwBlock(FwBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    asn: int
    nfv_service_id: str
    customer_asn: int
    availability_zone_name: str
    l2_endpoints: ListOfL2Endpoints[FwL2EndpointBlock]
    l3_endpoints: ListOfL3Endpoints[FwL3EndpointBlock]
    ip_gw_endpoint: FwIpGwEndpointBlock | None
    deploy_type: FwDeployType

    @serializable_property
    def title(self) -> str:
        return f"{self.tag} {self.availability_zone_name} {self.customer_asn}"
