# The builder image stage, used to build the virtual environment
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim AS builder

# Install and configure Poetry 1.5.1
RUN pip install poetry==1.5.1
# Do not ask any interactive questions
ENV POETRY_NO_INTERACTION=1 \
    # Create venv in project root (this will be copied to the `runtime` stage)
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    # Create venv if one doesn't already exist
    POETRY_VIRTUALENVS_CREATE=1 \
    # Set the cache directory that will later be removed
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set the working directory and copy the dependency files
WORKDIR /app
COPY /app/pyproject.toml /app/poetry.lock ./

# Install application dependencies
RUN poetry lock --no-update
RUN poetry install --without dev --no-root
RUN rm -rf $POETRY_CACHE_DIR
#RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image stage, used to just run the code provided its virtual environment
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim AS runtime

# The TCSO_ROOT_CA is passed via build args to the docker build command in the
# build_deploy stage of the GitLab pipeline. Certificates are added to the CA
# certificate database using the update-ca-certificates command.
ARG TCSO_ROOT_CA
RUN echo "$TCSO_ROOT_CA" > /usr/local/share/ca-certificates/tcso-root.crt && \
    update-ca-certificates
# The HTTPX library uses the SSL_CERT_FILE env variable to load CA certificates
ENV SSL_CERT_FILE=/usr/local/share/ca-certificates/tcso-root.crt

# Set the path variable to have the venv in front, and copy it from builder stage
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Copy the application code
COPY /app .
