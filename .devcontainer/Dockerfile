FROM mcr.microsoft.com/devcontainers/python:3.11

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install all your packages with uv (much faster than conda)
RUN uv pip install --system \
    jupyterlab \
    ipykernel \
    numpy \
    pandas \
    matplotlib \
    scikit-learn \
    introcs

EXPOSE 8888