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

from surf.products.product_blocks.lrss import (
    Sn8LightPathRedundantServiceSettingsBlock,
    Sn8LightPathRedundantServiceSettingsBlockInactive,
    Sn8LightPathRedundantServiceSettingsBlockProvisioning,
)
from surf.products.product_types.fixed_input_types import Domain, ProtectionType


class Sn8LightPathRedundantInactive(SubscriptionModel, is_base=True):
    domain: Domain
    protection_type: ProtectionType
    lrss: Sn8LightPathRedundantServiceSettingsBlockInactive


class Sn8LightPathRedundantProvisioning(Sn8LightPathRedundantInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    domain: Domain
    protection_type: ProtectionType
    lrss: Sn8LightPathRedundantServiceSettingsBlockProvisioning


class Sn8LightPathRedundant(Sn8LightPathRedundantProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """SN8 Light Path Redundant domain model.

    Attributes:
        domain: SURFNET8 or NETHERLIGHT8 to distinguish between de surf and NetherLight products. See:
            :class:`~surf.products.product_types.fixed_input_types.Domain`
        protection_type: Protected or Redundant To distinguish between redundant and protected LightPaths. See:
            :class:`~surf.products.product_types.fixed_input_types.ProtectionType`
        lrss: Virtual Circuit data. See :class:`~surf.products.product_blocks.lrss.Sn8LightPathRedundantServiceSettingsBlock`

    """

    domain: Domain
    protection_type: ProtectionType
    lrss: Sn8LightPathRedundantServiceSettingsBlock
