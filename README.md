# Development Guidelines for the Rest-API EDIFACT MSCONS Parser

This document provides guidelines and instructions for developing and maintaining the mscons-restify project.

## Build and Configuration Instructions

### OpenAPI generated FastAPI server components

This Python project uses [OpenAPI Generator](https://openapi-generator.tech) to generate the API endpoints (DTOs and
router endpoints) while the core business logic is manually created following a clean (hexagonal) architecture pattern:

- API version: 1.204c.1
- Generator version: 7.14.0-SNAPSHOT
- Build package: org.openapitools.codegen.languages.PythonFastAPIServerCodegen

> NOTE: Before starting the project, please generate the missing APIs first, see [generate-openapi-endpoints.md](docs/generate-openapi-endpoints.md)
> otherwise, the application will not be built properly!

### Local Development Setup

1. **Python Version**: This project requires Python 3.9 or higher.

2. **Virtual Environment Setup**:
   ```bash
   # Create a virtual environment named .venv
   python -m venv .venv

   # Activate the virtual environment
   # On Windows:
   #.venv\Scripts\activate
   
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Dependencies Installation**:
   > NOTE: Please execute the following from the root directory with the virtual environment activated!

   ```bash
   # Install uv if not already installed
   pip install uv

   # Install dependencies using uv
   uv pip install -e .

   # For development dependencies
   uv pip install -e ".[dev]"
   ```

   > NOTE: This project uses pyproject.toml for dependency management with the uv package manager.

3. **Running the Application**:

   You can run the application in several ways:

   **With uv**:
   ```bash
   # Install dependencies and start the application
   uv pip install -e .
   PYTHONPATH=src uv run -m uvicorn msconsparser.main:app --host 0.0.0.0 --port 8000
   ```

   **Without uv**:
   ```bash
   # Install dependencies and start the application
   pip install -e .
   PYTHONPATH=src python -m uvicorn msconsparser.main:app --host 0.0.0.0 --port 8000
   ```

   **Direct execution with uvicorn**:
   ```bash
   # After installing dependencies
   PYTHONPATH=src uvicorn msconsparser.main:app --host 0.0.0.0 --port 8000
   ```

   Or simply:
   ```bash
   uvicorn msconsparser.main:app --host 0.0.0.0 --port 8000
   ```

   After starting the application, open your browser at `http://0.0.0.0:8000/docs/` to see the API documentation.

### Docker Setup

To run the server on a Docker container, please execute the following from the root directory:

1. **Building the Docker Image**:
   ```bash
   docker build -t mscons-restify .
   ```

   The Dockerfile uses a multi-stage build process:
   - `builder` stage: Installs the application and dependencies
   - `test_runner` stage: Runs the tests
   - `service` stage: Creates the final image for deployment

2. **Running with Docker Compose**:
   ```bash
   docker compose up
   ```
   ```bash
   # or including the build
   docker compose up --build
   ```

   This will start the service on port 8000, which maps to the internal port 8000.

## Testing Information

### Running Tests

1. **Running All Tests**:
   ```bash
   python -m pytest
   ```

2. **Running Specific Tests**:
   ```bash
   python -m pytest tests/test_simple_parser.py
   ```

3. **Running Tests with Verbosity**:
   ```bash
   python -m pytest -v
   ```

### Adding New Tests

1. **Test Structure**:
   - Place test files in the `tests` directory
   - Use the naming convention `test_*.py` for test files
   - Use unittest or pytest style tests (the project uses both, unittest is preferred)

2. **Sample Test**:
   ```python
   import os
   import unittest

   from msconsparser.libs.edifactmsconsparser.edifact_mscons_parser import EdifactMSCONSParser

   class TestSimpleParser(unittest.TestCase):
       """A simple test case to demonstrate testing in this project."""

       def setUp(self):
           self.parser = EdifactMSCONSParser()

       def test_parse_sample_file(self):
           """Test that the parser can parse the sample file."""
           # Read the sample file
           mscons_file_path = "samples/mscons-message-example.txt" \
               if os.path.exists("samples/mscons-message-example.txt") \
               else "tests/samples/mscons-message-example.txt"

           with open(mscons_file_path, encoding='utf-8') as f:
               edifact_data = f.read()

           # Parse the data
           mscons_obj = self.parser.parse(edifact_data)

           # Verify some basic properties
           self.assertIsNotNone(mscons_obj)
           self.assertEqual(mscons_obj.unz_nutzdaten_endsegment.datenaustauschzaehler, 2)
           self.assertEqual(len(mscons_obj.unh_unt_nachrichten), 2)
   ```

3. **Test Fixtures**:
   - The project uses pytest fixtures defined in `tests/conftest.py`
   - These fixtures provide a FastAPI test client for API testing

4. **Sample Data**:
   - Sample MSCONS messages are provided in the `tests/samples` directory
   - Use these for testing or create new ones as needed

## Code Style and Development Guidelines

1. **Code Style**:
   - The project uses flake8 for linting
   - Maximum line length is 120 characters
   - Run flake8 to check for style issues:
     ```bash
     flake8 src tests
     ```

