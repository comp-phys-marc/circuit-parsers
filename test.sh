# depth 2 width 2 circuits
for((i = 0; i <= 167; i++)); do
  python tool.py --input_file examples/gen/$i/circuit_$i.jpg
done