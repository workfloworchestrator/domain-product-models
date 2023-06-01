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

from surf.products.product_blocks.vc_ip_bgp_sn8 import (
    Sn8IpBgpVirtualCircuitBlock,
    Sn8IpBgpVirtualCircuitBlockInactive,
    Sn8IpBgpVirtualCircuitBlockProvisioning,
)
from surf.products.product_blocks.vc_l2vpn_sn8 import (
    Sn8L2VpnVirtualCircuitBlock,
    Sn8L2VpnVirtualCircuitBlockInactive,
    Sn8L2VpnVirtualCircuitBlockProvisioning,
)


class FwIpGwEndpointBlockInactive(ProductBlockModel, product_block_name="FW IP Gateway Endpoint"):
    endpoint_description: str | None = None
    l2vpn_internal: Sn8L2VpnVirtualCircuitBlockInactive
    ip: Sn8IpBgpVirtualCircuitBlockInactive


class FwIpGwEndpointBlockProvisioning(FwIpGwEndpointBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    endpoint_description: str
    l2vpn_internal: Sn8L2VpnVirtualCircuitBlockProvisioning
    ip: Sn8IpBgpVirtualCircuitBlockProvisioning

    @serializable_property
    def title(self) -> str:
        return f"{self.name} {self.description}"


class FwIpGwEndpointBlock(FwIpGwEndpointBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    endpoint_description: str
    l2vpn_internal: Sn8L2VpnVirtualCircuitBlock
    ip: Sn8IpBgpVirtualCircuitBlock