2. **Project Structure**:
   - The project follows a hexagonal (clean) architecture pattern:

         mscons-restify                       # the root folder
         ├── docs                             # contains documentation related to this project, e.g.: openapi specs, how-to guides, etc.
         ├── scripts                          # helper scripts that can supports the project
         ├── src                              # the source code folder
         │   └── msconsparser                 # main package folder
         │       ├── adapters                 # adapter folder
         │       │   └── inbound              # Contains inbound adapters
         │       │       └── rest             # Inbound REST API implementation
         │       │           ├── apis         # **generated** from openapi-spec (not git commited)
         │       │           ├── impl         # custom implementation of the adapters, contains controllers, routers, filters, etc.
         │       │           └── models       # **generated** from openapi-spec (not git commited)
         │       ├── application              # Contains application services and use cases
         │       │   ├── services             # Contains service classes that orchestrate the business logic
         │       │   └── usecases             # Contains use case implementations of inbound ports
         │       ├── domain                   # Contains the domain models and interfaces
         │       │   ├── models               # Contains domain models of the business logic
         │       │   └── ports                # Contains domain interfaces (inbound/outbound ports)
         │       │       └── inbound          # Contains inbound ports (interfaces implemented by use cases)
         │       ├── infrastructure           # Contains cross-cutting concerns like logging
         │       └── libs                     # Contains library code that can be extracted as separate packages
         │           └── edifactmsconsparser  # EDIFACT MSCONS parser library
         │               ├── converters       # Contains segment converters
         │               ├── exceptions       # Contains parser-specific exceptions
         │               ├── handlers         # Contains segment handlers
         │               ├── utils            # Contains utility functions
         │               └── wrappers         # Contains library model wrappers
         │                   └── segments     # Contains segment model definitions
         └── tests                            # Contain all tests of the project

> NOTE: Thus our root domain code source is `src/msconsparser`.

3. **Parser Implementation**:
   - The parser follows the hexagonal architecture with a clear separation between the application and domain layers
   - The application layer contains the `ParserService` which uses the `ParseMessageUseCase` to parse MSCONS messages
   - The `ParseMessageUseCase` implements the `MessageParserPort` interface from the domain layer
   - The actual parsing logic is implemented in the `libs/edifactmsconsparser` package
   - The parser uses a dispatcher pattern to handle different segment types
   - Each segment type has its own converter in `libs/edifactmsconsparser/converters` and handlers in `libs/edifactmsconsparser/handlers`
   - The main parser class is `EdifactMSCONSParser` in `libs/edifactmsconsparser/edifact_mscons_parser.py`
   - Domain models are located in `libs/edifactmsconsparser/wrappers/segments`
   - For a detailed explanation of the parsing process, see [mscons-parsing-process.md](docs/mscons-parsing-process.md)
   - Library related exceptions are defined in `libs/edifactmsconsparser/exceptions` and use these exceptions for library-specific error handling

4. **API Implementation**:
   - The API is implemented using FastAPI
   - The OpenAPI specification is in `docs/edifact-mscons-parser.openapi.yaml`
   - The generated API endpoints are defined in `adapters/inbound/rest/apis`
   - The custom implementation of the controllers/routers are in `adapters/inbound/rest/impl` and for the business logic it is the `domain` directory
   - For details on API generation, see [section openapi-generated-fastapi-server-components](#openapi-generated-fastapi-server-components)

## Deployment

1. **Docker Deployment**:
   - The application is containerized and can be deployed using Docker
   - The Docker image exposes port `8000`
   - Use the provided docker-compose.yaml for simple testings and deployments

2. **Environment Variables**:
   - The application uses environment variables for configuration
   - These can be set in the docker-compose.yaml file or passed to the container

## Versioning

This project follows [Semantic Versioning 2.0.0](https://semver.org/) principles with a specific adaptation for the MSCONS specification version.

### Version Format

The version format is `MAJOR.MINOR.PATCH` where:

    1.204c.1
    |  |   |
    1  |   | -> **MAJOR**: Incremented when making incompatible API changes
      204c | -> **MINOR**: Contains the MSCONS specification version (e.g., "204c" for MSCONS version 2.4c, the 0-placeholder was added, in case the minor version of MSCONS-specs is getting greater than 9x, e.g. 3.10a => 2.310c.0)
           0 -> **PATCH**: Incremented when making backward compatible bug fixes

### Current Version

The current version can be found in the [pyproject.toml](pyproject.toml) file. 

### Version Consistency

There are two important places specifiying the version numbers in this project:

1. **Project Version**: Defined in `pyproject.toml` (e.g., `1.204c.1`)
2. **API Version**: Defined in the OpenAPI specification (e.g., `1.204c.1`)

Please ensure those places contain the same version number.

### When to Update Versions

- Increment the **MAJOR** version when you make incompatible API changes
- Update the **MINOR** version when the supported MSCONS specification version changes
- Increment the **PATCH** version when you make backward compatible bug fixes or enhancements

## Last words

> Please refer to project documentation and scripts in the [docs](docs) and [scripts](scripts) directories for more details.
