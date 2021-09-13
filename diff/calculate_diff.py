import difflib as dl


class Diff:
    def __init__(self):
        self.info = {
            'url': None,
            'id': None,
            'status': '',
            'price': 0,
            'title': '',
            'description': '',
        }

    def __bool__(self):
        return (
            self.info['status'] != ''
            or self.info['price'] != 0
            or self.info['title'] != ''
            or self.info['description'] != ''
        )


def calculate_diff(cur, prev) -> Diff:
    diff = Diff()

    diff.info['url'] = cur['url']
    diff.info['id'] = cur['id']

    diff.info['description'] = ''.join(list(dl.unified_diff(cur['description'], prev['description'])))
    diff.info['title'] = ''.join(list(dl.unified_diff(cur['title'], prev['title'])))
    diff.info['status'] = ''.join(list(dl.unified_diff(cur['status'], prev['status'])))
    diff.info['price'] = cur['price'] - prev['price']

    return diff


# if __name__ == '__main__':
#     print(calculate_diff(sys.argv[1], sys.argv[2]))
