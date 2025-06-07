# MSCONS Parsing Process Documentation

## Overview

This document describes the business logic for parsing EDIFACT MSCONS (Metered Services Consumption Report)
messages in the mscons-restify application. The parsing process transforms raw EDIFACT text into structured context
(domain) objects using a system of converters and handlers for each segment type.

## Architecture

The mscons-restify application follows a hexagonal architecture with clear separation of concerns:

1. **Application Layer**: Contains services and use cases
   - **ParserService**: Orchestrates the parsing process using the ParseMessageUseCase
   - **ParseMessageUseCase**: Implements the MessageParserPort interface and uses the EdifactMSCONSParser

2. **Domain Layer**: Contains ports (interfaces) and domain models
   - **MessageParserPort**: Interface that defines the contract for parsing messages

3. **Library Layer**: Contains the actual parsing logic in the libs/edifactmsconsparser package
   - **Parser**: The main entry point that orchestrates the parsing process
   - **Handlers**: Process specific segment types and update the parsing context
   - **Converters**: Transform raw segment data into structured context objects
   - **Wrappers**: Define the structure of the parsed data (context models)
   - **Context**: Maintains state during the parsing process

### Flow of the Parsing Process

1. The raw EDIFACT text is passed to the `EdifactMSCONSParser.parse()` method
2. The parser splits the text into segments using `MSCONSUtils.split_segments()`
3. For each segment:
   - The segment type is determined from the first element
   - The segment group is determined based on the segment type and current context
   - A handler for the segment type is retrieved from the `SegmentHandlerFactory`
   - The handler uses its converter to transform the segment data into a context object
   - The handler updates the parsing context with the converted segment
4. The parser returns the completed `EdifactInterchange` object

## Segment Types

EDIFACT MSCONS messages consist of various segment types, each with a specific purpose:

- **UNA**: Service String Advice - Defines EDIFACT separators
- **UNB/UNZ**: Interchange Header/Trailer - Encloses the data exchange
- **UNH/UNT**: Message Header/Trailer - Encloses a MSCONS message
- **BGM**: Beginning of Message - Message type/reference
- **DTM**: Date/Time/Period - Date and time information
- **RFF**: Reference - References (e.g., process ID, device number)
- **NAD**: Name and Address - Partner identification or delivery location
- **CTA**: Contact Information - Contact person
- **COM**: Communication Contact - Communication details (phone, email)
- **LOC**: Place/Location Identification - Balance group or object
- **UNS**: Section Control - Separates header and detail sections
- **LIN**: Line Item - Sequential position within the position group
- **PIA**: Additional Product ID - Additional product/device ID
- **QTY**: Quantity - Quantity element (e.g., measured value)
- **CCI**: Composite Code Information - Time series type identification
- **STS**: Status - Status information (plausibility, replacement procedure, etc.)

## Segment Groups

MSCONS messages are organized into segment groups that represent logical sections:

- **SG1**: Contains references (RFF) and date/time information (DTM)
- **SG2**: Contains market partner information (NAD)
- **SG4**: Contains contact information (CTA, COM)
- **SG5**: Contains location information (NAD)
- **SG6**: Contains value and recording information for the object (LOC, DTM, SG7, SG8, SG9)
- **SG7**: Contains reference information (RFF)
- **SG8**: Contains time series type information (CCI)
- **SG9**: Contains position data (LIN, PIA, SG10)
- **SG10**: Contains quantity and status information (QTY, DTM, STS)

## Handlers

Each segment type has a dedicated handler that processes segments of that type. Handlers are responsible for:

1. Validating that the context is appropriate for handling the segment
2. Using a converter to transform the segment data into a context object
3. Updating the parsing context with the converted segment

Handlers are created and managed by the `SegmentHandlerFactory`, which maintains a mapping of segment types to handler instances.

### Example: BGM Segment Handler

The `BGMSegmentHandler` processes BGM (Beginning of Message) segments:

