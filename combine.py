#!/usr/bin/env python

import os
import argparse
import shutil

parser = argparse.ArgumentParser()

parser.add_argument('pieces', nargs=argparse.REMAINDER, help='pieces')
parser.add_argument('-o', '--out', default='', help='output filename (default stdout)')
args = parser.parse_args()

piece_paths = [p for p in args.pieces if os.path.isfile(p)]

max_seen = 0
paths = []

for path in piece_paths:
    piece_num = 0
    try:
        piece_num = int(os.path.basename(path))
    except ValueError:
        pass
    max_seen = max(max_seen, piece_num)
    while len(paths) < max_seen + 1:
        paths.append(None)
    if paths[piece_num] is None:
        paths[piece_num] = path

pieces = []
for path in paths:
    with open(path, 'rb') as f:
        pieces.append(bytearray(f.read()))

original_contents = ''
for t in zip(*pieces):
    val = 0
    for i in t:
        val ^= i
    original_contents += chr(val)

if not args.out:
    print(original_contents)
else:
    with open(args.out, 'wb') as f:
        f.write(original_contents)
