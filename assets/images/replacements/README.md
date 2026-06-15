# Project Cover Replacement Sources

Put replacement source images in this directory, then run:

```bash
python scripts/build_project_images.py
```

The source files in this directory are ignored by git by default. The script writes optimized site assets to:

```text
assets/images/generated/
```

## Expected Filenames

Use one image per slot. Supported extensions: `.png`, `.jpg`, `.jpeg`, `.webp`.

```text
modelport.png
quantpilot.png
travel-agent.png
mamoji.png
reviewpilot.png
stock-assistant.png
portfolio-og.png
```

`portfolio-og` is optional. If present, it updates the home hero / social image.

## Output Files

For project covers, the script generates:

```text
anime-cover-<slot>.png
anime-cover-<slot>.webp
anime-cover-<slot>-thumb.webp
```

For the home hero / social image, the script generates:

```text
anime-portfolio-og.png
anime-portfolio-og.webp
anime-portfolio-og-thumb.webp
```

## Image Guidance

- Recommended ratio: `16:9`
- Recommended size: `1920x1080` or larger
- The script center-crops to `16:9` if the source ratio differs.
- Use images that are appropriate for public portfolio use.
