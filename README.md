# Council

Naive N of M encryption except that N is a theoretical maximum. Totally not secure.

## Usage

Use `split.py` to break a file into N component parts and then divide them among that many members. If robustness is desired, the parity flag (`-p`) can be used to ensure that each member has enough pieces that a maximum of [N - parity] members are required to reconstruct the original file. The output directory (`out` by default) will contain paths that each member is expected to keep.

Use `combine.py` to combine the components back together. Each argument to combine should be a file path to one of the pieces. Duplicate pieces are ignored (so long as their names haven't been altered). It's probably easiest to combine each member's parts into a single directory and then use shell globbing to pass the paths as arguments.

Example:
```
./split.py README.md --num-members 8 --parity 3
member 0 will hold pieces [0, 1, 2, 3]
member 1 will hold pieces [1, 2, 3, 4]
member 2 will hold pieces [2, 3, 4, 5]
member 3 will hold pieces [3, 4, 5, 6]
member 4 will hold pieces [4, 5, 6, 7]
member 5 will hold pieces [5, 6, 7, 0]
member 6 will hold pieces [6, 7, 0, 1]
member 7 will hold pieces [7, 0, 1, 2]
validating...
done!
```

README.md will be divided into 8 parts for 8 parties allowing the file to be reconstructed using only 5 of them.

To reconstruct...

```
./combine.py --out README.md out/**/*
```
