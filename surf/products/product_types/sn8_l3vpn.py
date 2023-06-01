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

from surf.products.product_blocks.vc_l3vpn_sn8 import (
    Sn8L3VpnVirtualCircuitBlock,
    Sn8L3VpnVirtualCircuitBlockInactive,
    Sn8L3VpnVirtualCircuitBlockProvisioning,
)
from surf.products.product_types.fixed_input_types import Domain


class Sn8L3VpnInactive(SubscriptionModel, is_base=True):
    domain: Domain
    vc: Sn8L3VpnVirtualCircuitBlockInactive


class Sn8L3VpnProvisioning(Sn8L3VpnInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    domain: Domain
    vc: Sn8L3VpnVirtualCircuitBlockProvisioning


class Sn8L3Vpn(Sn8L3VpnProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    domain: Domain
    vc: Sn8L3VpnVirtualCircuitBlock
