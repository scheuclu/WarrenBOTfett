datamodel-codegen \
  --input trading212_openapi.json \
  --output models.py \
  --output-model-type pydantic_v2.BaseModel \
  --field-constraints \
  --use-standard-collections \
  --target-python-version 3.13