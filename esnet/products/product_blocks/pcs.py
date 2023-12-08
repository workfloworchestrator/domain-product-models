from typing import Any, Dict, List, Optional, TypeVar, Union
from uuid import UUID

from orchestrator.domain.base import ProductBlockModel, SubscriptionInstanceList
from orchestrator.types import SubscriptionLifecycle
from pydantic import Field

from esnetorch.config.esdb import ESDBCircuitStateStr, ESDBInterfaceAdminState, ESDBInterfaceEthEncap
from esnetorch.config.nso import NSOPortStates

# In here, we define the values expected for a product block at each phase of the of the Subscription Lifecycle
# All resource types used by a product block need to be explicitly called out here and assigned
# expected types

T = TypeVar("T", covariant=True)


class CircuitBlock(ProductBlockModel, product_block_name="Circuit Block"):
    id: int
    state: ESDBCircuitStateStr


class ListOfMembers(SubscriptionInstanceList[T]):
    min_items = 0


class LagMember(
    ProductBlockModel,
    product_block_name="Lag Member Block",
    lifecycle=[SubscriptionLifecycle.INITIAL, SubscriptionLifecycle.PROVISIONING, SubscriptionLifecycle.ACTIVE],
):
    """Object model representing a member port of a LAG interface used by EquipmentInterfaceBlock"""

    equipment_interface_id: int
    port_name: str
    admin_state: NSOPortStates

    @classmethod
    def from_esdb_ifce(
        cls,
        owner_subscription_id: UUID,
        esdb_equip_iface: Dict[str, Any],
        admin_state: Optional[NSOPortStates] = NSOPortStates.UP,
    ) -> "LagMember":
        """Create and return a new instance of a LagMember block class for use in other serialization models
        from an esdb equipment_interface.

        Args:
            owner_subscription_id (UUID): UUID of top-level subscription
            esdb_equip_iface (Dict[str, Any]): Dictionary object retrieved from ESDB
            admin_state (NSOPortStates, optional): Admin-state to set on new LagMember object. Defaults to `NSOPortStates.UP`.

        Returns:
            LagMember: newly instantiated LagMember product block domain model instance
        """
        return cls.new(
            owner_subscription_id,
            port_name=esdb_equip_iface["interface"],
            equipment_interface_id=esdb_equip_iface["id"],
            admin_state=admin_state,
        )

    class Config:
        use_enum_values = True


class EquipmentInterfaceBlockInactive(ProductBlockModel, product_block_name="Equipment Interface Block"):
    """Object model for a Equipment Interface as used by various other products and blocks."""

    equipment_interface_id: Optional[int] = None
    admin_state: Optional[str] = None
    node_subscription_id: Optional[UUID] = None
    speed: Optional[str] = None
    eth_encap: Optional[str] = None
    lag_members: List[LagMember] = Field(default_factory=list)
    members: Optional[ListOfMembers[int]] = None
    circuit: Optional[CircuitBlock] = None
    enable_fec: Optional[bool] = None

    def get_lag_member(self, /, **kwargs) -> Optional[LagMember]:
        """Get a child LagMemberBlock object using attribute=value keyword arguments
        (more than one kwarg operates as logical OR)

        Example:
        ```python
        subscription: ProductType = ProductType.from_subscription(subscription_id)
        lag_member = subscription.equipment_interface_block.get_lag_member(port_name="1/1/c1")
        ```

        Returns:
            Optional[LagMember]: LagMember block if found, else None
        """
        for key, value in kwargs.items():
            for member in self.lag_members:
                if getattr(member, key) == value:
                    return member
        return None

    @classmethod
    def from_esdb_iface(
        cls,
        esdb_iface: Dict[str, Any],
        subscription_id: UUID,
        related_node_sub_id: UUID,
        enable_fec: bool = False,
        admin_states: Dict[int, Any] = {},
    ) -> Union["EquipmentInterfaceBlockInactive", "EquipmentInterfaceBlockProvisioning", "EquipmentInterfaceBlock"]:
        members = [
            LagMember.from_esdb_ifce(subscription_id, ifce, admin_state=admin_states.get(ifce["id"], NSOPortStates.UP))
            for ifce in esdb_iface.get("grouped_interfaces", [])
        ]
        return EquipmentInterfaceBlock.new(
            equipment_interface_id=esdb_iface["id"],
            admin_state=admin_states.get(esdb_iface["id"], ESDBInterfaceAdminState.UP),
            node_subscription_id=related_node_sub_id,
            speed=esdb_iface["interface_bandwidth"]["name"],
            subscription_id=subscription_id,
            eth_encap=ESDBInterfaceEthEncap.DOT1Q if esdb_iface.get("tagged") else ESDBInterfaceEthEncap.ACCESS,
            lag_members=members,
            enable_fec=enable_fec,
        )


class EquipmentInterfaceBlockProvisioning(
    EquipmentInterfaceBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    """Object model for a Equipment Interface in the Provisioning state as used by various other products and blocks."""

    equipment_interface_id: int
    admin_state: str
    node_subscription_id: UUID
    speed: Optional[str] = None
    eth_encap: Optional[str] = None
    lag_members: List[LagMember] = Field(default_factory=list)
    members: Optional[ListOfMembers[int]] = None
    circuit: Optional[CircuitBlock] = None
    enable_fec: Optional[bool] = None


class EquipmentInterfaceBlock(EquipmentInterfaceBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """Object model for a Equipment Interface in the Active state as used by various other products and blocks."""

    equipment_interface_id: int
    admin_state: str
    node_subscription_id: UUID
    speed: str
    eth_encap: str
    lag_members: List[LagMember] = Field(default_factory=list)
    members: Optional[ListOfMembers[int]] = None
    circuit: Optional[CircuitBlock] = None
    enable_fec: Optional[bool] = None


class PhysicalConnectionBlockInactive(ProductBlockModel, product_block_name="Physical Connection Block"):
    """Object model for a Physical Connection as used by Physical Connectivity Service"""

    # when first created we expect the interface and nso service id to be none
    physical_connection_id: Optional[int] = None
    conn_id: Optional[str] = None
    capacity: Optional[int] = None
    equipment_interface: Optional[EquipmentInterfaceBlockInactive] = None
    lag: Optional[bool] = None


class PhysicalConnectionBlockProvisioning(
    PhysicalConnectionBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    """Physical Connection with optional fields to use in the provisioning lifecycle state."""

    # We expect the ESDB interface to be set during provisioning state, but the NSO service may
    # not be set yet
    physical_connection_id: int
    conn_id: str
    capacity: int
    equipment_interface: EquipmentInterfaceBlockProvisioning
    lag: Optional[bool] = None


class PhysicalConnectionBlock(PhysicalConnectionBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """Physical Connection with optional fields to use in the active lifecycle state."""

    # In the active state, there will be an NSO service, as well as an ESDB interface assigned
    physical_connection_id: int
    conn_id: str
    capacity: int
    equipment_interface: EquipmentInterfaceBlock
    lag: bool
