# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from decimal import Decimal as PyDecimal, ROUND_HALF_UP
from typing import Union
from .types import Types


class Decimal:
    def __init__(
        self, value: Union[str, PyDecimal], precision: int = None, scale: int = None
    ):
        if isinstance(value, str):
            value = PyDecimal(value)

        # If precision and scale are not provided, calculate them based on the value
        if precision is None:
            precision = len(value.as_tuple().digits)
        if scale is None:
            scale = -value.as_tuple().exponent

        # Validate precision and scale using DecimalType's rules
        Types.DecimalType.check_precision_scale(precision, scale)

        if precision < value.adjusted() + 1:
            raise ValueError(
                f"Precision of value cannot be greater than precision of decimal: {value.adjusted() + 1} > {precision}"
            )

        # Set scale with rounding
        self._value = value.quantize(
            PyDecimal((0, (1,), -scale)), rounding=ROUND_HALF_UP
        )
        self._precision = precision
        self._scale = scale

    @classmethod
    def of(cls, value: Union[str, PyDecimal], precision: int = None, scale: int = None):
        return cls(value, precision, scale)

    @property
    def value(self) -> PyDecimal:
        return self._value

    @property
    def precision(self) -> int:
        return self._precision

    @property
    def scale(self) -> int:
        return self._scale

    def __str__(self) -> str:
        return str(self._value)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Decimal):
            return False
        return self._scale == other._scale and self._value == other._value

    def __hash__(self) -> int:
        return hash((self._value, self._precision, self._scale))
