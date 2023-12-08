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


class NodeEnrollmentInactive(SubscriptionModel, is_base=True):
    # Equipment state is planned
    ne: NodeEnrollmentBlockInactive


class NodeEnrollmentProvisioning(NodeEnrollmentInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    # Equipment state is Commissioning
    ne: NodeEnrollmentBlockProvisioning


class NodeEnrollment(NodeEnrollmentProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    # Equipment state is Provisioned
    ne: NodeEnrollmentBlock
