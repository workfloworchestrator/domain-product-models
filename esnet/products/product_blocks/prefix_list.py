from typing import List, Optional, TypeVar
from uuid import UUID

from orchestrator.domain.base import ProductBlockModel, SubscriptionInstanceList
from orchestrator.types import SubscriptionLifecycle

T = TypeVar("T", covariant=True)


class ListOfPrefixLists(SubscriptionInstanceList[T]):
    min_items = 0


class PrefixListBlockInactive(ProductBlockModel, product_block_name="Prefix List"):
    asn: Optional[int] = None
    esdb_peer_id: Optional[int] = None
    peer_type: Optional[str] = None
    prefix_manager_id: Optional[str] = None
    route_table: Optional[str] = None
    node_enrollment_subscription_id: Optional[List[UUID]] = None


class PrefixListBlockProvisioning(PrefixListBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    asn: int = None
    esdb_peer_id: int = None
    peer_type: str = None
    prefix_manager_id: str = None
    route_table: str = None
    node_enrollment_subscription_id: Optional[List[UUID]] = None


class PrefixListBlock(PrefixListBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    asn: int
    esdb_peer_id: int
    peer_type: str
    prefix_manager_id: str
    route_table: str
    node_enrollment_subscription_id: List[UUID]
