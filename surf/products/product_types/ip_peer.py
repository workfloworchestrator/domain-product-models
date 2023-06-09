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

from surf.products.product_blocks.ip_peer import IpPeerBlock, IpPeerBlockInactive, IpPeerBlockProvisioning
from surf.products.product_types.fixed_input_types import Domain


class IpPeerInactive(SubscriptionModel, is_base=True):
    domain: Domain
    ip_peer_block: IpPeerBlockInactive


class IpPeerProvisioning(IpPeerInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    domain: Domain
    ip_peer_block: IpPeerBlockProvisioning


class IpPeer(IpPeerProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    domain: Domain
    ip_peer_block: IpPeerBlock
