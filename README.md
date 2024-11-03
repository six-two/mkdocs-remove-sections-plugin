# mkdocs-remove-sections-plugin

Remove marked sections from pages.
For example to remove private information from a public version of a web site.

## Usage

Add the plugin to your `mkdocs.yml`:
```yaml
plugins:
- search
- remove_sections
```

Any content on pages between `<!-- remove:start -->` and `<!-- remove:end -->` is replaced by the plugin with the text `Some content has been redacted in this version`.
If there are uncertanities (start and end tags do not propperly match up), then this plugin will default to cutting too much rather than too little.
In addition a warning is shown during the build.

## Configuration

You can configure the plugin with the following options:
```yaml
plugins:
- search
- remove_sections:
    section_start_pattern: "<!--\\s*remove:start\\s*-->"
    section_end_pattern: "<!--\\s*remove:end\\s*-->"
    # section_heading_pattern: "Private: "
    section_replace_with: "\n\n> Some content has been redacted in this version.\n\n"
```

### section_start_pattern

Regular expression pattern that marks the start of a section that should be removed.

### section_end_pattern

Regular expression pattern that marks the end of a section that should be removed.

### section_heading_pattern

**NOT IMPLEMENTED YET**: Regular expression for a section heading (`h1` through `h6`) that marks a section to be removed.
Any subsections are removed as well.
You can use it like this:
```markdown
Text to keep

## Private: Section to remove

This will be removed, since the section title matches the regex.

### Subsection

This will be removed too, since it is a subsection.

## Other section

This will not be removed, since it is a section on the same level as the removed section (not a child).
```

### section_replace_with

The removed content will be replaced with this text.
You can set an empty string to remove it entirely.
By default a placeholder is shown, so that you see that something was removed.
