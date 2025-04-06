import fitz
import os

def extract_text_and_images(pdf_path):
    doc = fitz.open(pdf_path)
    text_blocks = []
    image_paths = []

    for i, page in enumerate(doc):
        text_blocks.append(page.get_text())
        for img_index, img in enumerate(page.get_images(full=True)):
            base_image = doc.extract_image(img[0])
            image_bytes = base_image["image"]
            img_path = f"temp_page_{i}_img_{img_index}.png"
            with open(img_path, "wb") as img_file:
                img_file.write(image_bytes)
            image_paths.append(img_path)

    return text_blocks, image_paths