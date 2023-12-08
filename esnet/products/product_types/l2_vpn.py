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
