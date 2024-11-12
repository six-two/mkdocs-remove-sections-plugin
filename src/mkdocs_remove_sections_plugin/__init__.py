# builtin
import os
import re
# pip
from mkdocs.config.config_options import Type
from mkdocs.config.base import Config
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.structure.pages import Page
from mkdocs.config.defaults import MkDocsConfig

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
logger = get_plugin_logger(__name__)


class RemoveSectionsConfig(Config):
    section_start_pattern = Type(str, default=r"<!--\s*remove:start\s*-->")
    section_end_pattern = Type(str, default=r"<!--\s*remove:end\s*-->")
    section_heading_pattern = Type(str, default=r"^Private:")
    section_replace_with = Type(str, default="\n\n> Some content has been redacted in this version.\n\n")
    regex_case_sensitive = Type(bool, default=False)


class RemoveSectionsPlugin(BasePlugin[RemoveSectionsConfig]):
    def on_config(self, config: MkDocsConfig) -> None:
        flags = 0 if self.config.regex_case_sensitive else re.IGNORECASE
        self.start_tag = re.compile(self.config.section_start_pattern, flags)
        self.end_tag = re.compile(self.config.section_end_pattern, flags)
        self.heading_title_regex = re.compile(self.config.section_heading_pattern, flags)

    def on_page_markdown(self, markdown, page, config, files):
        try:
            markdown = self.strip_sections_marked_with_tags(markdown, page.file.src_uri)
            markdown = self.strip_sections_with_marked_titles(markdown, page.file.src_uri)
            return markdown
        except Exception as ex:
            raise PluginError(f"Uncaught internal error: {ex}")

    def strip_sections_marked_with_tags(self, markdown: str, file_name: str) -> str:
        sections = self.start_tag.split(markdown)
        if len(sections) >= 1:
            # Check the initial section for an end section
            start_parts = self.end_tag.split(sections[0])
            if len(start_parts) == 1:
                # No end section, this is the expected case. We just keep the full beginning section
                pass
            else:
                # End section before the first start section. We cut everything before it.
                logger.logger.warning(f"[remove_sections] {file_name}: {len(start_parts) - 1} end sections found before the first start section. This may have resulted in too much content being cut.")
                sections[0] = self.config.section_replace_with + start_parts[-1]

            # Handle the remaining sections
            for i in range(1, len(sections)):
                parts = self.end_tag.split(sections[i])
                if len(parts) == 2:
                    # This is the expected case. There is one start and one end section. We just keep the part after the end section
                    sections[i] = parts[-1]
                elif len(parts) == 1:
                    # There is no end tag for this start tag, so we cut the entire block
                    logger.logger.warning(f"[remove_sections] {file_name}: No end section after start section {i}. This may have resulted in too much content being cut.")
                    sections[i] = ""
                else:
                    # Multiple end sections for one section. We just keep the text after the last one
                    logger.logger.warning(f"[remove_sections] {file_name}: {len(parts) - 1} end sections after start section {i}. This may have resulted in too much content being cut.")
                    sections[i] = parts[-1]
            
            # Replace the removed content with the configured value
            markdown = self.config.section_replace_with.join(sections)

        return markdown


    def strip_sections_with_marked_titles(self, markdown: str, file_name: str) -> str:
        DONT_REMOVE_CURRENT_LINES = 9999
        lines = markdown.split("\n")
        keep_lines = []
        is_fenced_code_block = False
        remove_section_depth = DONT_REMOVE_CURRENT_LINES # this gets set to the section depth when something gets marked. It is set to a high number when nothing is marked currently.
        for line in lines:
            # Code listings can be indented and still be valid
            if line.lstrip().startswith("```"):
                is_fenced_code_block = not is_fenced_code_block
            elif line.startswith("#") and not is_fenced_code_block:
                # I think that heading lines need to start with a hashtag. If they are indented, they may be in a code block

                # Remove leading hashtags
                level = 0
                title = line
                while title.startswith("#"):
                    title = title[1:]
                    level += 1
                title = title.strip()

                if level <= remove_section_depth:
                    # This section is not a child of the section to remove, so we have to check by its title whether to remove it too
                    if self.heading_title_regex.search(title):
                        # this and children need to be removed
                        remove_section_depth = level
                    else:
                        # stop the deletion here and keep the current line
                        if remove_section_depth != DONT_REMOVE_CURRENT_LINES:
                            remove_section_depth = DONT_REMOVE_CURRENT_LINES
                            keep_lines.append(self.config.section_replace_with)
            
            # If we are in a section the be deleted, then drop all lines. Otherwise keep the lines
            if remove_section_depth == DONT_REMOVE_CURRENT_LINES:
                keep_lines.append(line)

        # if the page ends and we are removing stuff, then we add the replacement text
        if remove_section_depth != DONT_REMOVE_CURRENT_LINES:
            keep_lines.append(self.config.section_replace_with)
        return "\n".join(keep_lines)



