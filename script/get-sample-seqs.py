
import sys, random

USAGE = """
python script/get-sample-numbers.py sample_size total_population
"""

if __name__ == '__main__':
    sample_size = int(sys.argv[1])
    total_population = int(sys.argv[2])

    sample_seqs = random.sample(range(total_population), sample_size)
    for seq in sorted(sample_seqs):
        print(seq)