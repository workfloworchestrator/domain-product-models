from typing import Optional, TypeVar
from uuid import UUID

from orchestrator.domain.base import ProductBlockModel, SubscriptionInstanceList
from orchestrator.types import SubscriptionLifecycle

# Product Block definitions for Backbone Link Service

# Constrained lists for models

T = TypeVar("T", covariant=True)


class ListOfMembers(SubscriptionInstanceList[T]):
    min_items = 1
    max_items = 16


class PortPair(SubscriptionInstanceList[T]):
    min_items = 2
    max_items = 2


# Backbone Link Interface


class BackboneLinkInterfaceBlockInactive(ProductBlockModel, product_block_name="Backbone Link Interface"):
    """Object model for a Backbone Link Interface as used by
    Backbone Link Service"""

    port_identifier: Optional[str] = None
    esdb_equipment_interface_id: Optional[int] = None
    nso_service_id: Optional[UUID] = None
    dns_name: Optional[str] = None
    port_type: Optional[str] = None
    eth_encap: Optional[str] = None
    vlan: Optional[int] = None
    ipv4_address: Optional[str] = None
    ipv6_address: Optional[str] = None
    adjacency_sid_v4: Optional[int] = None
    adjacency_sid_v6: Optional[int] = None


class BackboneLinkInterfaceBlockProvisioning(
    BackboneLinkInterfaceBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    """Backbone Link Interface with fields for use in the provisioning lifecycle"""

    port_identifier: Optional[str] = None
    esdb_equipment_interface_id: Optional[int] = None
    nso_service_id: Optional[UUID] = None
    dns_name: Optional[str] = None
    port_type: Optional[str] = None
    eth_encap: Optional[str] = None
    vlan: Optional[int] = None
    ipv4_address: Optional[str] = None
    ipv6_address: Optional[str] = None
    adjacency_sid_v4: Optional[int] = None
    adjacency_sid_v6: Optional[int] = None


class BackboneLinkInterfaceBlock(BackboneLinkInterfaceBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """Backbone Link Interface with fields for use in the provisioning lifecycle"""

    port_identifier: str
    esdb_equipment_interface_id: int
    nso_service_id: UUID
    dns_name: str
    port_type: str
    eth_encap: str
    vlan: int
    ipv4_address: str
    ipv6_address: str
    adjacency_sid_v4: Optional[int]
    adjacency_sid_v6: Optional[int]


# Backbone Link Member


class BackboneLinkMemberBlockInactive(ProductBlockModel, product_block_name="Backbone Link Member"):
    """Object model for a Backbone Link Member as used by
    Backbone Link Service"""

    # DO NOT declare additional nested classes as Option[class] = None
    port_pair: PortPair[BackboneLinkInterfaceBlockInactive]
    esdb_circuit_id: Optional[str] = None
    nso_service_id: Optional[UUID] = None
    bandwidth: Optional[int] = None
    admin_state: Optional[str] = None


class BackboneLinkMemberBlockProvisioning(
    BackboneLinkMemberBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    """Backbone Link Member with fields for use in the provisioning lifecycle"""

    port_pair: PortPair[BackboneLinkInterfaceBlockProvisioning]
    esdb_circuit_id: Optional[str] = None
    nso_service_id: Optional[UUID] = None
    bandwidth: Optional[int] = None
    admin_state: Optional[str] = None


class BackboneLinkMemberBlock(BackboneLinkMemberBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """Backbone Link Member with fields for use in the active lifecycle"""

    port_pair: PortPair[BackboneLinkInterfaceBlock]
    esdb_circuit_id: str
    nso_service_id: UUID
    bandwidth: int
    admin_state: str


# Backbone Link Block


class BackboneLinkBlockInactive(ProductBlockModel, product_block_name="Backbone Link Block"):
    """Object model for a Backbone Link Block as used by
    Backbone Link Service"""

    members: ListOfMembers[BackboneLinkMemberBlockInactive]
    latency: Optional[int] = None
    preference: Optional[str] = None
    node_a_subscription_id: Optional[str] = None
    node_z_subscription_id: Optional[str] = None


class BackboneLinkBlockProvisioning(BackboneLinkBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    """Backbone Link Block with fields for use in the provisioning lifecycle"""

    members: ListOfMembers[BackboneLinkMemberBlockProvisioning]
    latency: int
    preference: str
    node_a_subscription_id: str
    node_z_subscription_id: str


class BackboneLinkBlock(BackboneLinkBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """Backbone Link Block with fields for use in the active lifecycle"""

    members: ListOfMembers[BackboneLinkMemberBlock]
    latency: int
    preference: str
    node_a_subscription_id: str
    node_z_subscription_id: str
