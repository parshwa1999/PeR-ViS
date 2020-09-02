#
# File to do the actual evaluation, will compare a ground truth data to a set of results
# and output some info on how well it worked
#
#	SD, 2018/07/23		Initial effort
#

import results
import ground_truth

def FindResult(results, query_id):
	for r in results:
		if (int(r['query_id']) == query_id):
			return r

	return None;

def Rank(gt, r):
	for key in r:
		if (r[key] == gt[1]):
			return int(key)

	return -1

def GetCMC(rank):
	cmc = []
	for i in range(len(rank)):
		count = 0
		for j in range(len(rank)):
			if (rank[j] <= (i +1)):
				count = count + 1

		cmc.append(count)

	return cmc		

def Evaluate(results, ground_truth):

	rank = []

	fail = len(ground_truth);
	for gt in ground_truth:

		r = FindResult(results, gt[0])
		if (r is not None):
			rank.append(Rank(gt, r))
		else:
			rank.append(fail)

	return rank