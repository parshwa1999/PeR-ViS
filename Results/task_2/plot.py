import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pyplot

def results_for_sequence(data, sequence, width=10, height=8, title="", save_loc="sequence.png"):
	fig = pyplot.figure()
	fig.set_size_inches(width, height)

	frames = []
	iou = []
	for d in data:
		if (d['sequence'] == sequence):
			frames.append(d['frame'])
			iou.append(d['iou'])

	pyplot.plot(frames, iou)

	pyplot.ylim([0, 1.0])
	pyplot.title(title)
	pyplot.xlabel('Frame')
	pyplot.ylabel('IoU')

	fig.savefig(save_loc)

def all_sequences(data, width=10, height=8, title="", save_loc="all_sequences.png"):
	fig = pyplot.figure()
	fig.set_size_inches(width, height)

	iou = []
	for d in data:
		iou.append(d['average_IoU'])

	pyplot.bar(range(1, len(iou)+1), iou)

	pyplot.xlim([0.25, len(iou)+0.75])
	pyplot.ylim([0, 1.0])
	pyplot.title(title)
	pyplot.xlabel('Sequence')
	pyplot.ylabel('Average IoU')

	fig.savefig(save_loc)

def summary_by_difficulty(data, difficulty_ratings, width=10, height=8, title="", save_loc="sequences_by_difficulty.png"):
	fig = pyplot.figure()
	fig.set_size_inches(width, height)

	pyplot.ylim([0, 1.0])
	pyplot.title(title)
	pyplot.xlabel('Difficulty')
	pyplot.ylabel('Average IoU')

	fig.savefig(save_loc)
