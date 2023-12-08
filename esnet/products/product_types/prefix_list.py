# The products for the layer 3 product - contains all three of the
# products - service port, l3 service and peering

from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SubscriptionLifecycle

from esnetorch.products.product_blocks.prefix_list import (
    PrefixListBlock,
    PrefixListBlockInactive,
    PrefixListBlockProvisioning,
)
from esnetorch.products.product_types.fixed_input_types import RoutingDomain


class PrefixListInactive(SubscriptionModel, is_base=True):
    prefix_list: PrefixListBlockInactive
    routing_domain: RoutingDomain


class PrefixListProvisioning(PrefixListInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    prefix_list: PrefixListBlockProvisioning
    routing_domain: RoutingDomain


class PrefixList(PrefixListProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    prefix_list: PrefixListBlock
    routing_domain: RoutingDomain
