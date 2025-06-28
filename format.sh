reset; ruff format .
reset; pyright .
isort .
autoflake --remove-unused-variables --remove-all-unused-imports --in-place --recursive
