#!/usr/bin/env python3
"""Check profile assets and optionally the published URLs; no dependencies."""
import ast
import concurrent.futures
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import urllib.request
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'img':
            assert attrs.get('alt','').strip(), 'Image missing meaningful alt text'
            self.refs.append(attrs['src'])
        elif tag == 'source':
            self.refs.append(attrs['srcset'])


def main():
    for name in ['README.md','SETUP.md','.github/workflows/snake.yml','assets/header.svg','assets/header-mobile.svg']:
        assert (ROOT/name).is_file(), name
    for path in (ROOT/'assets').rglob('*.svg'):
        root = ET.parse(path).getroot()
        assert root.tag == '{http://www.w3.org/2000/svg}svg', path
        assert root.get('viewBox'), path
        for element in root.iter():
            assert element.tag.rsplit('}',1)[-1] not in ('script','foreignObject'), path
            for key,value in element.attrib.items():
                assert not key.lower().startswith('on'), path
                if key.endswith('href'):
                    assert value.startswith('#'), f'External SVG resource: {path}'
    for path in (ROOT/'scripts').glob('*.py'):
        ast.parse(path.read_text())
    readme = (ROOT/'README.md').read_text()
    parser = Images()
    parser.feed(readme)
    for ref in parser.refs:
        if not ref.startswith('https://'):
            assert (ROOT/ref).is_file(), ref
    for tag in ['table','tr','td','details','picture','p']:
        assert len(re.findall(fr'<{tag}(?:\s|>)',readme)) == readme.count(f'</{tag}>'), f'Unbalanced {tag}'
    print(f'PASS: {len(parser.refs)} images/sources, SVG structure and safety, local references, HTML balance, Python syntax')
    if '--network' in sys.argv:
        urls = set(re.findall(r'https://[^\s<>"\)]+',readme))
        def check(url):
            url = unescape(url)
            request = urllib.request.Request(url,headers={'User-Agent':'profile-link-check'})
            with urllib.request.urlopen(request,timeout=30) as response:
                data=response.read()
                assert response.status == 200 and data, url
                if '.svg' in url or 'komarev.com' in url:
                    assert ET.fromstring(data).tag == '{http://www.w3.org/2000/svg}svg', url
            return url
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            for url in pool.map(check,sorted(urls)):
                print('PASS:',url)


if __name__ == '__main__':
    main()
