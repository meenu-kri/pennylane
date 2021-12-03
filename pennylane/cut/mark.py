# Copyright 2021 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Functionality for marking manually-placed cut locations"""
from functools import wraps
from typing import Type

from pennylane.operation import Operation, AnyWires
from pennylane.tape import QuantumTape

GATE_CUTS_SUPPORTED = ["CZ"]


class wire(Operation):
    """pennylane.cut.wire(wires)
    Manually place a wire cut in a circuit.

    Marks the placement of a wire cut of the type introduced in
    `Peng et al. <https://arxiv.org/abs/1904.00102>`__. Behaves like an :class:`~.Identity`
    operation if cutting subsequent functionality is not applied to the whole circuit.

    Args:
        wires (Sequence[int] or int): the wires to be cut
    """
    num_wires = AnyWires
    grad_method = None

    def __init__(self, wires):
        super().__init__(wires=wires)

    def label(self, decimals=None, base_label=None):
        return "|️"

    def expand(self):
        with QuantumTape() as tape:
            ...
        return tape


class CutOperation(QuantumTape):
    ...


def gate(op: Type[Operation]):
    """pennylane.cut.gate(operation)
    Manually place a wire cut in a circuit.

    Marks the placement of a gate cut of the type introduced in
    `Mitarai et al. <https://arxiv.org/abs/1909.07534>`__.

    Args:
        op (Operation type): the operation to be cut
    """
    if op.__name__ not in GATE_CUTS_SUPPORTED:
        supported_gates = ", ".join(GATE_CUTS_SUPPORTED)
        err_msg = "Gate cutting can only be applied to the following gates: " + supported_gates
        raise ValueError(err_msg)

    @wraps(op)
    def wrapped_op(*args, **kwargs):
        """Replaces ``op`` with a ``CutOperation``, which is a special type of ``QuantumTape``."""
        with CutOperation():
            op(*args, **kwargs)

    return wrapped_op