```python
from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import (
   SegmentGroup, ParsingContext, SegmentBGM
)
from msconsparser.libs.edifactmsconsparser.converters import BGMSegmentConverter
from msconsparser.libs.edifactmsconsparser.handlers import SegmentHandler


class BGMSegmentHandler(SegmentHandler[SegmentBGM]):
   def __init__(self):
      super().__init__(BGMSegmentConverter())

   def _update_context(self, segment: SegmentBGM, current_segment_group: Optional[SegmentGroup],
                       context: ParsingContext) -> None:
      context.current_message.bgm_beginn_der_nachricht = segment
```

## Converters

Converters transform raw segment data into structured context objects. Each segment type has a dedicated converter
that knows how to interpret the segment's components.

Converters implement the `SegmentConverter` abstract base class, which provides:

1. A public `convert()` method that handles exceptions and wraps the internal conversion logic
2. An abstract `_convert_internal()` method that must be implemented by concrete converters
3. A helper method `_get_identifier_name()` for mapping qualifier codes to human-readable names

### Example: BGM Segment Converter

The `BGMSegmentConverter` transforms BGM segment components into a `SegmentBGM` object:

```python
from typing import Optional

from msconsparser.libs.edifactmsconsparser.wrappers.segments import (
    SegmentGroup, SegmentBGM, DokumentenNachrichtenname, DokumentenNachrichtenIdentifikation
)
from msconsparser.libs.edifactmsconsparser.converters import SegmentConverter


class BGMSegmentConverter(SegmentConverter[SegmentBGM]):
   def _convert_internal(
           self,
           element_components: list[str],
           last_segment_type: Optional[str],
           current_segment_group: Optional[SegmentGroup]
   ) -> SegmentBGM:
      dokumentenname_code = element_components[1]
      dokumentennummer = element_components[2]
      nachrichtenfunktion_code = element_components[3] if len(element_components) > 3 else None

      return SegmentBGM(
         dokumenten_nachrichtenname=DokumentenNachrichtenname(
            dokumentenname_code=dokumentenname_code
         ),
         dokumenten_nachrichten_identifikation=DokumentenNachrichtenIdentifikation(
            dokumentennummer=dokumentennummer
         ),
         nachrichtenfunktion_code=nachrichtenfunktion_code
      )
```

## Parsing Context

The `ParsingContext` maintains state during the parsing process. It contains:

1. An `EdifactInterchange` object that represents the entire parsed interchange
2. References to the current message and various segment groups (SG1-SG10)
3. A segment counter (actually, each line from the message file represents a segment)
4. A method to reset the context for a new message

The context is updated by handlers as each segment is processed, gradually building up the complete parsed data structure.

## Context Models

The parsed data is structured according to context models defined in the `libs/edifactmsconsparser/wrappers/segments` directory:

1. `interchange.py`: Models for the interchange and basic segments
2. `message.py` and `message_structure.py`: Models for messages and message structures
3. `segment_group.py`: Models for segment groups
4. Other files like `location.py`, `measurement.py`, `partner.py`, `reference.py`: Models for specific MSCONS segments

These models define the structure of the parsed data and are populated by the segment handlers during the parsing process.

## Extending the Parser

To extend the parser to support new segment types or modify existing behavior:

1. Define a new segment type in `libs/edifactmsconsparser/wrappers/segments/constants.py` if needed
2. Create a context model for the segment in one of the files in `libs/edifactmsconsparser/wrappers/segments/` (e.g., message.py, interchange.py)
3. Export the new model in `libs/edifactmsconsparser/wrappers/segments/__init__.py`
4. Implement a converter for the segment that extends `SegmentConverter` in the `libs/edifactmsconsparser/converters` directory
5. Implement a handler for the segment that extends `SegmentHandler` in the `libs/edifactmsconsparser/handlers` directory
6. Register the handler in `SegmentHandlerFactory.__register_handlers()` in `libs/edifactmsconsparser/handlers/segment_handler_factory.py`
7. Update the `get_segment_group()` method in `EdifactMSCONSParser` in `libs/edifactmsconsparser/edifact_mscons_parser.py` if the segment affects segment group determination

## Conclusion

The MSCONS parsing process in this application follows a clean, modular design with clear separation of concerns.
The use of dedicated handlers and converters for each segment type makes the code maintainable and extensible,
allowing for easy addition of new segment types or modification of existing behavior.
