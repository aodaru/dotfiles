---
name: markdown-image-organizer
description: >
  Organize, rename, and normalize image references in Markdown files.
  Use this skill whenever the user mentions organizing images, renaming images,
  cleaning up markdown image references, standardizing image files in a markdown
  document, or working with attachments/annexes in a manual or documentation file.
  Also trigger when the user mentions images with spaces in their names,
  broken image links in markdown, or wants to structure/rename annexes or
  attachments referenced in .md files. This applies to Obsidian vaults,
  documentation repositories, manuals, guides, or any markdown-based content
  with embedded images.
  When the user says things like "organize images", "rename images in markdown",
  "fix image references", "standardize image names", "clean up attachments",
  "rename anexos", or mentions multiple markdown files with image issues,
  ALWAYS use this skill.
---

# Markdown Image Organizer

## Purpose

Normalize image references in one or more Markdown files by:
1. Finding all referenced images
2. Renaming them to a clean, consistent format
3. Moving them to a standard location (e.g., `anexo/` subfolder)
4. Updating all references in the Markdown file(s)

## When to Use

- User mentions images with spaces or special characters in names
- User wants to organize/rename attachments or annexes
- Multiple Markdown files reference images inconsistently
- User wants a clean, standardized image naming convention
- User mentions broken or inconsistent image paths in markdown

## Required Tools

- `read`: Read .md files and inspect current references
- `glob`: Find image files in directories
- `edit`: Update image references in .md files
- `bash`: Use `mv` to rename/move image files, `mkdir` to create directories

## Workflow

### Step 1: Identify Target Markdown Files

Extract the Markdown file path(s) from the user's request. The user may:
- Reference files with `@filename.md`
- Provide explicit paths
- Say "all .md files in this folder"

If the user does not specify files, ASK: "Which Markdown file(s) would you like me to process?"

If the user says "all" or "everything", use `glob` to find all `.md` files in the current working directory.

### Step 2: Confirm Naming Format

Propose the default naming convention to the user:

> **Default format**: `{md_filename_snake_case}_anexo_{N}.{ext}`
> Example: For `Cierre de caja.md`, images become `cierre_de_caja_anexo_1.png`, `cierre_de_caja_anexo_2.png`, etc.

Ask: "¿Deseas personalizar el formato de renombrado? (Sí/No)"

If the user says "Sí" or "Yes", ask: "¿Qué prefijo o patrón deseas usar?"

If the user provides a custom format, use it. Otherwise, use the default.

**Rules for the default format:**
- Convert markdown filename to `snake_case` (lowercase, spaces → underscores, remove accents if needed)
- Remove the `.md` extension from the filename base
- Append `_anexo_{N}` where N starts at 1
- Preserve the original file extension (`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.svg`, etc.)

### Step 3: Process Each Markdown File

For EACH Markdown file, execute the following sub-steps in order:

#### 3.1 Read the Markdown File

Use `read` to get the full content of the file.

#### 3.2 Extract Image References

Scan the file content and identify ALL image references. Look for these patterns:

**Pattern A — Standard Markdown:**
```
![alt text](path/to/image.png)
![alt text](path%20with%20spaces.png)
```

**Pattern B — Wiki-style Links (Obsidian):**
```
![[image.png]]
![[path/to/image.png]]
![[image.png|caption text]]
```

**Pattern C — HTML img tags:**
```
<img src="path/to/image.png">
<img src="path%20with%20spaces.png">
```

For each match, record:
- The **exact original string** as it appears in the file (needed for `edit`)
- The **image filename** (e.g., `image.png`, `Pasted image 20250101.png`)
- The **relative path** if specified (e.g., `anexo/image.png`, `assets/image.png`)

#### 3.3 Locate Each Image in the Filesystem

For each unique image filename found in Step 3.2:

1. **Try the exact path** as written in the markdown reference
2. If not found, search using `glob` in these locations (in order):
   - The same directory as the `.md` file
   - `anexo/` subdirectory
   - `assets/` subdirectory
   - `images/` subdirectory

Use glob patterns like `**/*filename.png` to search recursively if needed.

Record:
- ✅ **Found**: Current absolute path
- ❌ **Not Found**: Mark as missing

#### 3.4 Rename and Relocate Images

For each **found** image:

1. Determine the target directory:
   - Create `anexo/` as a subdirectory of the `.md` file's directory if it does not exist (use `bash mkdir -p`)
   - The renamed image will live in `anexo/`

