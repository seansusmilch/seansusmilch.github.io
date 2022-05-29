#! /usr/bin/python
from pathlib import Path
from datetime import datetime
import yaml
import re

title = input('Enter title: ')
title_sani = re.sub(r"\W+", "", title.strip().lower().replace(" ","_"))

now = datetime.now()
new_filename = f'_posts/{now.strftime("%Y-%m-%d")}-{title_sani}.md'

header = {
    'title': title,
    'date': now.strftime('%Y-%m-%d %H:%M:%S'),
    'categories': [],
    'tags': [],
}

with open(new_filename, 'x') as f:
    f.write(f'---\n{yaml.dump(header, sort_keys=False)}---\n\n')
    f.close()

print(f'CREATED "{title}" at {new_filename}')