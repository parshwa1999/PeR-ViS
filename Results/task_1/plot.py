import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pyplot

def cmc(rank, width=10, height=8, title="CMC Plot", save_loc="cmc.png"):
	fig = pyplot.figure()
	fig.set_size_inches(width, height)

	cmc = [float(r)/float(len(rank)) for r in rank]
	xaxis = range(0, len(cmc) + 1)
	cmc.insert(0, 0)

	pyplot.plot(xaxis, cmc)
	pyplot.ylim([0, 1.0])
	pyplot.title(title)
	pyplot.xlabel('Rank')
	pyplot.ylabel('Accuracy')

	fig.savefig(save_loc)

def cmcs(ranks, labels, width=10, height=8, title="CMC Plot", save_loc="cmc.png"):
	fig = pyplot.figure()
	fig.set_size_inches(width, height)

	for rank, l in zip(ranks, labels):
		cmc = [float(r)/float(len(rank)) for r in rank]
		xaxis = range(1, len(rank) + 1)
		pyplot.plot(xaxis, cmc, label=l)

	pyplot.ylim([0, 1.0])
	pyplot.title(title)
	pyplot.xlabel('Rank')
	pyplot.ylabel('Accuracy')

	fig.savefig(save_loc)
