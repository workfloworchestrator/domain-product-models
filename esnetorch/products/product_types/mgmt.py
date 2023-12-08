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

from esnetorch.products.product_blocks.blink import (
    BackboneLinkBlock,
    BackboneLinkBlockInactive,
    BackboneLinkBlockProvisioning,
)
from esnetorch.products.product_types.fixed_input_types import Flavor, IsisService

# Product definition for Backbone Link Service.


class ManagementLinkInactive(SubscriptionModel, is_base=True):
    blink: BackboneLinkBlockInactive
    flavor: Flavor
    isis_service: IsisService


class ManagementLinkProvisioning(ManagementLinkInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    blink: BackboneLinkBlockProvisioning
    flavor: Flavor
    isis_service: IsisService


class ManagementLink(ManagementLinkProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    blink: BackboneLinkBlock
    flavor: Flavor
    isis_service: IsisService
