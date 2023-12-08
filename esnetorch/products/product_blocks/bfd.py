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

from uuid import UUID, uuid4

from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SubscriptionLifecycle
from pydantic import Field

# In here, we define the values expected for a product block at each phase of the of the Subscription Lifecycle
# All resource types used by a product block need to be explicitly called out here and assigned
# expected types

# BFD Template Product Blocks


class BFDTemplateInactive(ProductBlockModel, product_block_name="BFD Template"):
    """A BFD Template Instance in the Inactive State

    Here, we generate a UUID that will eventually be sent to NSO as the
    primary key used to reference this product block. All other values
    are set to be empty, and will be populated by the NES CREATE workflow.
    """

    uuid: UUID = Field(default_factory=uuid4)
    template_name: str | None
    interval: int | None
    multiplier: int | None


class BFDTemplateProvisioning(BFDTemplateInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """A BFD Template Instance in the Provisioning state

    In this state, the UUID will have already been set upon instantiation,
    and all other values will be instantiated once the NES CREATE workflow
    has been run.

    All values are now fully required at this state.
    """

    uuid: UUID
    template_name: str
    interval: int
    multiplier: int


class BFDTemplate(BFDTemplateProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """A BFD Template Instance in the Active state.

    All values are now fully required.
    """

    uuid: UUID
    template_name: str
    interval: int
    multiplier: int


# S-BFD Reflector
class SBFDReflectorInactive(ProductBlockModel, product_block_name="S-BFD Reflector"):
    """An s-BFD Reflector configuration instance. Here, we generate a
    UUID that will eventually be sent to NSO as the primary key used
    to reference this product block. All other values are set to be empty,
    and will be populated by the "Provision NES" workflow.
    """

    uuid: UUID = Field(default_factory=uuid4)
    discriminator: int | None = None


class SBFDReflectorProvisioning(SBFDReflectorInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """An s-BFD Reflector configuration instance. There are no changes
    to this model in the provisioning lifecycle state.
    """

    uuid: UUID
    discriminator: int | None


class SBFDReflector(SBFDReflectorProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """An s-BFD Reflector configuration instance.

    All values are now fully required.
    """

    uuid: UUID
    discriminator: int
