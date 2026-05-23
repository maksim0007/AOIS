from __future__ import annotations


def ascii_table(headers: list[str], rows: list[list[object]]) -> str:
    text_rows = [[str(cell) for cell in row] for row in rows]
    widths = [len(str(header)) for header in headers]
    for row in text_rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))
    border = "+" + "+".join("-" * (width + 2) for width in widths) + "+"
    lines = [border]
    lines.append("|" + "|".join(f" {str(header):^{widths[index]}} " for index, header in enumerate(headers)) + "|")
    lines.append(border)
    for row in text_rows:
        lines.append("|" + "|".join(f" {cell:^{widths[index]}} " for index, cell in enumerate(row)) + "|")
    lines.append(border)
    return "\n".join(lines)
