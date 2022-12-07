# Scrapers

This repository is a container for some generic web scraping resources pulled from other projects I've worked on.

The code uses the Python based [Scrapy](https://docs.scrapy.org/en/latest/topics/settings.html) web scraping framework.

The codebase structure was generated with the built in Scrapy commands:

    $ scrapy startproject scrapers

with some minor changes described below.

### settings.py
```python
import pathlib

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent

# We use this to store output from our spiders.
DATA_DIR = PROJECT_ROOT / "data"

SPIDER_DIR = PROJECT_ROOT / "scrapers" / "spiders"

BOT_NAME = "scrapers"

# We alter this so we can put each spider in its own directory so we can store a README
# with easy to reach usage instructions beside it.
SPIDER_MODULES = []
for dir in SPIDER_DIR.iterdir():
    # get all meaningful directories in the spiders directory
    if dir.is_dir() and dir.name != "__pycache__":
        # format them as "scraping.spiders.<dirname>" string as SPIDER_MODULES spec requires
        # using pathlib parts attribute:
        SPIDER_MODULES.append(".".join(dir.parts[-3:]))
```
Here we use an approach similar to the [django project](https://www.djangoproject.com/) to define various project directories in the settings using Python's `pathlib` library, that can be used throughout the codebase.

In particular, we have defined a `DATA_DIR` to provide a default directory to store output of our spiders on the filesystem.

We have also changed the default location for each spider so that a spider is contained in its own subdirectory as a container to group together spider specific code and documentation.


### middlewares.py

Changes introduced here:

- `RequestTimestampMiddleware` adds a timestamp to each `request` object produced by our spiders. This is useful for monitirong for changes to a webpage over time.


## Spiders

Each spider in this repository is contained in its own subdirectory within the `scrapers/spiders/` directory.

Contents:

- [`indexer`](https://github.com/aaronsgithub/scrapers/tree/main/scrapers/spiders/indexer) a generic website indexer.
