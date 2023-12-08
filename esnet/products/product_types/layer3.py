# The products for the layer 3 product - contains all three of the
# products - service port, l3 service and peering

from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SubscriptionLifecycle

from esnetorch.products.product_blocks.layer3 import L3Block, L3BlockInactive, L3BlockProvisioning
from esnetorch.products.product_types.fixed_input_types import RoutingDomain

# l3 service


class L3ServiceInactive(SubscriptionModel, is_base=True):
    l3_block: L3BlockInactive
    routing_domain: RoutingDomain


class L3ServiceProvisioning(L3ServiceInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    l3_block: L3BlockProvisioning
    routing_domain: RoutingDomain


class L3Service(L3ServiceProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    l3_block: L3Block
    routing_domain: RoutingDomain
