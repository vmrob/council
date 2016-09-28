#!/usr/bin/env python

import os
import argparse
import binascii
import shutil

parser = argparse.ArgumentParser()

parser.add_argument('input', help='file to split')
parser.add_argument('-n', '--num-members', type=int, default=3, help='number of members')
parser.add_argument('-p', '--parity', type=int, default=0, help='allowed missing parties')
parser.add_argument('-o', '--output-directory', default='out', help='output directory')
args = parser.parse_args()

contents = bytearray()
with open(args.input, 'rb') as f:
    contents = bytearray(f.read())

pieces = []
for i in range(args.num_members - 1):
    pieces.append(bytearray(os.urandom(len(contents))))

final_piece = bytearray()
for t in zip(contents, *pieces):
    val = 0
    for i in t:
        val ^= i
    final_piece.append(val)

pieces.append(final_piece)

out_path = args.output_directory
if not os.path.exists(out_path):
    os.makedirs(out_path)

for i in range(args.num_members):
    member_path = os.path.join(out_path, 'member-{}'.format(i))
    member_pieces = [(i + j) % args.num_members for j in range(args.parity + 1)]
    shutil.rmtree(member_path)
    os.makedirs(member_path)
    print('member {} will hold pieces {}'.format(i, member_pieces))
    for p in member_pieces:
        with open(os.path.join(member_path, '{}'.format(p)), 'wb') as f:
            f.write(pieces[p])

print('validating...')

original_contents = ''
for t in zip(*pieces):
    val = 0
    for i in t:
        val ^= i
    original_contents += chr(val)

assert(original_contents == contents)

print('done!')
