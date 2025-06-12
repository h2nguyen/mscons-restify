# coding: utf-8

import logging
from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers import ParsingContext
from msconsparser.libs.edifactmsconsparser.exceptions import MSCONSParserException
from msconsparser.libs.edifactmsconsparser.wrappers.segments import SegmentType, SegmentGroup, EdifactInterchange
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandlerFactory
from msconsparser.libs.edifactmsconsparser.utils.edifact_syntax_helper import EdifactSyntaxHelper
from msconsparser.libs.edifactmsconsparser.wrappers.segments.constants import EdifactConstants

logger = logging.getLogger(__name__)


class EdifactMSCONSParser:
    """
    Parser for EDIFACT-MSCONS files according to the defined domain model.
    Uses dictionary-based handlers for the segment types.
    """

    def __init__(self, handler_factory: Optional[SegmentHandlerFactory] = None) -> None:
        self.__context = ParsingContext()
        self.__syntax_parser = EdifactSyntaxHelper()
        self.__handler_factory = handler_factory or SegmentHandlerFactory(self.__syntax_parser)

    def parse(self, edifact_text: str, max_lines_to_parse: int = -1) -> EdifactInterchange:
        """
        Main method: Reads the EDIFACT string, splits it at the segment separators,
        and calls the appropriate handler for each segment.

        Args:
            edifact_text (str): The EDIFACT text to parse
            max_lines_to_parse (int): The maximum number of lines to parse, defaults to -1 has not parsing limit

        Returns:
            EdifactInterchange: The parsed interchange object
        """
        if edifact_text is None:
            raise MSCONSParserException("No valid parsing input. Input was", str(edifact_text))

        edifact_text = self.__extract_and_process_una_segment(edifact_text)

        segments = self.__syntax_parser.split_segments(edifact_text, self.__context)
        amount_of_segments = len(segments)

        if (0 < max_lines_to_parse) and (max_lines_to_parse < amount_of_segments):
            raise MSCONSParserException(f"Maximum number of segments reached (max: {max_lines_to_parse} less than number of segments: {amount_of_segments})")

        last_segment_type: Optional[str] = None
        current_segment_group: Optional[str] = None
        line_number: int = 0
        for segment in segments:
            line_number = line_number + 1
            segment_line = segment.strip()
            if not segment_line:
                continue
            element_components = self.__syntax_parser.split_elements(
                string_content=segment_line,
                context=self.__context
            )
            if not element_components:
                continue
            segment_type_components = self.__syntax_parser.split_components(
                string_content=element_components[0],
                context=self.__context
            )
            if not segment_type_components:
                continue
            segment_type = segment_type_components[0]
            current_segment_group = self.get_segment_group(
                current_segment_type=segment_type,
                current_segment_group=current_segment_group
            )
            self.__context.segment_count += 1

            segment_handler = self.__handler_factory.get_handler(segment_type)
            if segment_handler:
                # Use the dedicated handler
                segment_handler.handle(
                    line_number=line_number,
                    element_components=element_components,
                    last_segment_type=last_segment_type,
                    current_segment_group=current_segment_group,
                    context=self.__context
                )
            last_segment_type = segment_type

        return self.__context.interchange

    def __extract_and_process_una_segment(self, edifact_text):
        # Check for UNA segment at the beginning of the file
        if edifact_text.startswith(SegmentType.UNA):
            # Extract the UNA segment (always 9 characters long)
            una_segment = edifact_text[:EdifactConstants.UNA_SEGMENT_MAX_LENGTH]

            # Process the UNA segment to set the delimiters
            una_handler = self.__handler_factory.get_handler(SegmentType.UNA)
            if una_handler:
                una_handler.handle(
                    line_number=1,
                    element_components=[una_segment],
                    last_segment_type=None,
                    current_segment_group=None,
                    context=self.__context
                )

            # Remove the UNA segment from the text to avoid processing it again
            # IMPROVEMENT note:
            # Should we do this or just leave the UNA segment in the text to save processing time?
            # Since the text can be very long, it might be better to leave it in the text to save processing time.
            edifact_text = edifact_text[EdifactConstants.UNA_SEGMENT_MAX_LENGTH:]
        return edifact_text

    @staticmethod
    def get_segment_group(
            current_segment_type: str,
            current_segment_group: Optional[SegmentGroup],
    ) -> Optional[SegmentGroup]:
        """
        Determines the segment group based on the current segment type and the current segment group.

        Args:
            current_segment_type (str): The type of the current segment
            current_segment_group (Optional[SegmentGroup]): The current segment group

        Returns:
            Optional[SegmentGroup]: The determined segment group, or None if the segment type is empty
        """
        if not current_segment_type:
            logger.error(f"Error: Segment type '{current_segment_type}' not exist!")
            return None

        if current_segment_type.startswith(SegmentType.DTM):
            return current_segment_group

        if current_segment_type.startswith(SegmentType.RFF):
            if current_segment_group is None:
                return SegmentGroup.SG1
            if current_segment_group == SegmentGroup.SG1:
                return SegmentGroup.SG1
            if current_segment_group == SegmentGroup.SG6:
                return SegmentGroup.SG7
            if current_segment_group == SegmentGroup.SG7:
                return SegmentGroup.SG7

        if current_segment_type.startswith(SegmentType.NAD):
            if current_segment_group == SegmentGroup.SG1:
                return SegmentGroup.SG2
            if current_segment_group == SegmentGroup.SG4:
                return SegmentGroup.SG2
            if current_segment_group is None:
                return SegmentGroup.SG5

        if current_segment_type.startswith(SegmentType.CTA):
            return SegmentGroup.SG4
        if current_segment_type.startswith(SegmentType.COM):
            return SegmentGroup.SG4

        if current_segment_type.startswith(SegmentType.LOC):
            return SegmentGroup.SG6

        if current_segment_type.startswith(SegmentType.CCI):
            return SegmentGroup.SG8

        if current_segment_type.startswith(SegmentType.LIN):
            return SegmentGroup.SG9
        if current_segment_type.startswith(SegmentType.PIA):
            return SegmentGroup.SG9

        if current_segment_type.startswith(SegmentType.QTY):
            return SegmentGroup.SG10

        if current_segment_type.startswith(SegmentType.STS):
            return SegmentGroup.SG10

        return None
