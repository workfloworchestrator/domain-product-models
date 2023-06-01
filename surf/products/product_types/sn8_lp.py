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

from surf.products.product_blocks.vc_lp_sn8 import (
    Sn8LightPathVirtualCircuitBlock,
    Sn8LightPathVirtualCircuitBlockInactive,
    Sn8LightPathVirtualCircuitBlockProvisioning,
)
from surf.products.product_types.fixed_input_types import Domain, ProtectionType


class Sn8LightPathInactive(SubscriptionModel, is_base=True):
    domain: Domain
    protection_type: ProtectionType
    vc: Sn8LightPathVirtualCircuitBlockInactive


class Sn8LightPathProvisioning(Sn8LightPathInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    domain: Domain
    protection_type: ProtectionType
    vc: Sn8LightPathVirtualCircuitBlockProvisioning


class Sn8LightPath(Sn8LightPathProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """SN8 Light Path domain model.

    Attributes:
        domain: SURFNET8 or NETHERLIGHT8 to distinguish between de surf and NetherLight products. See:
            :class:`~surf.products.product_types.fixed_input_types.Domain`
        protection_type: Protected or Redundant To distinguish between redundant and protected LightPaths. See:
            :class:`~surf.products.product_types.fixed_input_types.ProtectionType`
        vc: Virtual Circuit data. See :class:`~surf.products.product_blocks.vc_lp_sn8.Sn8LightPathVirtualCircuitBlock`

    """

    domain: Domain
    protection_type: ProtectionType
    vc: Sn8LightPathVirtualCircuitBlock
