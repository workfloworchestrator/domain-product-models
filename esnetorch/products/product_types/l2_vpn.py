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

from esnetorch.products.product_blocks.l2_vpn import (
    L2VPNMemberBlock,
    L2VPNMemberBlockInactive,
    L2VPNMemberBlockProvisioning,
)
from esnetorch.products.product_blocks.service_edge import EdgeBlock, EdgeBlockInactive, EdgeBlockProvisioning


class L2VPNMemberInactive(SubscriptionModel, is_base=True):
    l2_vpn_member: L2VPNMemberBlockInactive
    edge: EdgeBlockInactive


class L2VPNMemberProvisioning(L2VPNMemberInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    l2_vpn_member: L2VPNMemberBlockProvisioning
    edge: EdgeBlockProvisioning


class L2VPNMember(L2VPNMemberProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    l2_vpn_member: L2VPNMemberBlock
    edge: EdgeBlock
