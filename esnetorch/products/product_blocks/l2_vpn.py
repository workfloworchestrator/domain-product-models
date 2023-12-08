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

from typing import Optional

from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SubscriptionLifecycle


class L2VPNMemberBlockInactive(ProductBlockModel, product_block_name="L2 VPN Member Block"):
    esdb_l2vpn_id: Optional[int] = None
    esdb_l2vpn_name: Optional[str] = None


class L2VPNMemberBlockProvisioning(L2VPNMemberBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    esdb_l2vpn_id: Optional[int] = None
    esdb_l2vpn_name: Optional[str] = None


class L2VPNMemberBlock(L2VPNMemberBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    esdb_l2vpn_id: int
    esdb_l2vpn_name: str
