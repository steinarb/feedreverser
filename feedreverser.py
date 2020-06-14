#!/usr/bin/env python3
import os
import sys
import yaml
from dateutil import parser
import feedparser
from datetime import datetime, timezone
from feedgen.feed import FeedGenerator

def main():
    config_file = get_config_file()
    if not os.path.isfile(config_file):
        setup(config_file)

    config = read_config(config_file)
    feed = feedparser.parse(config['feed_url'])
    consumed = config['consumed']
    fg = FeedGenerator();
    fg.title('Reversed feed')
    fg.link(href='http://localhost/reversed', rel='alternate')
    fg.description('Snudd feed')
    for entry in reversed(feed.entries):
        if entry.id not in consumed:
            fe = fg.add_entry()
            fe.id(entry.id)
            fe.title(entry.title)
            fe.summary(entry.summary)
            for tag in entry.tags:
                if 'uncategorized' != tag.term.lower():
                    fe.category(term = tag.term)
            now = datetime.now(tz=timezone.utc)
            fe.pubDate(now)
            fe.updated(now)
            consumed.append(entry.id)
            break

    fg.rss_file(config['reversed_file'])
    save_config(config, config_file)

def get_config_file():
    if __name__ == "__main__" and len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = os.path.join(os.path.expanduser("~"), ".feedreverser")
    return config_file

def save_config(config, config_file):
    copy = dict(config)
    copy['updated'] = datetime.now(tz=timezone.utc).isoformat()
    with open(config_file, 'w') as fh:
        fh.write(yaml.dump(copy, default_flow_style=False))

def read_config(config_file):
    config = {}
    with open(config_file) as fh:
        config = yaml.load(fh)
    return config

def setup(config_file):
    feed_url = input('RSS/Atom feed URL to watch: ')
    reversed_file = input('Path to file to save the reversed feed: ')
    config = {
        'feed_url': feed_url,
        'reversed_file': reversed_file,
        'consumed': [],
    }
    save_config(config, config_file)

if __name__ == "__main__":
    main()
