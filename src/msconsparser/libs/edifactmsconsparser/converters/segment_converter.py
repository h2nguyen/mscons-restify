# coding: utf-8

import logging
from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic

from msconsparser.libs.edifactmsconsparser.exceptions import CONTRLException
from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup

logger = logging.getLogger(__name__)

T = TypeVar('T')


class SegmentConverter(ABC, Generic[T]):
    """
    Abstract base class for all segment converters in the MSCONS parser.

    This class defines the interface for converting EDI segment components into 
    typed domain model objects. It handles exception management and provides a 
    consistent conversion pattern for all segment types.

    The generic type parameter T represents the specific segment model type that 
    a concrete converter implementation will return.

    Attributes:
        None
    """

    def convert(
            self,
            line_number: int,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup]
    ) -> T:
        """
        Converts segment components to a typed domain model object.

        This method wraps the internal conversion logic with exception handling.
        If an exception occurs during conversion, it's caught, logged, and wrapped
        in a CONTRLException with detailed error information.

        Args:
            line_number: The line number in the EDI file where this segment appears
            element_components: List of segment components extracted from the EDI file
            last_segment_type: The type of the previous segment (e.g., 'UNH', 'BGM')
            current_segment_group: The current segment group being processed

        Returns:
            A typed domain model object of type T

        Raises:
            CONTRLException: If any error occurs during the conversion process
        """
        try:
            return self._convert_internal(element_components, last_segment_type, current_segment_group)
        except Exception as ex:
            # Service-Meldungen: CONTRL – Syntax-Prüfung und Rückmeldung über Ankunft der Meldung (Syntax- und Servicereport-Meldungen für
            error_message = f"CONTRL -> l{line_number} -> {element_components} -> {ex}"
            logger.error(error_message)
            raise CONTRLException(message=error_message)


    @abstractmethod
    def _convert_internal(
            self,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup]
    ) -> T:
        """
        Internal method to convert segment components to a typed domain model object.

        This abstract method must be implemented by all concrete converter classes.
        It contains the specific logic for converting a particular segment type.

        Args:
            element_components: List of segment components extracted from the EDIFACT file
            last_segment_type: The type of the previous segment (e.g., 'UNH', 'BGM')
            current_segment_group: The current segment group being processed

        Returns:
            A typed domain model object of type T
        """
        pass

    def _get_identifier_name(
            self,
            qualifier_code: Optional[str],
            current_segment_group: Optional[SegmentGroup]
    ) -> Optional[str]:
        """
        Helper method to get a human-readable identifier name based on qualifier code.

        This method can be overridden by subclasses to provide specific mappings
        from qualifier codes to human-readable names, often depending on the
        current segment group context.

        Args:
            qualifier_code: The qualifier code from the segment
            current_segment_group: The current segment group being processed

        Returns:
            A human-readable identifier name, or None if no mapping exists
        """
        pass
