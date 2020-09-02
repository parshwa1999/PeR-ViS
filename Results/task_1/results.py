#
# File to load user results for Task 1 of the Semantic Search challenge 
#
#	SD, 2018/07/23		Initial effort
#

import csv
import os

#
# Load the results. These should be stored as a CSV file
# \param filename 		the file that contains the results
# \return 				loaded results, as a list of dictionary items. Each dictionary
#						is the results for a single query
#
def load_results(filename):
	rows = []

	csv_file = csv.DictReader(open(filename, 'r'), skipinitialspace=True, delimiter=',')
	for r in csv_file:
		rows.append(r)

	return rows
