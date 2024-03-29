# TGM-ACC-2019
My Solution for the TGM Advent Coding Contest 2019 expert difficulty. Public version of this repository @ https://github.com/pdamianik/TGM-ACC-2019/.

## Adding custom input files

To Add your own input files you just need to add a .in file into the directory of the level you want to handle the input file

## Run
To get results either:
 - run the `main.py` in the root directory and enter the number of the level you want to execute:
 
 ```
 the/repository/location> python main.py
 Level: 0
 The output of level0
 ```
 
 - run the main() function of the main.py in the level folder from the root folder of this repository:
 
 ```
 the/repository/location> python
 >>> import sys
 >>> from importlib import reload
 >>> from levels.level0 import main
 >>> sys.modules["levels.level0.main"].main()
 The output of level0
 >>> reload(sys.modules["level.level0"])
 The output of the __init__.py file of level0
 <module 'levels.level0' from '/repo/location/levels/level0/__init__.py'>
 >>> reload(sys.modules["levels.level0.main"])
 <module 'levels.level0.main' from '/repo/location/levels/level0/main.py'>
 >>> sys.modules["levels.level0.main"].main()
 The output of level0
 ```
 
The results will then be written to the `.out` files in the level directory with the same name as there corresponding `.in` files (e.g. `example.in` -> `example.out`).
