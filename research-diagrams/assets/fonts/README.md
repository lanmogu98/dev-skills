# Rendering fonts

Unmodified Source Sans 3 Regular and Semibold, release `3.052R`, from
[Adobe's source-sans repository](https://github.com/adobe-fonts/source-sans/tree/3.052R/OTF).
The SIL Open Font License and copyright notice are retained in [OFL.txt](OFL.txt).
The rendering profile records the exact file hashes.

Use `font-family="Source Sans 3"` with weights 400 and 600 in SVG authoring sources.
These fonts do not cover every language or mathematical symbol. For another script,
put the necessary licensed fonts in a project font directory, record a project
profile with `render_svg.py lock --font-dir ... --profile ...`, and inspect glyphs.
The exporter uses only that directory, avoiding system-font fallback. Keep its
fonts and licenses with the editable figure sources when sharing the build.
