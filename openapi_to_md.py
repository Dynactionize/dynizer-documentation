#!/usr/bin/env python
"""Render an OpenAPI JSON/YAML spec into a Markdown document.

Usage:
    python openapi_to_md.py [OPTIONS] [INPUT] [OUTPUT]

Positional arguments:
    INPUT   Path to OpenAPI JSON or YAML file (or directory of them).
    OUTPUT  Path for the generated Markdown (or output directory).

Options:
    -i, --input PATH    Input file or directory (overrides positional INPUT).
    -o, --output PATH   Output file or directory (overrides positional OUTPUT).
    --input-dir PATH    Directory of OpenAPI specs to convert (all .json/.yaml/.yml).
    --output-dir PATH   Directory for generated Markdown files.

When a directory is given as input (via --input-dir or -i), every OpenAPI
spec (.json, .yaml, .yml) in that directory is converted.  The output
directory defaults to the same directory unless --output-dir / -o is given.

No external dependencies beyond PyYAML (already in the project).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml


# ── Helpers ───────────────────────────────────────────────────────────

def _resolve_ref(spec: dict, ref: str) -> dict:
    """Follow a $ref pointer like '#/components/schemas/Foo'."""
    parts = ref.lstrip("#/").split("/")
    node = spec
    for p in parts:
        node = node.get(p, {})
    return node


def _schema_name(ref: str) -> str:
    return ref.rsplit("/", 1)[-1] if ref else ""


def _type_str(schema: dict, spec: dict) -> str:
    """Human-readable type string from a schema node."""
    if not schema:
        return ""
    if "$ref" in schema:
        name = _schema_name(schema["$ref"])
        return f"[{name}](#{name.lower()})"
    if "anyOf" in schema:
        parts = [_type_str(s, spec) for s in schema["anyOf"]]
        return " | ".join(p for p in parts if p)
    if schema.get("type") == "array":
        items = schema.get("items", {})
        inner = _type_str(items, spec)
        return f"array of {inner}" if inner else "array"
    if schema.get("type") == "object" and "additionalProperties" in schema:
        ap = schema["additionalProperties"]
        if isinstance(ap, dict):
            vtype = _type_str(ap, spec)
            return f"map of {vtype}" if vtype else "object"
    t = schema.get("type", "")
    if schema.get("enum"):
        return f"{t} enum: {schema['enum']}"
    return t


def _schema_ref_link(schema: dict) -> str:
    """Markdown link if the schema is a $ref."""
    if "$ref" in schema:
        name = _schema_name(schema["$ref"])
        return f"[{name}](#{name.lower()})"
    return ""


# ── Rendering ─────────────────────────────────────────────────────────

def _render_info(spec: dict, lines: list[str]) -> None:
    info = spec.get("info", {})
    lines.append(f"# {info.get('title', 'API')}\n")
    if info.get("description"):
        lines.append(f"{info['description']}\n")

    rows = []
    if info.get("version"):
        rows.append(f"| Version | {info['version']} |")
    if info.get("contact"):
        c = info["contact"]
        contact = c.get("name", "")
        if c.get("email"):
            contact += f" <{c['email']}>"
        if c.get("url"):
            contact += f" ({c['url']})"
        rows.append(f"| Contact | {contact} |")
    if rows:
        lines.append("| Field | Value |")
        lines.append("|-------|-------|")
        lines.extend(rows)
        lines.append("")


def _render_tags(spec: dict, lines: list[str]) -> None:
    tags = spec.get("tags", [])
    if not tags:
        return
    lines.append("## Tags\n")
    lines.append("| Name | Description |")
    lines.append("|------|-------------|")
    for tag in tags:
        lines.append(f"| {tag['name']} | {tag.get('description', '')} |")
    lines.append("")


def _render_servers(spec: dict, lines: list[str]) -> None:
    servers = spec.get("servers", [])
    if not servers:
        return
    lines.append("## Servers\n")
    lines.append("| URL | Description |")
    lines.append("|-----|-------------|")
    for s in servers:
        lines.append(f"| `{s['url']}` | {s.get('description', '')} |")
    lines.append("")


def _render_request_body(operation: dict, spec: dict, lines: list[str]) -> None:
    rb = operation.get("requestBody")
    if not rb:
        return
    content = rb.get("content", {})
    for media_type, media in content.items():
        schema = media.get("schema", {})
        link = _schema_ref_link(schema)
        if link:
            lines.append(f"**Request Body** (`{media_type}`): {link}\n")
        else:
            lines.append(f"**Request Body** (`{media_type}`)\n")


def _render_responses(operation: dict, spec: dict, lines: list[str]) -> None:
    responses = operation.get("responses", {})
    if not responses:
        return
    lines.append("**Responses**\n")
    for status, response in responses.items():
        if "$ref" in response:
            resp_obj = _resolve_ref(spec, response["$ref"])
            ref_name = _schema_name(response["$ref"])
            desc = resp_obj.get("description", "")
            content = resp_obj.get("content", {})
            schema = content.get("application/json", {}).get("schema", {})
            schema_link = _schema_ref_link(schema)
            detail = f" — {schema_link}" if schema_link else ""
            lines.append(f"- `{status}`: {desc}{detail}")
        else:
            desc = response.get("description", "")
            content = response.get("content", {})
            schema = content.get("application/json", {}).get("schema", {})
            schema_link = _schema_ref_link(schema)
            detail = f" — {schema_link}" if schema_link else ""
            lines.append(f"- `{status}`: {desc}{detail}")
    lines.append("")


def _render_parameters(operation: dict, spec: dict, lines: list[str]) -> None:
    params = operation.get("parameters", [])
    if not params:
        return
    lines.append("**Parameters**\n")
    lines.append("| Name | In | Type | Required | Description |")
    lines.append("|------|----|------|----------|-------------|")
    for p in params:
        if "$ref" in p:
            p = _resolve_ref(spec, p["$ref"])
        schema = p.get("schema", {})
        lines.append(
            f"| {p.get('name', '')} | {p.get('in', '')} "
            f"| {_type_str(schema, spec)} | {p.get('required', False)} "
            f"| {p.get('description', '')} |"
        )
    lines.append("")


def _render_callbacks(operation: dict, spec: dict, lines: list[str]) -> None:
    callbacks = operation.get("callbacks")
    if not callbacks:
        return
    lines.append("**Callbacks**\n")
    for cb_name, cb in callbacks.items():
        lines.append(f"- `{cb_name}`")
        for expression, methods in cb.items():
            lines.append(f"  - Expression: `{expression}`")
            for method, cb_op in methods.items():
                summary = cb_op.get("summary", "")
                lines.append(f"  - `{method.upper()}` {summary}")
    lines.append("")


def _render_endpoints(spec: dict, lines: list[str]) -> None:
    lines.append("## Endpoints\n")
    for path, methods in spec.get("paths", {}).items():
        for method, operation in methods.items():
            if not isinstance(operation, dict):
                continue
            lines.append(f"### `{method.upper()} {path}`\n")
            if operation.get("summary"):
                lines.append(f"*{operation['summary']}*\n")
            if operation.get("tags"):
                tags = ", ".join(f"`{t}`" for t in operation["tags"])
                lines.append(f"Tags: {tags}\n")
            if operation.get("operationId"):
                lines.append(f"Operation ID: `{operation['operationId']}`\n")
            if operation.get("description") and operation["description"] != operation.get("summary"):
                lines.append(f"{operation['description']}\n")

            _render_parameters(operation, spec, lines)
            _render_request_body(operation, spec, lines)
            _render_responses(operation, spec, lines)
            _render_callbacks(operation, spec, lines)
            lines.append("---\n")


def _render_schema(name: str, schema: dict, spec: dict, lines: list[str]) -> None:
    lines.append(f"### {name}\n")
    if schema.get("description"):
        lines.append(f"{schema['description']}\n")

    props = schema.get("properties", {})
    required = set(schema.get("required", []))
    if props:
        lines.append("| Field | Type | Required | Description |")
        lines.append("|-------|------|----------|-------------|")
        for field_name, field_schema in props.items():
            ftype = _type_str(field_schema, spec)
            req = "yes" if field_name in required else ""
            desc = field_schema.get("description", "")
            if field_schema.get("default") is not None:
                desc += f" (default: `{field_schema['default']}`)"
            lines.append(f"| {field_name} | {ftype} | {req} | {desc} |")
        lines.append("")

    if schema.get("enum"):
        lines.append(f"Enum values: {schema['enum']}\n")


def _render_components(spec: dict, lines: list[str]) -> None:
    components = spec.get("components", {})

    responses = components.get("responses", {})
    if responses:
        lines.append("## Response Components\n")
        for name, response in responses.items():
            lines.append(f"### {name}\n")
            if response.get("description"):
                lines.append(f"{response['description']}\n")
            content = response.get("content", {})
            for media_type, media in content.items():
                schema = media.get("schema", {})
                link = _schema_ref_link(schema)
                if link:
                    lines.append(f"Content (`{media_type}`): {link}\n")
        lines.append("")

    schemas = components.get("schemas", {})
    if schemas:
        lines.append("## Schemas\n")
        for name, schema in schemas.items():
            _render_schema(name, schema, spec, lines)


# ── Main ──────────────────────────────────────────────────────────────

def render(spec: dict) -> str:
    lines: list[str] = []
    _render_info(spec, lines)
    _render_tags(spec, lines)
    _render_servers(spec, lines)
    _render_endpoints(spec, lines)
    _render_components(spec, lines)
    return "\n".join(lines) + "\n"


SPEC_EXTENSIONS = {".json", ".yaml", ".yml"}


def _convert_file(input_path: Path, output_path: Path) -> None:
    """Convert a single OpenAPI spec file to Markdown."""
    text = input_path.read_text()
    if input_path.suffix == ".json":
        spec = json.loads(text)
    else:
        spec = yaml.safe_load(text)

    md = render(spec)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(md)
    print(f"wrote {output_path}")


def _md_output_for(input_path: Path, output_dir: Path) -> Path:
    """Derive the .md output path from an input spec path."""
    return output_dir / (input_path.stem + ".md")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render OpenAPI JSON/YAML specs into Markdown.",
    )
    parser.add_argument("input", nargs="?", help="Input file or directory")
    parser.add_argument("output", nargs="?", help="Output file or directory")
    parser.add_argument("-i", "--input-file", dest="input_opt", help="Input file or directory")
    parser.add_argument("-o", "--output-file", dest="output_opt", help="Output file or directory")
    parser.add_argument("--input-dir", help="Directory of OpenAPI specs to convert")
    parser.add_argument("--output-dir", help="Directory for generated Markdown files")
    args = parser.parse_args()

    # Resolve input
    input_path = Path(args.input_dir or args.input_opt or args.input or ".")
    output_path_arg = args.output_dir or args.output_opt or args.output

    if input_path.is_dir():
        # Batch mode: convert all spec files in the directory
        specs = sorted(
            f for f in input_path.iterdir() if f.suffix in SPEC_EXTENSIONS
        )
        if not specs:
            print(f"ERROR: no OpenAPI specs found in {input_path}", file=sys.stderr)
            sys.exit(1)
        out_dir = Path(output_path_arg) if output_path_arg else input_path
        for spec_file in specs:
            _convert_file(spec_file, _md_output_for(spec_file, out_dir))
    else:
        # Single file mode
        if not input_path.exists():
            print(f"ERROR: {input_path} not found.", file=sys.stderr)
            sys.exit(1)
        if output_path_arg:
            out = Path(output_path_arg)
            if out.is_dir() or output_path_arg.endswith("/"):
                out = _md_output_for(input_path, out)
        else:
            out = input_path.with_suffix(".md")
        _convert_file(input_path, out)


if __name__ == "__main__":
    main()
