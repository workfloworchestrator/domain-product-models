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

from orchestrator.domain.base import (
    SI,
    ProductBlockModel,
    SubscriptionInstanceList,
    SubscriptionModel,
    serializable_property,
)
from orchestrator.types import SubscriptionLifecycle

from surf.products.product_blocks.corelink_aggregate import (
    Sn8CorelinkAggregateBlock,
    Sn8CorelinkAggregateBlockInactive,
    Sn8CorelinkAggregateBlockProvisioning,
)
from surf.products.product_blocks.corelink_port_pair import (
    Sn8CorelinkPortPairBlock,
    Sn8CorelinkPortPairBlockInactive,
    Sn8CorelinkPortPairBlockProvisioning,
)


class ListOfAggregates(SubscriptionInstanceList[SI]):
    min_items = 2
    max_items = 2


class ListOfPortPairs(SubscriptionInstanceList[SI]):
    min_items = 1
    max_items = 8


class Sn8CorelinkBlockInactive(ProductBlockModel, product_block_name="Corelink"):
    """Object model for a Corelink product block in initial state."""

    aggregates: ListOfAggregates[Sn8CorelinkAggregateBlockInactive]
    port_pairs: ListOfPortPairs[Sn8CorelinkPortPairBlockInactive]

    isis_metric: int | None = None
    nso_service_id: UUID | None = None
    ims_circuit_id: int | None = None
    maintenance_mode: bool = False


class Sn8CorelinkBlockProvisioning(Sn8CorelinkBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """Object model for a Corelink product block in initial state."""

    aggregates: ListOfAggregates[Sn8CorelinkAggregateBlockProvisioning]
    port_pairs: ListOfPortPairs[Sn8CorelinkPortPairBlockProvisioning]

    isis_metric: int
    nso_service_id: UUID
    ims_circuit_id: int | None = None
    maintenance_mode: bool

    @serializable_property
    def title(self) -> str:
        subscription = SubscriptionModel.from_subscription(self.owner_subscription_id)
        return f"{subscription.description}"


class Sn8CorelinkBlock(Sn8CorelinkBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """Object model for a Corelink product block."""

    aggregates: ListOfAggregates[Sn8CorelinkAggregateBlock]
    port_pairs: ListOfPortPairs[Sn8CorelinkPortPairBlock]

    isis_metric: int
    nso_service_id: UUID
    ims_circuit_id: int
    maintenance_mode: bool
