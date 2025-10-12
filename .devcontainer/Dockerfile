# Base image tuned for VS Code devcontainers, includes a non-root 'vscode' user
FROM mcr.microsoft.com/devcontainers/miniconda:0-3

# Use conda-forge with strict priority
RUN conda config --add channels conda-forge \
 && conda config --set channel_priority strict

# Copy and apply your environment
COPY ../environment.yml /tmp/environment.yml
RUN conda env update -n base -f /tmp/environment.yml \
 && conda clean -afy

# Make sure Jupyter is reachable if you run it in the container
EXPOSE 8888
