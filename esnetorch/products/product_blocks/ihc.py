# Copyright 2019-2023 surf.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Optional, TypeVar, Union
from uuid import UUID

import structlog
from orchestrator.domain.base import ProductBlockModel, SubscriptionInstanceList
from orchestrator.types import SubscriptionLifecycle, strEnum
from pydantic import Field

from esnetorch.products.product_blocks.pcs import (
    EquipmentInterfaceBlock,
    EquipmentInterfaceBlockInactive,
    EquipmentInterfaceBlockProvisioning,
    LagMember,
)
from esnetorch.products.product_blocks.service_edge import EdgeBlock, EdgeBlockInactive, EdgeBlockProvisioning


T = TypeVar("T", covariant=True)

logger = structlog.get_logger(__name__)

class NSOMirrorCollectEnum(strEnum):
    BOTH = "both"
    INGRESS = "ingress"
    EGRESS = "egress"

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
