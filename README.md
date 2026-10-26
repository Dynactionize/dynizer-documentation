# Dynizer Documentation

Documentation repository for the [Dynizer](https://www.dynizer.com) platform by Dynactionize NV.

## Repository Structure

```
docs/           Markdown documentation files
api/            OpenAPI specification files (YAML)
openapi_to_md.py   Script to convert OpenAPI specs to Markdown
```

## Documentation

The `docs/` directory contains detailed documentation covering:

- **[Dynizer Overview](docs/dynizer_overview.md)** — Architecture, semantic model, and core concepts
- **[DQL](docs/DQL.md)** — Dynizer Query Language reference
- **[Actions](docs/dynizer_actions.md)** — Dynizer action definitions
- **[Proto](docs/dynizer_proto.md)** — Protocol buffer definitions
- **[Pipeline](docs/dynizer-pipeline.md)** — Pipeline architecture and usage
- **[Pipeline Plugins](docs/dynizer_pipeline_plugins.md)** — Available pipeline plugins
- **[Analyze API](docs/dynizer_analyze_api.md)** — Analyze API documentation
- **[Analyze API v2](docs/dynizer_analyze_api_v2.md)** — Analyze API v2 documentation
- **[Analyze v2 Core](docs/dynizer_analyze_v2_core.md)** — Analyze v2 core concepts
- **[Extract Text API](docs/dynizer_extract_text_api.md)** — Text extraction API
- **[Swagger](docs/dynizer.swagger.md)** — Dynizer gRPC gateway / REST API

## API Specifications

The `api/` directory contains OpenAPI specs for:

- Dynizer Analyze API (`dynizer-analyze-api.openapi.yaml`)
- Dynizer Analyze API v2 (`dynizer-analyze-api-v2.openapi.yaml`)
- Dynizer Pipeline API v1.0.5 and v1.1.0
- Dynizer Extract Text API (`dynizer-extract-text-api.openai.yaml`)
- Dynizer MAG API (`dynizer-mag-api.openai.yml`)
- Dynizer Split Service (`dynizer-split-service.openapi.yaml`)

## OpenAPI to Markdown Converter

Convert an OpenAPI YAML/JSON spec to Markdown:

```bash
python openapi_to_md.py <input.yaml> <output.md>
```

Requires PyYAML (`pip install pyyaml`).

## License

[MIT](LICENSE) — Copyright (c) 2025 Dynactionize NV
