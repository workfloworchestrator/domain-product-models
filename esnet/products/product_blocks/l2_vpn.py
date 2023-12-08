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
