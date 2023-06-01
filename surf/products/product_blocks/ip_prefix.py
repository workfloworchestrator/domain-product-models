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

from orchestrator.domain.base import ProductBlockModel, SubscriptionModel, serializable_property
from orchestrator.types import SubscriptionLifecycle


class IpPrefixBlockInactive(ProductBlockModel, product_block_name="IP_PREFIX"):
    """Object model for a IP Prefix product block in initial state."""

    customer_aggregate: bool | None = None
    to_internet: bool | None = None
    planned: bool | None = None
    ipam_prefix_id: int | None = None
    parent_prefix: Optional["IpPrefixBlockInactive"] = None  # Forward references fail with new optional notation
    extra_information: str | None = None


class IpPrefixBlockProvisioning(IpPrefixBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """Object model for a IP Prefix product block."""

    customer_aggregate: bool
    to_internet: bool
    planned: bool
    ipam_prefix_id: int | None = None
    parent_prefix: Optional["IpPrefixBlockProvisioning"] = None  # Forward references fail with new optional notation
    extra_information: str | None = None

    @serializable_property
    def title(self) -> str:
        subscription = SubscriptionModel.from_subscription(self.owner_subscription_id)
        return f"{subscription.description}"


class IpPrefixBlock(IpPrefixBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """Object model for a IP Prefix product block."""

    customer_aggregate: bool
    to_internet: bool
    planned: bool
    ipam_prefix_id: int
    parent_prefix: Optional["IpPrefixBlock"] = None  # Forward references fail with new optional notation
    extra_information: str | None = None
