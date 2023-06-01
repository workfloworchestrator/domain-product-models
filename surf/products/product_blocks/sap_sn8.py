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

from orchestrator.domain.base import ProductBlockModel, serializable_property
from orchestrator.types import SubscriptionLifecycle
from orchestrator.utils.vlans import VlanRanges

from surf.products.product_blocks.irb import Sn8IrbServicePortBlock
from surf.products.product_blocks.node import NodeProductBlock
from surf.products.product_blocks.sn8_aggsp import Sn8AggregatedServicePortBlock
from surf.products.product_blocks.sp import Sn8ServicePortBlock
from surf.products.product_blocks.sp_msc_sn8 import Sn8MscBlock


class Sn8ServiceAttachPointBlockInactive(ProductBlockModel, product_block_name="SN8 Service Attach Point"):
    """Object model for a Service Attach Point as used in SN8."""

    port: Sn8ServicePortBlock | Sn8MscBlock | Sn8AggregatedServicePortBlock | Sn8IrbServicePortBlock | None = None

    @property
    def port_subscription_id(self) -> UUID | None:
        return self.port.owner_subscription_id if self.port else None

    vlanrange: VlanRanges | None = None


class Sn8ServiceAttachPointBlock(
    Sn8ServiceAttachPointBlockInactive,
    lifecycle=[SubscriptionLifecycle.ACTIVE, SubscriptionLifecycle.PROVISIONING],
):
    """ServiceAttachPointSN8 with fields to use in the active lifecycle state."""

    port: Sn8ServicePortBlock | Sn8MscBlock | Sn8AggregatedServicePortBlock | Sn8IrbServicePortBlock

    @property
    def port_subscription_id(self) -> UUID:
        return self.port.owner_subscription_id

    vlanrange: VlanRanges

    @property
    def node(self) -> NodeProductBlock:
        match self.port:
            case Sn8AggregatedServicePortBlock() as aggsp:
                return aggsp.node
            case Sn8ServicePortBlock() as sp:
                return sp.node
            case Sn8IrbServicePortBlock() as irbsp:
                return irbsp.node
            case Sn8MscBlock() as msc:
                return msc.node

    @serializable_property
    def title(self) -> str:
        return f"{self.tag} {self.node.nso_device_id} {self.vlanrange}"
