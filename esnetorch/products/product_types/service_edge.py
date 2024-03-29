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

from esnetorch.products.product_blocks.service_edge import EdgeBlock, EdgeBlockInactive, EdgeBlockProvisioning
from esnetorch.products.product_types.fixed_input_types import RoutingDomain


class ServiceEdgeInactive(SubscriptionModel, is_base=True):
    edge: EdgeBlockInactive
    routing_domain: RoutingDomain


class ServiceEdgeProvisioning(ServiceEdgeInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    edge: EdgeBlockProvisioning
    routing_domain: RoutingDomain


class ServiceEdge(ServiceEdgeProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    edge: EdgeBlock
    routing_domain: RoutingDomain
