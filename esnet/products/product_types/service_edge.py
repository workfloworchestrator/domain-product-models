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
