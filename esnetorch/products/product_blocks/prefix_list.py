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

from typing import List, Optional, TypeVar
from uuid import UUID

from orchestrator.domain.base import ProductBlockModel, SubscriptionInstanceList
from orchestrator.types import SubscriptionLifecycle

T = TypeVar("T", covariant=True)


class ListOfPrefixLists(SubscriptionInstanceList[T]):
    min_items = 0


class PrefixListBlockInactive(ProductBlockModel, product_block_name="Prefix List"):
    asn: Optional[int] = None
    esdb_peer_id: Optional[int] = None
    peer_type: Optional[str] = None
    prefix_manager_id: Optional[str] = None
    route_table: Optional[str] = None
    node_enrollment_subscription_id: Optional[List[UUID]] = None


class PrefixListBlockProvisioning(PrefixListBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    asn: int = None
    esdb_peer_id: int = None
    peer_type: str = None
    prefix_manager_id: str = None
    route_table: str = None
    node_enrollment_subscription_id: Optional[List[UUID]] = None


class PrefixListBlock(PrefixListBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    asn: int
    esdb_peer_id: int
    peer_type: str
    prefix_manager_id: str
    route_table: str
    node_enrollment_subscription_id: List[UUID]