2. Compute the new filename using the format from Step 2

3. Use `bash mv` to rename/move the file:
   ```bash
   mv "source/path/old name.png" "target/anexo/new_name_anexo_1.png"
   ```
   Always quote paths that contain spaces.

**Important**: If multiple `.md` files are being processed, each file gets its own numbering sequence (N=1, 2, 3...). Do NOT share counters across different markdown files unless the user explicitly requests it.

#### 3.5 Update References in the Markdown File

For each image that was successfully renamed:

Use `edit` to replace the **exact original string** (from Step 3.2) with the new reference.

**Reference replacement rules:**

- **Pattern A** `![alt](old/path.png)` → `![alt](anexo/new_name_anexo_N.png)`
- **Pattern B** `![[old/path.png]]` → `![[anexo/new_name_anexo_N.png]]`
  (Preserve any `|caption` text if present)
- **Pattern B with pipe** `![[old.png|caption]]` → `![[anexo/new_name_anexo_N.png|caption]]`
- **Pattern C** `<img src="old/path.png">` → `<img src="anexo/new_name_anexo_N.png">`

**Important**: Always use `replaceAll: true` when the same image reference appears multiple times in the file.

If the old reference used URL-encoded spaces (`%20`), replace the entire URL-encoded path.

### Step 4: Generate Final Report

After ALL markdown files have been processed, present a clear report to the user.

Use this exact report structure:

```markdown
## 📊 Reporte de Organización de Imágenes

### Archivos Markdown Procesados
| Archivo | Estado |
|---------|--------|
| `filename.md` | ✅ Procesado |

### Imágenes Renombradas Exitosamente
| # | Nombre Anterior | Nuevo Nombre | Ubicación |
|---|----------------|-------------|-----------|
| 1 | `Pasted image 20250101.png` | `manual_anexo_1.png` | `anexo/` |

### Imágenes Referenciadas pero NO Encontradas
| # | Referencia en archivo | Razón |
|---|----------------------|-------|
| 1 | `missing.png` | Archivo no encontrado en carpeta ni subcarpetas |

### Resumen
- ✅ {N} imágenes renombradas
- ⚠️ {M} imágenes no encontradas
- 📝 {K} archivos markdown actualizados
```

If there are missing images, advise the user:
> "⚠️ Algunas imágenes referenciadas no fueron encontradas. Por favor verifica que existan en el sistema de archivos o que las referencias sean correctas."

## Edge Cases and Important Notes

### Duplicate Filenames
If two different markdown files both reference an image with the same filename (e.g., `image.png`), but they are different files in different folders, treat them as separate images. Each gets its own rename within its respective context.

### Images Referenced Multiple Times
The same image may be referenced multiple times within one markdown file. Use `replaceAll: true` to update all occurrences.

### Images Already in anexo/
If an image is already in `anexo/` but has a bad name (spaces, etc.), still rename it to the standard format and update the reference.

### Spaces and Special Characters
When renaming, always remove spaces from the new filename. Use `snake_case` consistently.

### Case Sensitivity
Assume case-sensitive filesystems. If the reference says `Image.PNG` but the file is `image.png`, the glob should still find it (use case-insensitive patterns if the tool supports it).

### Nested Subdirectories
If images are in deeply nested subdirectories (e.g., `docs/assets/images/`), still move them to `anexo/` at the same level as the `.md` file, unless the user specifies otherwise.

## Examples

**Example 1 — Simple file with 2 images:**
- User: "@Manual de Ventas.md organiza las imágenes"
- Result: Images renamed to `manual_de_ventas_anexo_1.png`, `manual_de_ventas_anexo_2.png`
- References updated to `anexo/manual_de_ventas_anexo_1.png`, etc.

**Example 2 — Wiki links with captions:**
- Original: `![[Pasted image 20250101.png|Vista previa]]`
- New: `![[anexo/manual_anexo_1.png|Vista previa]]`
- Caption preserved.

**Example 3 — HTML img tag:**
- Original: `<img src="Screenshot 2025-01-01.png">`
- New: `<img src="anexo/guia_anexo_1.png">`

## Success Criteria

The task is complete when:
1. All found images have been renamed to the agreed format
2. All renamed images are in the `anexo/` folder (or as specified)
3. All references in the markdown file(s) point to the new names/locations
4. The user has received a complete report of what was done and what was missing
