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

from surf.products.product_blocks.corelink import (
    Sn8CorelinkBlock,
    Sn8CorelinkBlockInactive,
    Sn8CorelinkBlockProvisioning,
)


# Extra model for handling showing pre domain model wf subscriptions
class Sn8CorelinkInitial(SubscriptionModel, is_base=True, lifecycle=[SubscriptionLifecycle.INITIAL]):
    corelink: Sn8CorelinkBlockInactive | None = None


class Sn8CorelinkInactive(Sn8CorelinkInitial):
    corelink: Sn8CorelinkBlockInactive


class Sn8CorelinkProvisioning(Sn8CorelinkInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    corelink: Sn8CorelinkBlockProvisioning


class Sn8Corelink(Sn8CorelinkProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    corelink: Sn8CorelinkBlock
