from typing import List, Optional, TypeVar
from uuid import UUID

from orchestrator.domain.base import ProductBlockModel, SubscriptionInstanceList
from orchestrator.types import SubscriptionLifecycle
from pydantic import Field

from esnetorch.products.product_blocks.bfd import (
    BFDTemplate,
    BFDTemplateInactive,
    BFDTemplateProvisioning,
    SBFDReflector,
    SBFDReflectorInactive,
    SBFDReflectorProvisioning,
)
from esnetorch.products.product_blocks.pcs import (
    EquipmentInterfaceBlock,
    EquipmentInterfaceBlockInactive,
    EquipmentInterfaceBlockProvisioning,
)

# In here, we define the values expected for a product block at each phase of the of the Subscription Lifecycle
# All resource types used by a product block need to be explicitly called out here and assigned
# expected types

T = TypeVar("T", covariant=True)


class ListOfInterfaces(SubscriptionInstanceList[T]):
    max_items = 2


class NodeEnrollmentBlockInactive(ProductBlockModel, product_block_name="Node Enrollment"):
    """Object model for a Node Enrollment as used by Node Enrollment Service"""

    # when first created we expect all resources to be none
    esdb_node_id: Optional[int] = None
    esdb_node_uuid: Optional[UUID] = None
    node_name: Optional[str] = None
    nso_service_id: Optional[UUID] = None
    v6_loopback: Optional[str] = None
    routing_domain: Optional[str] = None
    v4_loopback: Optional[str] = None
    mgmt_ports: ListOfInterfaces[EquipmentInterfaceBlockInactive]
    bfd_templates: List[BFDTemplateInactive] = Field(
        default_factory=list
    )  # This allows empty lists for MPRs, TPDRs, etc.
    sbfd_reflector: Optional[SBFDReflectorInactive] = None


class NodeEnrollmentBlockProvisioning(NodeEnrollmentBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """Node Enrollment with optional fields to use in the provisioning lifecycle state."""

    # In the Provisioning state, there will be an ESDB node, Device Group, and NSO service assigned
    esdb_node_id: int
    esdb_node_uuid: UUID
    node_name: str
    nso_service_id: UUID
    v6_loopback: str
    v4_loopback: Optional[str] = None
    routing_domain: Optional[str] = None
    mgmt_ports: ListOfInterfaces[EquipmentInterfaceBlockProvisioning]
    bfd_templates: List[BFDTemplateProvisioning] = Field(
        default_factory=list
    )  # This allows empty lists for MPRs, TPDRs, etc.
    sbfd_reflector: Optional[SBFDReflectorProvisioning] = None


class NodeEnrollmentBlock(NodeEnrollmentBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """Node Enrollment with optional fields to use in the active lifecycle state."""

    # In the active state, there will be an ESDB node, Device Group, and NSO service assigned
    esdb_node_id: int
    esdb_node_uuid: UUID
    node_name: str
    nso_service_id: UUID
    v6_loopback: str
    routing_domain: str
    v4_loopback: Optional[str] = None
    mgmt_ports: ListOfInterfaces[EquipmentInterfaceBlock]
    bfd_templates: List[BFDTemplate] = Field(default_factory=list)  # This allows empty lists for MPRs, TPDRs, etc.
    sbfd_reflector: Optional[SBFDReflector] = None
