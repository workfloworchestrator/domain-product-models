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

from esnetorch.products.product_blocks.nes import (
    NodeEnrollmentBlock,
    NodeEnrollmentBlockInactive,
    NodeEnrollmentBlockProvisioning,
)

# In here, we define the values expected for a product block at each phase of the of the Subscription Lifecycle
# All resource types used by a product block need to be explicitly called out here and assigned
# expected types


class NodeEnrollmentMPRInactive(SubscriptionModel, is_base=True):
    ne: NodeEnrollmentBlockInactive


class NodeEnrollmentMPRProvisioning(NodeEnrollmentMPRInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    ne: NodeEnrollmentBlockProvisioning


class NodeEnrollmentMPR(NodeEnrollmentMPRProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    ne: NodeEnrollmentBlock
