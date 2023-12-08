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

from typing import Optional
from uuid import UUID

from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SubscriptionLifecycle

from esnetorch.products.product_blocks.pcs import (
    EquipmentInterfaceBlock,
    EquipmentInterfaceBlockInactive,
    EquipmentInterfaceBlockProvisioning,
)


class BridgeServiceBlockInactive(ProductBlockModel, product_block_name="Bridge Service Block"):
    vlan: Optional[int] = None
    device: Optional[str] = None
    description: Optional[str] = None
    # device and etc can be deduced from this
    switch_uplink_id: Optional[int] = None
    pcs_iface: Optional[EquipmentInterfaceBlockInactive] = None
    trunk_iface: Optional[EquipmentInterfaceBlockInactive] = None


class BridgeServiceBlockProvisioning(BridgeServiceBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    vlan: int
    device: str
    description: str
    switch_uplink_id: int
    pcs_iface: EquipmentInterfaceBlockProvisioning
    trunk_iface: EquipmentInterfaceBlockProvisioning


class BridgeServiceBlock(BridgeServiceBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    vlan: int
    device: str
    description: str
    switch_uplink_id: int
    pcs_iface: EquipmentInterfaceBlock
    trunk_iface: EquipmentInterfaceBlock


class EdgeBlockInactive(ProductBlockModel, product_block_name="Edge"):
    esdb_service_edge_id: Optional[int] = None
    route_table: Optional[str] = None
    admin_state: Optional[str] = None
    physical_connection_subscription_id: Optional[UUID] = None
    bridge_service: Optional[BridgeServiceBlockInactive] = None


class EdgeBlockProvisioning(EdgeBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]):
    esdb_service_edge_id: int
    route_table: str
    admin_state: str
    physical_connection_subscription_id: Optional[UUID] = None
    bridge_service: Optional[BridgeServiceBlockProvisioning] = None


class EdgeBlock(EdgeBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    esdb_service_edge_id: int
    route_table: str
    admin_state: str
    physical_connection_subscription_id: Optional[UUID] = None
    bridge_service: Optional[BridgeServiceBlock] = None
