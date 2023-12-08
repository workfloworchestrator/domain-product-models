from typing import Optional
from uuid import UUID

from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SubscriptionLifecycle

# Blocks for L3 Service product


class L3BlockInactive(ProductBlockModel, product_block_name="L3 Block"):
    route_table: Optional[str] = None
    l3_type: Optional[str] = None
    nso_service_id: Optional[str] = None
    service_edge_subscription_id: Optional[UUID] = None
    prefix_list_subscription_id: Optional[UUID] = None


class L3BlockProvisioning(L3BlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    route_table: str
    l3_type: str
    nso_service_id: str
    service_edge_subscription_id: UUID
    prefix_list_subscription_id: UUID


class L3Block(L3BlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    route_table: str
    l3_type: str
    nso_service_id: str
    service_edge_subscription_id: UUID
    prefix_list_subscription_id: UUID
