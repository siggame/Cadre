import argparse

parser = argparse.ArgumentParser(description='Shows how to generate k-mean for clustering using a gamelog')
parser.add_argument('gamelog_path', action='store', help='the path to a gamelog to generate k-means for.')

args = parser.parse_args()

import grappe

k = grappe.parse(args.gamelog_path)

print("Calculated k-means for gamelog:", k)
