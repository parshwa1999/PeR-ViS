#
# File to load ground truth data for Task 1 of the Semantic Search challenge 
#
#	SD,	2018/07/23	 	Initial effort
#

import xml.etree.ElementTree as ET
import os

#
# Load the entire database. Will load the main file which will contain a list of 
# all other sequences, and will then load each sequence
#
#	\param mainfile		The xml file for the ground truth
#	\returns			loaded results, will be a list of tuples with the query number and
#						the correct matching query
#
def ParseGroundTruth(mainfile):
	tree = ET.parse(mainfile)
	root = tree.getroot()

	queries = []

	idx = 0
	for s in root.findall('Person'):
 		queries.append((idx, s.get('filename')))
 		idx += 1

	return queries
