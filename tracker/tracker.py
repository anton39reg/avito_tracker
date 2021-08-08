import sys
sys.path.insert(1, '../../parser')

from ..parser.urls_parser import parse
from ..diff.calculate_diff import calculate_diff


class Tracker:
    def __init__(self):
        self.history = {}

    def add(self, url):
        ads = parse(url)

        if ads['id'] not in self.history:
            self.history[ads['id']] = [ads]

    def update(self):
        updates = {}

        for item in self.history.values():
            last_info = parse(item[-1]['url'])
            diff = calculate_diff(last_info, item[-1])
            if diff:
                self.history[last_info['id']].append(last_info)
                updates[last_info['id']] = diff

        return updates

    def delete(self, url):
        ads = parse(url)
        self.history.pop(ads['id'], None)
