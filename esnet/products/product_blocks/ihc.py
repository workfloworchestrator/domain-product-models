from typing import List, Optional, TypeVar, Union
from uuid import UUID

import structlog
from orchestrator.domain.base import ProductBlockModel, SubscriptionInstanceList
from orchestrator.types import SubscriptionLifecycle
from pydantic import Field

from esnetorch.config.nso import NSOMirrorCollectEnum
from esnetorch.products.product_blocks.pcs import (
    EquipmentInterfaceBlock,
    EquipmentInterfaceBlockInactive,
    EquipmentInterfaceBlockProvisioning,
    LagMember,
)
from esnetorch.products.product_blocks.service_edge import EdgeBlock, EdgeBlockInactive, EdgeBlockProvisioning
from esnetorch.services.subscriptions import (
    retrieve_subscription_list_by_filters,
    retrieve_subscriptions_by_type_and_instance_values,
)

T = TypeVar("T", covariant=True)

logger = structlog.get_logger(__name__)


# If this is set to min_items = 1, the list will initialize populated
# with 1 empty EdgeBlockInactive
class ConnectionList(SubscriptionInstanceList[T]):
    min_items = 0
    max_items = 16


class MirrorBlock(
    ProductBlockModel,
    product_block_name="Mirror Block",
    lifecycle=[SubscriptionLifecycle.INITIAL, SubscriptionLifecycle.PROVISIONING, SubscriptionLifecycle.ACTIVE],
):
    vlan: int
    collect: NSOMirrorCollectEnum
    port_name: Optional[str] = None
    mirror_sources_subscription_id: List[UUID]  # Reference(s) to PCS || ServiceEdge subscription instances

    @classmethod
    def from_esdb(cls, esdb_mirror: dict, owner_subscription_id: UUID) -> "MirrorBlock":
        esdb_equip_iface_id = esdb_mirror["source_port"]["id"]
        # Look for a PCS subscription associated with the mirror source
        associated_sub = retrieve_subscription_list_by_filters(
            {"equipment_interface_id": esdb_equip_iface_id}, product_type_in=("PhysicalConnection",)
        )
        if not associated_sub:
            logger.warning(
                f"No PCS subscription found containing an equipment interface with ESDB ID {esdb_equip_iface_id}."
                " Attempting to find an associated EquipmentInterfaceBlock..."
            )
        # if there isn't an associated PCS, this may be an _internal_ host whose port is a mirror source,
        # so check for an EquipmentInterfaceBlock
        associated_sub = retrieve_subscriptions_by_type_and_instance_values(
            "equipment_interface_id", str(esdb_equip_iface_id)
        )
        assert (
            associated_sub is not None
        ), f"No PCS subscription or EquipmentInterfaceBlock found containing an equipment interface with ESDB ID {esdb_equip_iface_id}"
        dest_vlan = esdb_mirror["destination_vlan"]["vlan_id"]
        collect = esdb_mirror["mirror_type"].lower()
        port_name = esdb_mirror.get("source_port", {}).get("interface")
        # TODO: in future, multiple service edges may be able to defined as mirror sources?
        # For now only a single equipment interface can be defined, which is a limitation of Nokia devices
        mirror_sources = [associated_sub.subscription_id]

        return cls.new(
            owner_subscription_id,
            vlan=dest_vlan,
            collect=collect,
            mirror_sources_subscription_id=mirror_sources,
            port_name=port_name,
        )


"""
Connection Block

This model represents a service edge that will never contain a PCS subscription/PhysicalConnection in ESDB
"""


class ConnectionBlockInactive(ProductBlockModel, product_block_name="Connection Block"):
    edge: EdgeBlockInactive
    equipment_interface: EquipmentInterfaceBlockInactive
    mirrored_sources: List[MirrorBlock] = Field(default_factory=list)


class ConnectionBlockProvisioning(ConnectionBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    edge: EdgeBlockProvisioning
    equipment_interface: EquipmentInterfaceBlockProvisioning
    mirrored_sources: List[MirrorBlock] = Field(default_factory=list)


class ConnectionBlock(ConnectionBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    edge: EdgeBlock
    equipment_interface: EquipmentInterfaceBlock
    mirrored_sources: List[MirrorBlock] = Field(default_factory=list)


"""
Internal Host Connectivity Model

Defined here: https://docs.google.com/document/d/1kywxfnIA2nUezOnAY1I14uaJtjdhGCqAk6uRl9I4DDE/edit#bookmark=id.phnk0if73bij

This model represents connections from the network to an ESnet host, each defined in a specific way as product types
"""


class InternalHostConnectivityBlockInactive(ProductBlockModel, product_block_name="Internal Host Connectivity Block"):
    connections: ConnectionList[ConnectionBlockInactive]
    esdb_host_connectivity_id: Optional[int] = None
    host_type: Optional[str] = None
    ipmi_interface: Optional[EquipmentInterfaceBlockInactive] = None
    mgmt_interface: Optional[EquipmentInterfaceBlockInactive] = None
    route_table: Optional[str] = None

    def get_equip_iface(self, **kwargs) -> Optional[Union[EquipmentInterfaceBlockInactive, LagMember]]:
        """Get any child EquipmentInterfaceBlock from an InternalHostConnectivityBlock using attribute=value

        Example:
        ```python
        subscription = InternalHostConnectivity.from_subscription(subscription_id)
        ihc_block = subscription.internal_host_connectivity_block
        equipment_interface_block = ihc_block.get_equip_iface(equipment_interface_id=esdb_interface["id])
        ```

        Returns:
            Optional[Union[EquipmentInterfaceBlockInactive, LagMember]]: EquipmentInterfaceBlock or LagMember
        """
        k, v = list(kwargs.items())[0]
        for attr in [self.ipmi_interface, self.mgmt_interface]:
            if attr is not None:
                if getattr(attr, k) == v:
                    return attr
                member = attr.get_lag_member(**{k: v})
                if member is not None:
                    return member
        for connection in self.connections:
            if getattr(connection.equipment_interface, k) == v:
                return connection.equipment_interface
            conn_member = connection.equipment_interface.get_lag_member(**{k: v})
            if conn_member is not None:
                return conn_member
        return None


class InternalHostConnectivityBlockProvisioning(
    InternalHostConnectivityBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    connections: ConnectionList[ConnectionBlockProvisioning]
    esdb_host_connectivity_id: int
    host_type: Optional[str] = None
    ipmi_interface: Optional[EquipmentInterfaceBlockProvisioning] = None
    mgmt_interface: Optional[EquipmentInterfaceBlockProvisioning] = None
    # This will ensure that newly created IHC subs have defined
    # the route_table attribute.
    route_table: str


class InternalHostConnectivityBlock(
    InternalHostConnectivityBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]
):
    connections: ConnectionList[ConnectionBlock]
    esdb_host_connectivity_id: int
    host_type: str
    ipmi_interface: Optional[EquipmentInterfaceBlock] = None
    mgmt_interface: Optional[EquipmentInterfaceBlock] = None
    # This is a temporary but necessary evil. This needs to be
    # optional during the migration process or it will cause
    # hard breakage to the existing subs and also the updater.
    route_table: Optional[str] = None
