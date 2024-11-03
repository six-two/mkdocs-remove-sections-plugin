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
    section_heading_pattern = Type(str, default=r"Private: ")
    section_replace_with = Type(str, default="\n\n> Some content has been redacted in this version.\n\n")


class RemoveSectionsPlugin(BasePlugin[RemoveSectionsConfig]):
    def on_config(self, config: MkDocsConfig) -> None:
        self.start_tag = re.compile(self.config.section_start_pattern)
        self.end_tag = re.compile(self.config.section_end_pattern)

    def on_page_markdown(self, markdown, page, config, files):
        try:
            markdown = self.strip_sections_marked_with_tags(markdown, page.file.src_uri)

            # @TODO: check section stuff too

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



