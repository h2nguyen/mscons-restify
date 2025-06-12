"""
Context for parsing MSCONS messages.

This module provides the context object used during the parsing of MSCONS messages.
It maintains the state of the current interchange, message, and segment groups
being processed, allowing the parser to build the message structure incrementally.
"""
from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments.message_structure import (
    EdifactInterchange, EdifactMSconsMessage
)
from msconsparser.libs.edifactmsconsparser.wrappers.segments.segment_group import (
    SegmentGroup1, SegmentGroup2, SegmentGroup4, SegmentGroup5,
    SegmentGroup6, SegmentGroup7, SegmentGroup8, SegmentGroup9, SegmentGroup10
)


class ParsingContext:
    """
    The context that yields all relevant intermittent states during the parsing process.

    This class maintains references to the current interchange, message, and segment groups
    being processed during the parsing of an MSCONS message. It allows the parser to
    build the message structure incrementally as segments are encountered in the input.

    According to the MSCONS D.04B 2.4c standard, messages have a hierarchical structure
    with segment groups that can be nested. This context helps track the current position
    in this hierarchy during parsing.
    """

    def __init__(self):
        """
        Initialize a new parsing context.

        Creates an empty interchange and initializes all current segment group references to None.
        Also initializes the segment counter to 0.
        """
        self.interchange = EdifactInterchange()
        self.current_message: Optional[EdifactMSconsMessage] = None
        self.current_sg1: Optional[SegmentGroup1] = None
        self.current_sg2: Optional[SegmentGroup2] = None
        self.current_sg4: Optional[SegmentGroup4] = None
        self.current_sg5: Optional[SegmentGroup5] = None
        self.current_sg6: Optional[SegmentGroup6] = None
        self.current_sg7: Optional[SegmentGroup7] = None
        self.current_sg8: Optional[SegmentGroup8] = None
        self.current_sg9: Optional[SegmentGroup9] = None
        self.current_sg10: Optional[SegmentGroup10] = None
        self.segment_count = 0  # Segment counter for each message

    def reset_for_new_message(self):
        """
        Reset the context for a new message.

        This method is called when a new message is started (typically when a UNH segment
        is encountered). It resets all current segment group references to None and
        initializes the segment counter to 1 (counting the UNH segment).

        According to the MSCONS D.04B 2.4c standard, each message starts with a UNH segment
        and has its own hierarchy of segment groups, so the context needs to be reset
        for each new message.
        """
        self.segment_count = 1  # Reset the segment counter (counting the UNH segment)
        self.current_message: Optional[EdifactMSconsMessage] = None
        self.current_sg1: Optional[SegmentGroup1] = None
        self.current_sg2: Optional[SegmentGroup2] = None
        self.current_sg4: Optional[SegmentGroup4] = None
        self.current_sg5: Optional[SegmentGroup5] = None
        self.current_sg6: Optional[SegmentGroup6] = None
        self.current_sg7: Optional[SegmentGroup7] = None
        self.current_sg8: Optional[SegmentGroup8] = None
        self.current_sg9: Optional[SegmentGroup9] = None
        self.current_sg10: Optional[SegmentGroup10] = None
