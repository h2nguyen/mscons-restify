# coding: utf-8

from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup, SegmentQTY
from msconsparser.libs.edifactmsconsparser.converters import SegmentConverter
from msconsparser.libs.edifactmsconsparser.utils import MSCONSUtils


class QTYSegmentConverter(SegmentConverter[SegmentQTY]):

    def __init__(self):
        pass

    def _convert_internal(
            self,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup]
    ) -> SegmentQTY:
        """
        Converts QTY (Quantities) segment components to a SegmentQTY object.

        The QTY segment is used to specify quantities for the current item position.

        Args:
            element_components: List of segment components
            last_segment_type: The type of the previous segment
            current_segment_group: The current segment group being processed

        Returns:
            SegmentQTY object with quantity qualifier, the quantity and unit measurement code

        Examples:
        QTY+220:4250.465:D54'
        QTY+67:4250.465' - Example of a quantity and status specification as a substitute value with 3 decimal places without a unit of measurement
        QTY+220:4.123:D54' - Example of a quantity and status specification as a true value with 3 decimal places and the unit of measurement watts per square meter
        QTY+79:-4.987:KWH' - Example of a quantity and status specification as a summed energy quantity (total value, balance sheet total) as a negative value with 3 decimal places and the unit of measurement kilowatt hours
        """
        details = MSCONSUtils.split_components(element_components[1])
        menge_qualifier = details[0]
        menge = details[1] if len(details) > 1 else None
        masseinheit_code = details[2] if len(details) > 2 else None

        return SegmentQTY(
            menge_qualifier=menge_qualifier,
            menge=float(menge),
            masseinheit_code=masseinheit_code
        )
