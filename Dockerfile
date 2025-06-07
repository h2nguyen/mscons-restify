FROM python:3.9 AS builder

WORKDIR /usr/src/app

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install --upgrade pip uv

COPY . .
RUN uv pip install --no-cache-dir -e .


FROM python:3.9 AS test_runner
WORKDIR /tmp
COPY --from=builder /venv /venv
COPY --from=builder /usr/src/app/tests tests
COPY --from=builder /usr/src/app/src src
COPY --from=builder /usr/src/app/pyproject.toml pyproject.toml
COPY --from=builder /usr/src/app/LICENSE.txt LICENSE.txt
COPY --from=builder /usr/src/app/README.md README.md
ENV PATH=/venv/bin:$PATH

# install test dependencies
RUN pip install uv && uv pip install ".[dev]"

# run tests
RUN pytest tests


FROM python:3.9 AS service
WORKDIR /root/app/site-packages
COPY --from=test_runner /venv /venv
ENV PATH=/venv/bin:$PATH
