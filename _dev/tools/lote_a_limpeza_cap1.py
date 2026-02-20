from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup, NavigableString

ROOT = Path(r"d:\GitHub\Livro Banco de Dados")
TARGET = ROOT / "capitulo-01.html"


def is_blank_text(text: str) -> bool:
    if text is None:
        return True
    normalized = text.replace("\xa0", " ").replace("&nbsp;", " ")
    return normalized.strip() == ""


def has_meaningful_descendant(tag) -> bool:
    meaningful_tags = {"img", "table", "video", "iframe", "svg", "code", "pre", "ul", "ol", "li"}
    for desc in tag.descendants:
        if getattr(desc, "name", None) in meaningful_tags:
            return True
        if isinstance(desc, NavigableString) and not is_blank_text(str(desc)):
            return True
    return False


def add_tailwind_class(tag, classes):
    current = tag.get("class", [])
    merged = list(dict.fromkeys([*current, *classes]))
    tag["class"] = merged


def main():
    html = TARGET.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    removed_empty_p = 0
    removed_empty_b = 0
    removed_style_attrs = 0
    removed_mso_classes = 0
    normalized_tables = 0
    normalized_cells = 0
    normalized_imgs = 0

    for tag in soup.find_all(True):
        if tag.has_attr("style"):
            del tag["style"]
            removed_style_attrs += 1

    for tag in soup.find_all(True):
        if tag.has_attr("class"):
            original = tag.get("class", [])
            filtered = [class_name for class_name in original if not class_name.startswith("Mso")]
            removed_mso_classes += len(original) - len(filtered)
            if filtered:
                tag["class"] = filtered
            else:
                del tag["class"]

    for bold in soup.find_all("b"):
        txt = bold.get_text(" ", strip=False)
        if is_blank_text(txt) and not has_meaningful_descendant(bold):
            bold.decompose()
            removed_empty_b += 1

    for paragraph in soup.find_all("p"):
        txt = paragraph.get_text(" ", strip=False)
        if is_blank_text(txt) and not has_meaningful_descendant(paragraph):
            paragraph.decompose()
            removed_empty_p += 1

    for table in soup.find_all("table"):
        add_tailwind_class(table, ["border", "border-slate-300", "border-collapse", "w-full", "my-4", "text-sm"])
        for attr in ["width", "height", "cellpadding", "cellspacing", "border"]:
            if table.has_attr(attr):
                del table[attr]
        normalized_tables += 1

        for cell in table.find_all(["th", "td"]):
            add_tailwind_class(cell, ["border", "border-slate-300", "px-3", "py-2", "align-top"])
            for attr in ["width", "height"]:
                if cell.has_attr(attr):
                    del cell[attr]
            normalized_cells += 1

    for image in soup.find_all("img"):
        image["class"] = ["my-4", "rounded-lg", "shadow-sm"]
        for attr in ["width", "height", "hspace", "vspace", "align"]:
            if image.has_attr(attr):
                del image[attr]
        normalized_imgs += 1

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = TARGET.with_name(f"{TARGET.stem}.bak-{timestamp}{TARGET.suffix}")
    backup.write_text(html, encoding="utf-8")
    TARGET.write_text(str(soup), encoding="utf-8")

    print("Lote A finalizado.")
    print(f"Arquivo: {TARGET}")
    print(f"Backup:  {backup}")
    print("--- Relatório ---")
    print(f"<p> vazios removidos: {removed_empty_p}")
    print(f"<b> vazias removidas: {removed_empty_b}")
    print(f"style removidos: {removed_style_attrs}")
    print(f"classes Mso* removidas: {removed_mso_classes}")
    print(f"tabelas normalizadas: {normalized_tables}")
    print(f"células normalizadas: {normalized_cells}")
    print(f"imagens normalizadas: {normalized_imgs}")


if __name__ == "__main__":
    main()
