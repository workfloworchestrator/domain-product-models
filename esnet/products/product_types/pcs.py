from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SubscriptionLifecycle

from esnetorch.products.product_blocks.pcs import (
    PhysicalConnectionBlock,
    PhysicalConnectionBlockInactive,
    PhysicalConnectionBlockProvisioning,
)

# In here, we define for a subscription instance of a product
# what is expected in terms of the product blocks.  Since there is only a single product
# block for Physical Connection, we only have a single entry at each state


class PhysicalConnectionInactive(SubscriptionModel, is_base=True):
    pc: PhysicalConnectionBlockInactive


class PhysicalConnectionProvisioning(PhysicalConnectionInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    pc: PhysicalConnectionBlockProvisioning


class PhysicalConnection(PhysicalConnectionProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    pc: PhysicalConnectionBlock
