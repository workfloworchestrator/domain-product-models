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

from typing import Optional
from uuid import UUID

from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SubscriptionLifecycle

# Blocks for L3 Service product


class L3BlockInactive(ProductBlockModel, product_block_name="L3 Block"):
    route_table: Optional[str] = None
    l3_type: Optional[str] = None
    nso_service_id: Optional[str] = None
    service_edge_subscription_id: Optional[UUID] = None
    prefix_list_subscription_id: Optional[UUID] = None


class L3BlockProvisioning(L3BlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    route_table: str
    l3_type: str
    nso_service_id: str
    service_edge_subscription_id: UUID
    prefix_list_subscription_id: UUID


class L3Block(L3BlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    route_table: str
    l3_type: str
    nso_service_id: str
    service_edge_subscription_id: UUID
    prefix_list_subscription_id: UUID
