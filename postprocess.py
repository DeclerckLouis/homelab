# https://pypi.org/project/mkdocs-ultralytics-plugin
from plugin import postprocess_site

if __name__ == "__main__":
    postprocess_site(
        site_dir="site",  # Your build output directory
        docs_dir="docs",  # Your source docs directory
        site_url="https://lab.packetflow.be",
        default_author="declerck.louis@outlook.com",
        add_desc=True,
        add_image=True,
        add_keywords=True,
        add_json_ld=True,
        add_share_buttons=True,
        add_css=True,
        verbose=True,
    )