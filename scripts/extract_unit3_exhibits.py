"""Extract the three specification exhibits from prerequisites/unit3.docx.

The extraction preserves the source order and converts Word headings, lists,
and tables to plain Markdown so BMad can review the exhibits as text.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from docx import Document
from docx.document import Document as DocumentObject
from docx.table import Table
from docx.text.paragraph import Paragraph


EXHIBITS = {
    "prd.md": (
        "Product Requirements Document - CircleGuard",
        "Exhibit B: UX Design Specification",
    ),
    "ux-design-specification.md": (
        "UX Design Specification — CircleGuard",
        "Exhibit C: Architecture Decision Document",
    ),
    "architecture.md": (
        "Architecture Decision Document — CircleGuard",
        None,
    ),
}


def iter_blocks(document: DocumentObject):
    """Yield top-level paragraphs and tables in document order."""
    for child in document.element.body.iterchildren():
        if child.tag.endswith("}p"):
            yield Paragraph(child, document)
        elif child.tag.endswith("}tbl"):
            yield Table(child, document)


def clean(value: str) -> str:
    return " ".join(value.replace("\u00a0", " ").split())


def paragraph_markdown(paragraph: Paragraph) -> str:
    text = clean(paragraph.text)
    if not text:
        return ""

    style = paragraph.style.name.lower() if paragraph.style else ""
    if style.startswith("heading 1"):
        return f"# {text}"
    if style.startswith("heading 2"):
        return f"## {text}"
    if style.startswith("heading 3"):
        return f"### {text}"
    if "list bullet" in style:
        return f"- {text}"
    if "list number" in style:
        return f"1. {text}"
    return text


def table_markdown(table: Table) -> str:
    rows: list[list[str]] = []
    for row in table.rows:
        rows.append([clean(cell.text).replace("|", "\\|") for cell in row.cells])
    if not rows:
        return ""

    width = max(len(row) for row in rows)
    rows = [row + [""] * (width - len(row)) for row in rows]
    lines = [
        "| " + " | ".join(rows[0]) + " |",
        "| " + " | ".join(["---"] * width) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows[1:])
    return "\n".join(lines)


def extract(document_path: Path, output_dir: Path) -> None:
    document = Document(document_path)
    blocks = list(iter_blocks(document))
    output_dir.mkdir(parents=True, exist_ok=True)

    extracted_paths: list[Path] = []
    for filename, (start_marker, end_marker) in EXHIBITS.items():
        collecting = False
        rendered: list[str] = []

        for block in blocks:
            if isinstance(block, Paragraph):
                text = clean(block.text)
                if not collecting and text == start_marker:
                    collecting = True
                if collecting and end_marker and text.startswith(end_marker):
                    break
                if collecting:
                    value = paragraph_markdown(block)
                    if value:
                        rendered.append(value)
            elif collecting:
                value = table_markdown(block)
                if value:
                    rendered.append(value)

        if not rendered:
            raise RuntimeError(f"Could not find exhibit beginning with: {start_marker}")

        destination = output_dir / filename
        destination.write_text("\n\n".join(rendered).rstrip() + "\n", encoding="utf-8")
        extracted_paths.append(destination)
        print(f"wrote {destination} ({len(rendered)} blocks)")

    bundle = output_dir / "specification-bundle.md"
    bundle_parts = []
    for path in extracted_paths:
        bundle_parts.append(f"<!-- SOURCE: {path.name} -->\n\n{path.read_text(encoding='utf-8').rstrip()}")
    bundle.write_text("\n\n---\n\n".join(bundle_parts) + "\n", encoding="utf-8")
    print(f"wrote {bundle} ({len(extracted_paths)} exhibits)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("document", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    extract(args.document, args.output_dir)


if __name__ == "__main__":
    main()
