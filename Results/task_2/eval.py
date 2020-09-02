#
# File to do the actual evaluation, will compare a ground truth data to a set of results
# and output some info on how well it worked
#
#	SD, 2018/06/18		Initial effort
#	SD, 2018/06/19		more coding
#	SD, 2018/06/19		still going, I haven't had much time, added some comments too
#	2D, 2018/07/15		finally got back to this, added a missing return
#

import results
import ground_truth

#
# get the intersection between two bounding boxes. I'm sure that somewhere in python there's a box object
# and all the associated stuff, but the wifi is crap and it's easy to write somethign to do it
#	\param box_a	the first bounding box
#	\param box_b	the second bounding box
#	\return 		the intersection of box_a and box_b, note that this function will not test is this is a
#					valid box or not (i.e left <= right, top <= bottom), so something else should do that
#
def Intersection(box_a, box_b):
	intersection = {}
	intersection['left'] = max(float(box_a['left']), float(box_b['left']))
	intersection['top'] = max(float(box_a['top']), float(box_b['top']))
	intersection['bottom'] = min(float(box_a['bottom']), float(box_b['bottom']))
	intersection['right'] = min(float(box_a['right']), float(box_b['right']))
	return intersection

#
# get the area of a box
#	\param box 		the bounding box to look at
#	\return 		area of the box, i.e., width*height
#
def Area(box):
	if((float(box['left']) > float(box['right'])) | (float(box['top']) > float(box['bottom']))):
		return 0
	else:	
		return (float(box['right']) - float(box['left']) + 1)*(float(box['bottom']) - float(box['top']) + 1)

#
# get the intersection over union between the two boxes
#	\param box_a	the first bounding box
#	\param box_b	the second bounding box
#	\return 		the intersection over union of the two boxes
#
def IoU(box_a, box_b):
	#print('BOXA',box_a)
	#print('BOXB',box_b)
	intersect = Area(Intersection(box_a, box_b))
	return (intersect/(Area(box_a) + Area(box_b) - intersect))

def GetBoundingBox(fhs):
	x_locs = [fhs['hx'], fhs['rfx'], fhs['lfx'], fhs['rsx'], fhs['lsx'], fhs['rnx'], fhs['lnx'], fhs['rwx'], fhs['lwx']]
	x_locs = [x for x in x_locs if x > 0]
	y_locs = [fhs['hy'], fhs['rfy'], fhs['lfy'], fhs['rsy'], fhs['lsy'], fhs['rny'], fhs['lny'], fhs['rwy'], fhs['lwy']]
	y_locs = [y for y in y_locs if y > 0]

	bb = {}
	bb['left'] = float(min(x_locs))
	bb['right'] = float(max(x_locs))
	bb['top'] = float(min(y_locs))
	bb['bottom'] = float(max(y_locs))

	return bb

#
# evaluate a sequence, i.e compare the ground truth to the results from a single sequence
#	\param gt_sequence 			the gt_sequence to compare
#	\param results_sequence		the results we are comparing to
#	\return						a list of dictionaries, each dict is a frame index and an iou
#
def EvaluateSequence(gt_sequence, results_sequence):
	frame_results = []

	for gt in gt_sequence:
		if gt['gt'] == 'true':
			#r = results.GetResultsForFrame(results_sequence, gt['idx'])
			for i in results_sequence:
				if (int(i['frame']) == int(gt['idx'])):
					#print('qq',i)
					r = i
					break
				else:
					r = None
			if (r is not None):
				#print('GETBB',GetBoundingBox(gt))
				frame_results.append({'frame' : gt['idx'], 'IoU': IoU(r, GetBoundingBox(gt))})
			else:
				frame_results.append({'frame' : gt['idx'], 'IoU' : 0})

	return frame_results

#
# Evaluate a whole dataaset, basically, run EvaluateSequence over all sequences
#	\param gt_sequences 		the ground truth sequences 
#	\param results_sequence 	the results sequences
#	\return 					a list of sequence results, i.e. a list of what's retruned by EvaluateSequence 
#
def EvaluateDataset(gt_sequences, results_sequence):
	results = []
	for gt, res in zip(gt_sequences, results_sequence):
		results.append(EvaluateSequence(gt, res))

	return results

#
# Get some metrics for a sequence, compute somethings like the average IoU, number of frames above
# a threshoold, and whatever else I decide to add
#	\param sequence 		sequence to get metrics for
#	\param iou_thresh 		the minimum IoU that we need to consider a 'match'
#	\returm 				a dictionary, that has the average IoU for the seqeunce, the percentage of frames above
#							the IoU threshold, and the number of observations
#
def MetricsForSequence(sequence, iou_thresh = 0.4):
	average_iou = 0
	iou_above_thresh = 0
	for s in sequence:
		average_iou += s['IoU']
		if (s['IoU'] >= iou_thresh):
			iou_above_thresh += 1.0

	return {'average_IoU' : average_iou/float(len(sequence)), 'percentage_above_thresh' : iou_above_thresh / float(len(sequence)), 'observations' : len(sequence)}

#
# Get metrics for the entire dataset, will compute metrics per sequence and overall metrics
# 	\param results 			the full set of results to evaluate
#	\param iou_thresh 		the minimum IoU that we need to consider a 'match'
#	\returns				a list of sequence results (see MetricsForSequence) and a dictionary (same entires as sequence results)
#							that captures the overall metrics
#
def GenerateMetrics(results, iou_thresh = 0.4):
	frame_results = []
	sequence_results = []
	overall_metrics = {}
	overall_metrics['average_IoU'] = 0
	overall_metrics['percentage_above_thresh'] = 0
	overall_metrics['observations'] = 0	

	s = 0
	for r in results:
		for f in r:
			frame_results.append({'sequence' : s, 'frame' : f['frame'], 'IoU' : f['IoU']})

		sr = MetricsForSequence(r, iou_thresh)
		overall_metrics['average_IoU'] += sr['average_IoU']
		overall_metrics['percentage_above_thresh'] += sr['percentage_above_thresh']*sr['observations']
		overall_metrics['observations'] += sr['observations']
		sequence_results.append(sr)

		s += 1

	overall_metrics['average_IoU'] /= len(sequence_results)
	overall_metrics['percentage_above_thresh'] /= overall_metrics['observations']

	return frame_results, sequence_results, overall_metrics
