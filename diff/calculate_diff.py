import difflib as dl
import sys


def calculate_diff(a, b):
    return ''.join(list(dl.unified_diff(a, b)))


# if __name__ == '__main__':
#     print(calculate_diff(sys.argv[1], sys.argv[2]))
