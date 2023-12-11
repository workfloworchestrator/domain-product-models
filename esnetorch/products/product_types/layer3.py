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

from esnetorch.products.product_blocks.layer3 import L3Block, L3BlockInactive, L3BlockProvisioning
from esnetorch.products.product_types.fixed_input_types import RoutingDomain

# l3 service


class L3ServiceInactive(SubscriptionModel, is_base=True):
    l3_block: L3BlockInactive
    routing_domain: RoutingDomain


class L3ServiceProvisioning(L3ServiceInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    l3_block: L3BlockProvisioning
    routing_domain: RoutingDomain


class L3Service(L3ServiceProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    l3_block: L3Block
    routing_domain: RoutingDomain
