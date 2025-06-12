# coding: utf-8

from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic

from msconsparser.libs.edifactmsconsparser.converters import SegmentConverter
from msconsparser.libs.edifactmsconsparser.wrappers import ParsingContext
from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentGroup

T = TypeVar('T')


class SegmentHandler(ABC, Generic[T]):
    """
    Abstract base class for segment handlers.
    Each segment type should have its own handler implementation.
    """

    def __init__(self, converter: SegmentConverter[T]):
        """
        Initialize the handler with a converter for the specific segment type.

        Args:
            converter: The converter to use for converting the segment data.
        """
        self.converter = converter

    def handle(
            self,
            line_number: int,
            element_components: list[str],
            last_segment_type: Optional[str],
            current_segment_group: Optional[SegmentGroup],
            context: ParsingContext
    ) -> None:
        """
        Handle a segment by converting it and updating the context.

        Args:
            line_number: The line number of the segment in the input file.
            element_components: The components of the segment.
            last_segment_type: The type of the previous segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        # Check if the context is valid for this handler
        if not self._can_handle(context):
            return

        # Convert the segment
        segment = self.converter.convert(
            line_number=line_number,
            element_components=element_components,
            last_segment_type=last_segment_type,
            current_segment_group=current_segment_group,
            context=context
        )

        # Update the context with the converted segment
        self._update_context(segment, current_segment_group, context)

    def _can_handle(self, context: ParsingContext) -> bool:
        """
        Check if the context is valid for this handler.

        Args:
            context: The parsing context to check.

        Returns:
            True if the context is valid, False otherwise.
        """
        # Default behavior for handling when the current context message exists.
        return context.current_message is not None

    @abstractmethod
    def _update_context(self, segment: T, current_segment_group: Optional[SegmentGroup],
                        context: ParsingContext) -> None:
        """
        Update the context with the converted segment.

        Args:
            segment: The converted segment.
            current_segment_group: The current segment group.
            context: The parsing context to update.
        """
        pass
