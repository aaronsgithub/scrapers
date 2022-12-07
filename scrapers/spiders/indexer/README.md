# Spider: indexer

A basic spider which will index an entire website and download its http response body content (usually the HTML of the website but this depends on the response content-type).

## Usage

From anywhere inside the project root, user the command:
```bash
$ scrapy crawl indexwebsite -a url <root-url-of-website>
```
It is important to provide the root url of the website and not any subpaths or
subdomains as the spider uses the root url to determine what pages to follow.

This allows us to set this dynamically, as opposed to the default way in scrapy which would be to hardcode the spider's `allowed_domains` class variable.

The spider will follow all internal links it finds on a website, starting from the given root url.

It will collect and store all external links but it will not crawl these links.

## Outputs

The DATA_DIR setting we introduced in project "settings.py" module provides a configurable location on the filesystem to store the spider output on the file system.

The scrapy docs encourage an ETL like pattern where you write a spider which extracts structured content out of this returned html and save that. However, with this spider, we are using more of a ELT approach where we are saving everything to the file system, and logging key meta data as described below.

All data captured by this spider is stored on the file system under the path "DATA_DIR/<root-url-of-website>" with the following hierarchy:
```
DATA_DIR
│
└── example.com
    |
    |   # directory named with MD5 hash of scraped url
    ├── c984d06aafbecf6bc55569f964148ea3  
    |   |
    |   |   # html file named with MD5 hash of http response body
    │   └── 84238dfc8092e5d9c0dac8ef93371a07.html 
    |
    ├── <... MD5 hash of other scraped page url ...>
    |
    |   # jsonlines log file of fields captured from each scraped page
    └── example.com.jsonl
```
We use the MD5 hash of each url the spider crawls as an identifier to create a directory.

Within that directory, we download the response body which contains the html retrieved from that url. As a filename we use the MD5 hash of the contents we are downloading as an identifier. That means that if we crawl the page again, we can check if the content has changed and only save the content when it has.

The use of hashes in file / directory names allows us to keep a flat directory structure relative to the tree like structure of a typical website, whilst also being able succinctly monitor for changes in content at a given url. We do not need these hashes to be cryptographically secure - MD5 is a fairly arbitrary choice here.

The <root-url-of-website>.jsonl file is a log file we append to each time the spider is run on that URL.

For each page that is crawled, it outputs the `Webpage` scrapy `Item` subclass defined in `scrapers.items.Webpage`.

We log metadata such as timestamps, request and reponse headers, as well as lists of internal and external links found for further analysis. The log maps back to the MD5 hash named folders and .html files so we can us the link data contained in the logs to rebuild the website tree hiearchy.