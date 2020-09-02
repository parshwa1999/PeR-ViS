#
# File to load user results for Task 2 of the Semantic Search challenge 
#
#	SD, 2018/06/18		Initial effort
#

import csv
import os

#
# Load a file for a single sequence
# \param filename 		the file that contains the sequence to load
# \return 				loaded sequence, as a list of dictionary items
#
def ParseSequence(filename):
	rows = []

	csv_file = csv.DictReader(open(filename, 'r'), skipinitialspace=True, delimiter=',')
	for r in csv_file:
		rows.append(r)

	return rows

#
# Load all results for a sequence
# \param path 			path to the data
# \param num_subjects	the number of subjects to grab data for
# \return 				a list of loaded sequences
#
def ParseResults(path, num_subjects):
	data = []

	for i in range(num_subjects):
		data.append(ParseSequence(os.path.join(path, str(i).zfill(3) + '.txt')))

	return data

def GetResultsForFrame(results, frame_id):
	for i in results:
		if (int(i['frame']) == int(frame_id)):
			return i

	return None
