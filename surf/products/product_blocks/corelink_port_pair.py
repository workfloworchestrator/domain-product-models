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
from orchestrator.domain.base import ProductBlockModel, serializable_property
from orchestrator.types import SubscriptionLifecycle


class Sn8CorelinkPortPairBlockInactive(ProductBlockModel, product_block_name="Corelink Port Pair"):
    ims_port_id_1: int | None = None
    ims_port_id_2: int | None = None
    ims_corelink_trunk_id: int | None = None

    @serializable_property
    def title(self) -> str:
        return f"{self.name}"


class Sn8CorelinkPortPairBlockProvisioning(
    Sn8CorelinkPortPairBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    ims_port_id_1: int
    ims_port_id_2: int
    ims_corelink_trunk_id: int | None = None


class Sn8CorelinkPortPairBlock(Sn8CorelinkPortPairBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    ims_port_id_1: int
    ims_port_id_2: int
    ims_corelink_trunk_id: int
