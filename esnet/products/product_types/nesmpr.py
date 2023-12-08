from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SubscriptionLifecycle

from esnetorch.products.product_blocks.nes import (
    NodeEnrollmentBlock,
    NodeEnrollmentBlockInactive,
    NodeEnrollmentBlockProvisioning,
)

# In here, we define the values expected for a product block at each phase of the of the Subscription Lifecycle
# All resource types used by a product block need to be explicitly called out here and assigned
# expected types


class NodeEnrollmentMPRInactive(SubscriptionModel, is_base=True):
    ne: NodeEnrollmentBlockInactive


class NodeEnrollmentMPRProvisioning(NodeEnrollmentMPRInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    ne: NodeEnrollmentBlockProvisioning


class NodeEnrollmentMPR(NodeEnrollmentMPRProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    ne: NodeEnrollmentBlock
