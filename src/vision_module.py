from PIL import (
    Image,
    ImageFilter,
    ImageOps
)

import pytesseract

# ---------------------------------------------------
# TESSERACT PATH
# ---------------------------------------------------

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# ---------------------------------------------------
# OCR TEXT FILTER
# ---------------------------------------------------

def _is_meaningful_text(
    text: str
):

    if not text:

        return False

    text = text.strip()

    if len(text) < 5:

        return False

    return True

# ---------------------------------------------------
# PREPROCESS IMAGE
# ---------------------------------------------------

def preprocess_image(
    image_path: str
):

    try:

        img = Image.open(
            image_path
        ).convert("L")

        # CONTRAST
        img = ImageOps.autocontrast(
            img
        )

        # SHARPEN
        img = img.filter(
            ImageFilter.SHARPEN
        )

        # RESIZE
        w, h = img.size

        img = img.resize(
            (w * 2, h * 2)
        )

        # OCR
        text = pytesseract.image_to_string(
            img,
            lang="eng",
            config="--psm 6"
        )

        text = text.strip()

        if _is_meaningful_text(text):

            return text

        return ""

    except Exception as e:

        print(
            "[OCR ERROR]:",
            e
        )

        return ""