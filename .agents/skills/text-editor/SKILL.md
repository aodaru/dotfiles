---
name: text-editor
description: Grammar and spell checker for Spanish and English. Use when user wants to correct, proofread, or check text for grammar, spelling, or style errors. Supports bilingual (Spanish/English) text with automatic language detection.
---

# Text Editor

Grammar and spell checker skill using LanguageTool API for Spanish and English.

## When to Use This Skill

Activate when user:
- Asks to "corrige", "revisa", "ortografía", "grammar", "spell"
- Requests "proofread", "corrección", "fix grammar", "check spelling"
- Needs to fix errors in Spanish or English text
- Asks for "revisar texto" or "revisar orthografía"

## How It Works

### Step 1: Get Text to Check

Receive the text from the user. If user provides a file path, read it first.

### Step 2: Detect Language (if needed)

The API can auto-detect, but you can also:
- If text is mostly Spanish → use `es-ES`
- If text is mostly English → use `en-US`
- Use `auto` for automatic detection

### Step 3: Call LanguageTool API

Use `Bash` tool to call the API:

```bash
curl -s -X POST "https://api.languagetool.org/v2/check" \
  -d "text=<encoded_text>" \
  -d "language=auto"
```

For multi-paragraph text, use `-d "text=$TEXT"` with proper quoting.

### Step 4: Process Results

The API returns JSON with:
- `matches`: Array of errors found
- Each match has:
  - `message`: Description of error
  - `context`: The sentence with error highlighted
  - `suggestions`: Array of suggested corrections
  - `rule`: Rule that triggered the error

### Step 5: Apply Corrections or Present Results

**Option A: Show all errors with suggestions**
Present a list of errors found, letting user choose which to apply.

**Option B: Auto-apply corrections**
If user explicitly asks to "fix" or "correct", apply the first suggestion for each error automatically.

**Option C: Show statistics**
Tell user how many errors found, by category (grammar, spelling, style).

## Error Categories

| Category | Spanish Examples | English Examples |
|----------|------------------|------------------|
| Spelling | "aca" → "ahí", "haber" vs "a ver" | "teh" → "the" |
| Grammar | "yo soy" → "soy", "le dijé" | "I are" → "I am" |
| Punctuation | Falta tilde, coma mal usada | Missing Oxford comma |
| Style | Repeticiones, muletillas | Wordiness, passive voice |

## Special Rules for Spanish

- **Tildes:**檢查必要的水印位置
- **b/v:** "haber" vs "a ver", "vaya" vs "baya"
- **h:** "he" vs "eh", "huevo" vs "uevo"
- **q/k:** "que" vs "ke"
- **accentos diacríticos:** "él", "tú", "mí", "sí"

## Special Rules for English

- **their/there/they're**
- **your/you're**
- **its/it's**
- **affect/effect**
- **than/then**

## Output Format

### Error List Format
```
🔍 Errores encontrados: N

1. Gramática: "yo soy inteligente"
   → Message: "Possible typo: Did you mean..."
   → Suggestion: "soy inteligente"
   → Context: "Yo soy inteligente porque..."

2. Ortografía: "haber echo"
   → Message: "Confusion of 'haber' (to have) and 'a ver' (let's see)"
   → Suggestion: "haber hecho"
   → Context: "Lo hätte echo si..."
```

### Corrected Text Format
```
✅ Texto corregido:

El texto original contenía X errores. Aquí está la versión corregida:

[Texto corregido]
```

## Edge Cases

- **Empty text:** Ask user to provide text
- **Very long text (>20KB):** Split into chunks, process separately
- **Non-Spanish/English:** Warn user this skill only supports ES/EN
- **API failure:** Show error, suggest trying again or manual check
- **No errors found:** Congratulate user! "No se encontraron errores. ¡Buen trabajo!"

## Examples

### Example 1: Simple correction
User: "corrige este texto: Yo soy una persona que le gusta mucho jugar football"

Process:
1. Call API with text
2. API returns: "football" → "futbol" (in ES), or keeps "football" (in EN)
3. Apply first suggestion
4. Output corrected text

### Example 2: Proofread with explanation
User: "revisa esta email para mi jefe"

Process:
1. Get text
2. Call API
3. Show all errors with explanations
4. Let user decide which to apply

## Related Skills

- **ghostwriter**: Use after text-editor to generate new content that gets proofread
