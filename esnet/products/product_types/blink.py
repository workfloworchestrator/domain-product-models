from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SubscriptionLifecycle

from esnetorch.products.product_blocks.blink import (
    BackboneLinkBlock,
    BackboneLinkBlockInactive,
    BackboneLinkBlockProvisioning,
)
from esnetorch.products.product_types.fixed_input_types import Flavor, IsisService

# Product definition for Backbone Link.


class BackboneLinkInactive(SubscriptionModel, is_base=True):
    blink: BackboneLinkBlockInactive
    flavor: Flavor
    isis_service: IsisService


class BackboneLinkProvisioning(BackboneLinkInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    blink: BackboneLinkBlockProvisioning
    flavor: Flavor
    isis_service: IsisService


class BackboneLink(BackboneLinkProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    blink: BackboneLinkBlock
    flavor: Flavor
    isis_service: IsisService
