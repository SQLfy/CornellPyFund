Class work for python fundamentals. More importantly the dev container definition.

Substituting in uv pip 

 "postCreateCommand": "python -m ipykernel install --user --name=pyfundamentals --display-name='Python (pyfundamentals)'",
 with 
 "postCreateCommand": "curl -LsSf https://astral.sh/uv/install.sh | sh && python -m ipykernel install --user --name=pyfundamentals --display-name='Python (pyfundamentals)'",
