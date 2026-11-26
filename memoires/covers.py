"""Couverture d'un mémoire : la première page du PDF, en JPEG."""
import pymupdf

COVER_WIDTH = 720


def first_page_jpeg(pdf_bytes: bytes) -> bytes | None:
    """Renvoie la première page en JPEG, ou None si le PDF ne peut pas être lu."""
    try:
        with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
            if doc.page_count == 0:
                return None
            page = doc[0]
            zoom = COVER_WIDTH / page.rect.width
            pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), alpha=False)
            return pix.tobytes("jpeg", jpg_quality=82)
    except Exception:
        return None
