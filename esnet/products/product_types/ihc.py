from orchestrator.domain.base import SubscriptionModel
from orchestrator.types import SubscriptionLifecycle

from esnetorch.products.product_blocks.ihc import (
    InternalHostConnectivityBlock,
    InternalHostConnectivityBlockInactive,
    InternalHostConnectivityBlockProvisioning,
)


class InternalHostConnectivityInactive(SubscriptionModel, is_base=True):
    internal_host_connectivity_block: InternalHostConnectivityBlockInactive


class InternalHostConnectivityProvisioning(
    InternalHostConnectivityInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    internal_host_connectivity_block: InternalHostConnectivityBlockProvisioning


class InternalHostConnectivity(InternalHostConnectivityProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    internal_host_connectivity_block: InternalHostConnectivityBlock
