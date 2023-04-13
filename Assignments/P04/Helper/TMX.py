#https://pytiled-parser.readthedocs.io/_/downloads/en/latest/pdf/

#why do people program like this...
from pathlib import Path
import pytiled_parser


map_file = Path("../Levels/Test.tmx")
map = pytiled_parser.parse_map(map_file)

floor = map.layers[0].data
objects = map.layers[1].data

print(len(floor[0]))