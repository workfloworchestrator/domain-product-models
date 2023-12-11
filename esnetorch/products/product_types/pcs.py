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

from esnetorch.products.product_blocks.pcs import (
    PhysicalConnectionBlock,
    PhysicalConnectionBlockInactive,
    PhysicalConnectionBlockProvisioning,
)

# In here, we define for a subscription instance of a product
# what is expected in terms of the product blocks.  Since there is only a single product
# block for Physical Connection, we only have a single entry at each state


class PhysicalConnectionInactive(SubscriptionModel, is_base=True):
    pc: PhysicalConnectionBlockInactive


class PhysicalConnectionProvisioning(PhysicalConnectionInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    pc: PhysicalConnectionBlockProvisioning


class PhysicalConnection(PhysicalConnectionProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    pc: PhysicalConnectionBlock
