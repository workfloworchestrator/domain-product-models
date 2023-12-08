from typing import Optional

from orchestrator.domain.base import ProductBlockModel
from orchestrator.types import SubscriptionLifecycle


class CircuitTransitionBlockInactive(ProductBlockModel, product_block_name="Circuit Transition"):
    """Object model for a Circuit Transition as used by Circuit Transition Service"""

    # when first created we expect the interface and nso service id to be none
    esnet5_circuit_id: Optional[str] = None
    esnet6_circuit_id: Optional[str] = None
    snow_ticket_assignee: Optional[str] = None
    snow_ticket_number: Optional[str] = None


class CircuitTransitionBlockProvisioning(
    CircuitTransitionBlockInactive, lifecycle=[SubscriptionLifecycle.PROVISIONING]
):
    """Circuit Transition with optional fields to use in the provisioning lifecycle state."""

    # We expect the ESDB interface to be set during provisioning state, but the NSO service may
    # not be set yet
    esnet5_circuit_id: str
    esnet6_circuit_id: str
    snow_ticket_assignee: str
    snow_ticket_number: Optional[str] = None


class CircuitTransitionBlock(CircuitTransitionBlockProvisioning, lifecycle=[SubscriptionLifecycle.ACTIVE]):
    """Circuit Transition with optional fields to use in the active lifecycle state."""

    # In the active state, there will be an NSO service, as well as an ESDB interface assigned
    esnet5_circuit_id: str
    esnet6_circuit_id: str
    snow_ticket_assignee: str
    snow_ticket_number: str
