#
# Main file to control everything
#
#	SD, 2018/07/15		Initial effort
#	SD, 2018/07/26		Add Task 1
#	SD, 2018/08/20		Added main, and all that stuff
#						Store output in a file, rather than print to screen
#

import csv
import os
import argparse

import task_2.eval as t2_eval
import task_2.ground_truth as t2_gt
import task_2.results as t2_results
import task_2.plot as t2_plot

import task_1.eval as t1_eval
import task_1.ground_truth as t1_gt
import task_1.results as t1_results
import task_1.plot as t1_plot

#
# Task 1
#
# 	\param groundtruth_file		The xml file with the ground truth (use 'sample_data/GT.xml' for the sanity check)
# 	\param results_file		This is the results .txt file (use 'sample_data/results_1.txt' or 'sample_daata/results_2.txt' or your own txt file for the sanity check)
#	\param output_path 		MAH - Not in use (20180730)
# 	\param prefix			MAH - Not in use (20180730)	
def RunEval_Task1(groundtruth_file, results_file, output_path = '.', prefix = ''):
	# load in the ground truth from the xml
	gt = t1_gt.ParseGroundTruth(groundtruth_file)

	# load in the results data from the txt file - CSV
	user_data = t1_results.load_results(results_file)

	# calculate the desired results.
	results = t1_eval.Evaluate(user_data, gt)
	cmc = t1_eval.GetCMC(results)

	t1_plot.cmc(cmc, save_loc=prefix + '-cmc.png')

	f = open(os.path.join(output_path, prefix + '-cmc.txt'), 'w')
	for i in cmc:
		f.write(str(i) + '\n')
	f.close()

	f = open(os.path.join(output_path, prefix + '-rank.txt'), 'w')
	for i in results:
		f.write(str(i) + '\n')
	f.close()

#
# Function to run the eval for task 2. Will load database and results, compute metrics, and dump results to
# a file
#	\param database_path		path to the database
#	\param database_main_file	main file for the datbase
#	\parma results_path			where the results files are located
#	\param num_sequences		number of test sequences, used to guide loading of the results
#	\param output_path			path to write outputs to
#	\param prefix				prefix to append to metrics that are written
#
def RunEval_Task2(database_path, database_main_file, results_path, num_sequences, output_path = '.', prefix = ''):
	# load ground truth
	subjects = t2_gt.ParseDatabase(database_main_file, database_path)

	# load results
	user_data = t2_results.ParseResults(results_path, num_sequences)

	# do eval
	eval_results = t2_eval.EvaluateDataset(subjects, user_data)
	# and get the metrics, use IoU = 0.4, so just leave this as default
	frame_results, sequence_results, metrics = t2_eval.GenerateMetrics(eval_results)

	keys_frame = frame_results[0].keys()
	#print('keys_frame',frame_results)
	keys_sequence = sequence_results[0].keys()
	keys_metrics = metrics.keys()

	t2_plot.all_sequences(sequence_results, save_loc=prefix + 'sequennce_results.png')

	with open(os.path.join(output_path, prefix + 'frame_results.txt'), 'w') as csv_out:
		dict_writer = csv.DictWriter(csv_out, keys_frame)
		dict_writer.writeheader()
		dict_writer.writerows(frame_results)

	with open(os.path.join(output_path, prefix + 'sequence_results.txt'), 'w') as csv_out:
		dict_writer = csv.DictWriter(csv_out, keys_sequence)
		dict_writer.writeheader()
		dict_writer.writerows(sequence_results)

	with open(os.path.join(output_path, prefix + 'overall.txt'), 'w') as csv_out:
		dict_writer = csv.DictWriter(csv_out, keys_metrics)
		dict_writer.writeheader()
		dict_writer.writerow(metrics)

def Main():

	parser = argparse.ArgumentParser(description='AVSS 2018 Semantic Search Challenge Eval Tool.')
	parser.add_argument('--mode', dest='mode', type=int, help='what eval are we doing? Task 1 (1), or Task 2 (2)? Anything else here is wrong.')

	# task 1 arguments
	parser.add_argument('--t1_groundtruth', dest='t1_groundtruth', action='store', help='ground truth file for task 1')
	parser.add_argument('--t1_results_file', dest='t1_results_file', action='store', help='results file for task 1')
	parser.add_argument('--t1_output_path', dest='t1_output_path', action='store', help='output path for task 1 results', default='')
	parser.add_argument('--t1_prefix', dest='t1_prefix', action='store', help='what to prepend output file with', default='')

	# task 2 arguments
	parser.add_argument('--t2_database_path', dest='t2_database_path', action='store', help='path to database for task 2')
	parser.add_argument('--t2_database_main_file', dest='t2_database_main_file', action='store', help='main XML file for the database')
	parser.add_argument('--t2_results_path', dest='t2_results_path', action='store', help='path to the results for task 2. Note that we expect these in a certain format')
	parser.add_argument('--t2_num_sequences', dest='t2_num_sequences', type=int, help='number of sequences in the database', default=41)
	parser.add_argument('--t2_output_path', dest='t2_output_path', action='store', help='output path for task 2 results', default='')
	parser.add_argument('--t2_prefix', dest='t2_prefix', action='store', help='what to prepend output file with', default='')

	args = parser.parse_args()

	if (args.mode == 1):
		RunEval_Task1(args.t1_groundtruth, args.t1_results_file, args.t1_output_path, args.t1_prefix)
	elif (args.mode == 2):
		RunEval_Task2(args.t2_database_path, args.t2_database_main_file, args.t2_results_path, args.t2_num_sequences, \
					  args.t2_output_path, args.t2_prefix)
	else:
		print('No, try again.')

if __name__ == "__main__":
    Main()
