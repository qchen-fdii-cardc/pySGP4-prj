import os
import subprocess
import tempfile

TYPST_IMGS_DIR = "typst_imgs"
IMGS_DIR = "imgs"
PAGE_WRAPPER = """#set page(width: 30em, height: auto, margin: 12pt, fill: white)
#show: body => block(
    width: 100%,
    inset: 10pt,
    stroke: 0.8pt + green,
    radius: 4pt,
    body,
)
"""

os.makedirs(IMGS_DIR, exist_ok=True)

for filename in os.listdir(TYPST_IMGS_DIR):
    if filename.endswith(".typ"):
        typ_path = os.path.join(TYPST_IMGS_DIR, filename)
        # Read the original .typ file
        with open(typ_path, "r", encoding="utf-8") as f:
            typ_content = f.read()
        # Prepend the page and border directives.
        modified_content = PAGE_WRAPPER + typ_content
        # Write to a temporary file
        with tempfile.NamedTemporaryFile("w", suffix=".typ", delete=False, encoding="utf-8") as tmp_file:
            tmp_file.write(modified_content)
            tmp_typ_path = tmp_file.name
        png_name = os.path.splitext(filename)[0] + ".png"
        png_path = os.path.join(IMGS_DIR, png_name)
        subprocess.run([
            "typst", "compile", tmp_typ_path, png_path
        ], check=True)
        print(f"Generated {png_path} from {typ_path}")
