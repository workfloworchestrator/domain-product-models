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

from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SubscriptionLifecycle

from esnetorch.products.product_blocks.prefix_list import (
    PrefixListBlock,
    PrefixListBlockInactive,
    PrefixListBlockProvisioning,
)
from esnetorch.products.product_types.fixed_input_types import RoutingDomain


class PrefixListInactive(SubscriptionModel, is_base=True):
    prefix_list: PrefixListBlockInactive
    routing_domain: RoutingDomain


class PrefixListProvisioning(PrefixListInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    prefix_list: PrefixListBlockProvisioning
    routing_domain: RoutingDomain


class PrefixList(PrefixListProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    prefix_list: PrefixListBlock
    routing_domain: RoutingDomain
