---
name: illustration
description: Use to create the header image and the inline illustrations of a blog post on this site, drawn in the line style of 19th century naturalist plates (black ink, hatching, stippling, cross-sections), with OpenAI gpt-image. Reads the post, proposes a visual script for approval, generates, saves into the post's assets and inserts the images. Fires on 'illustrate this post', 'header image', 'add an illustration', 'illustration', 'regenerate figure 2'.
---

# illustration

Turns a post from `src/content/blog/` into one header image and a few inline illustrations, drawn in a single, recognisable line style.

**Guiding principle: the drawing carries an idea of the post, it does not decorate it.** A naturalist's plate exists to show how a living thing is built and how it works. Each illustration shows a mechanism, a tension or a before/after from the text, through an organism, an anatomical structure or, when nothing living fits, an object. If a section has no idea that a drawing would make clearer, it gets no drawing.

Inspired by [article-image-generator-skill](https://github.com/ifeihong/article-image-generator-skill) (visual script first, locked style, quality gates), narrowed to one style and one site.

---

## Style: the naturalist's plate

What we borrow from 19th century natural-history and anatomical plates is **the drawing itself**:

- black ink on a blank background, no colour, no grey wash, no gradient;
- fine, even pen lines, slightly thicker outlines; sparse, most surfaces left white;
- shading only by **parallel hatching**, cross-hatching or **stippling**, never by fill;
- scientific views: cross-section, dissection, the specimen from its most telling angle, related specimens side by side, dashed lines for hidden parts and movement;
- one subject, centred, nothing cropped, generous white space.

**Pick the subject's domain from the article.** Memory, learning, consolidation: biology (organisms, shells, cells, neurons); the reference set is the hermit crab and its shells, the nautilus section, cells sharing one DNA, the neuron with dormant branches. Pipelines, gates, verification, control: 19th century machinery (canal locks, railway points and signals, governors, balances, looms), drawn with the same open line as an engineering plate. Never mix both in one drawing.

What we **do not** borrow: plate formalism (plate numbers, Latin labels, reference letters, captions, borders). No text in the image at all, unless the user asks for one or two words.

Also forbidden: people and faces, cute or cartoon style, flat vector icons, flowcharts and boxes-and-arrows, slide-deck aesthetics, photorealism, paper texture or yellowed background (the site provides the paper).

The prompt block that encodes this lives in `references/style.md`. Every prompt starts with it, unchanged.

---

## Formats

| Slot | Size | Use |
|---|---|---|
| Header | `1536x1024` (3:2) | `heroImage` in the front matter, shown above the title |
| Inline | `1536x1024` (3:2) by default, `1024x1024` for a single compact object | after the paragraph it illustrates |

Count: 1 header + 1 inline per ~600 words, 4 inline at most. Fewer is better.

Background is always transparent (PNG): the site inverts images in dark mode, which only works on black line art over transparency.

---

## Workflow

### 1. Read the post

Read the post (`src/content/blog/<slug>.md`) in full. List its **anchors**: the central claim, each mechanism it explains, the trade-offs, the before/after. Ignore sections that are pure context.

### 2. Visual script (always, before generating)

For the header and each inline slot, write:

- **Where**: after which paragraph (quote its first words).
- **Idea**: the one sentence of the post the drawing makes visible.
- **Object**: the machine or object that embodies it, and **why this object** (what in its mechanism maps to the idea).
- **View**: cutaway, exploded, oblique, section…
- **Composition**: what is in the frame, what is hidden (dashed), what moves.

For each slot, propose **two or three objects**, best first. A good subject makes the reader *see* the mechanism: a hermit crab changing shells for "the memory outlives the tool", a nautilus whose chambers all stay sealed for "versioned, append-only", a neuron with pale dormant branches for "archived, not deleted". A weak object only labels the topic (a brain for "memory", a robot for "agent"): avoid.

Show the script, then **wait for the user's choices**. Never generate before the script is approved: images cost money and the user's taste decides.

### 3. Generate

```bash
python3 .claude/skills/illustration/scripts/generate.py \
  --prompt-file /tmp/illustration/<slug>-01.txt \
  --out src/assets/illustrations/<slug>/01-<name>.png \
  --size 1536x1024 --draft
```

- Prompt file = `references/style.md` block + the composition, in English, concrete and visual (shapes, parts, view angle), never the abstract idea alone.
- **Draft quality is the default** (`--draft`: fast model, low quality). For this line style it is good enough to publish; the user chose it over the quality model. Use the quality model (no `--draft`) only when the user asks for it.
- **Style consistency**: pass the header as `--reference` for the inline images when their line weight or hatching drifts from it.
- Inline images: add `--trim` to crop the empty bands above and below the drawing. Never trim the header (cards expect 3:2).
- `OPENAI_API_KEY` comes from the environment (the user's shell profile). Never print it, never write it to a file.

### 4. Quality gates

Look at every image before showing it, composited on the site's paper colour (`#f8f7f3`): the raw transparent PNG hides how dense the drawing really is. Regenerate (at most twice, adjusting the prompt) when:

- there is colour, grey fill, a gradient or a paper texture;
- it looks like a dense engraving (texture everywhere) rather than an open naturalist's plate;
- there is text, numerals, a caption or a border;
- the subject is cropped or the frame is crowded;
- it reads as an icon, a diagram with boxes, or a cartoon;
- the object does not show the mechanism promised in the script.

### 5. Insert

- Header: `heroImage: '../../assets/illustrations/<slug>/00-header.png'` in the front matter.
- Inline: a Markdown image after the paragraph, with an `alt` that describes the drawing for a reader who cannot see it:

  ```markdown
  ![Cutaway of a ratchet wheel: the pawl lets it turn one way only.](../../assets/illustrations/<slug>/01-ratchet.png)
  ```

- Check the page in the dev server, light and dark.

### 6. Report

One line per image: slot, object, file, kept or regenerated. No style theory.

---

## Files

- `references/style.md`: the style prompt block, and the negative list.
- `scripts/generate.py`: calls the OpenAI Images API (generation, or edit with a style reference), writes a transparent PNG.
- Output: `src/assets/illustrations/<slug>/`, numbered `00-header.png`, `01-<name>.png`…
