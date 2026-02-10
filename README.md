Class work for python fundamentals. More importantly the dev container definition.

Substituting in uv pip 

 "postCreateCommand": "python -m ipykernel install --user --name=pyfundamentals --display-name='Python (pyfundamentals)'",
 with 
 "postCreateCommand": "curl -LsSf https://astral.sh/uv/install.sh | sh && python -m ipykernel install --user --name=pyfundamentals --display-name='Python (pyfundamentals)'",

## GitHub Copilot

This repository is configured with GitHub Copilot and has the memory feature enabled. For more information on how to use it, see the [Copilot Memory Guide](docs/copilot-memory-guide.md).

