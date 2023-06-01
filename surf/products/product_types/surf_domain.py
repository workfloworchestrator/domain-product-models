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

from surf.products.product_blocks.surf_domain_settings import (
    SurfDomainSettingsBlock,
    SurfDomainSettingsBlockInactive,
    SurfDomainSettingsBlockProvisioning,
)
from surf.products.product_types.fixed_input_types import Domain


class SURFdomainInactive(SubscriptionModel, is_base=True):
    domain: Domain
    domain_settings: SurfDomainSettingsBlockInactive


class SURFdomainProvisioning(SURFdomainInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    domain: Domain
    domain_settings: SurfDomainSettingsBlockProvisioning


class SURFdomain(SURFdomainProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    domain: Domain
    domain_settings: SurfDomainSettingsBlock
