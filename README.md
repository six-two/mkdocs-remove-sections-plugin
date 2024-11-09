# mkdocs-remove-sections-plugin

Remove marked sections from pages.
For example to remove private information from a public version of a web site.

## Installation

You can install it with `pip`:
```bash
pip install mkdocs-remove-sections-plugin
```

## Usage

Add the plugin to your `mkdocs.yml`:
```yaml
plugins:
- search
- remove_sections
```

To remove a section and its subsections, you can begin its title with `Private:` like `## Private: My section`.

If you need a more precise removal, you can also manually set start and end points for the removal.
Any content on pages between `<!-- remove:start -->` and `<!-- remove:end -->` is replaced by the plugin with the text `Some content has been redacted in this version`.
If there are uncertanities (start and end tags do not propperly match up), then this plugin will default to cutting too much rather than too little.
In addition a warning is shown during the build.

## Configuration

You can configure the plugin with the following options.
The information shown below shows the default values:
```yaml
plugins:
- search
- remove_sections:
    section_start_pattern: "<!--\\s*remove:start\\s*-->"
    section_end_pattern: "<!--\\s*remove:end\\s*-->"
    section_heading_pattern: "^Private: "
    section_replace_with: "\n\n> Some content has been redacted in this version.\n\n"
    regex_case_sensitive: false
```

### section_start_pattern

Regular expression pattern that marks the start of a section that should be removed.

### section_end_pattern

Regular expression pattern that marks the end of a section that should be removed.

### section_heading_pattern

Regular expression for a section heading (`h1` through `h6`) that marks a section to be removed.
Any subsections are removed as well.
You can use it like this:
```markdown
## Private: Section to remove
```

### section_replace_with

The removed content will be replaced with this text.
You can set an empty string to remove it entirely.
By default a placeholder is shown, so that you see that something was removed.

### regex_case_sensitive

This controls, whether the patterns you defined with the other options should be case sensitive or insensitive.
It defaults to case insensitive.

## Notable changes

### Version 0.1.0

- Added removing sections by title

### Version 0.0.1

- Initial version
