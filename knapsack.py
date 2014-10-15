# Phillip Stewart
# I was doing some optimization algorithms online course and wrote this

#fiddlesticks

import time
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def brute(items, item_count, capacity):
	# Runs through all valid selections and selects best
	# sorts by weight, and then
	# uses index list of 1s and 0s to select items
	# adds lightest first, then index list is incremented
	# when weight goes over, some jenga incrementation is used
	# to save some unnecessary checking
	# for example, upon reaching an item larger than the capacity,
	# no more incrementing is done, as all valid have been checked
	#  -it's sloppy, but the logic is sound
	
	start = time.time()
	opt = 1

	items.sort(key=lambda x: x[2], reverse=True)

	indy = [0]*item_count
	indy[-1] = 1
	taken = [0]*item_count
	best_v = 0
	
	ticking = True
	while(ticking):
		if time.time() - start > 10:
			opt = 0
			break
		weight = 0
		value = 0
		for i in xrange(item_count):
			if indy[i] == 1:
				weight += items[i].weight
				value += items[i].value
		if weight <= capacity:
			if value > best_v:
				taken = indy[:]
				best_v = value
			#uptick regularly
			tick = len(indy) - 1
			while indy[tick] == 1:
				if tick == 0:
					ticking = False
					break
				tick -= 1
			indy[tick] = 1
			while tick < len(indy) - 1:
				tick += 1
				indy[tick] = 0
		else:
			#play jenga
			if indy.count(1) == 1:
				ticking = False
			else:
				tick = len(indy) - 1
				hit = False
				while tick >= 0:
					if tick == 0:
						ticking = False
						break
					elif indy[tick] == 1:
						if hit:
							while indy[tick] == 1:
								if tick == 0:
									break
								tick -= 1
							indy[tick] = 1
							while tick < len(indy) - 1:
								tick += 1
								indy[tick] = 0
							break
						else:
							hit = True
					tick -= 1

	solind = [0]*item_count
	for i in xrange(item_count):
		if taken[i] == 1:
			solind[items[i][0]] = 1

	# prepare the solution in the specified output format
	output_data = str(best_v) + ' ' + str(opt) + '\n'
	output_data += ' '.join(map(str, solind))
	return output_data


def zero_one_shuffle(indy):
	i = len(indy) - 1
	while indy[i] == 1:
		if i == 0:
			return 0, []
		i -= 1
	while indy[i] == 0:
		if i == 0:
			return 0, []
		i -= 1
	indy[i] = 0
	i += 1
	indy[i] = 1
	return i, indy
	
	
def prunes(items, item_count, capacity):
	# The approach here is to sort by value/weight
	# then add most value dense items
	# A binary tree is simulated using index list of 1s or 0s
	# A first run is conducted to get a baseline best_value
	# from there, we can check the best possible
	# outcome for each node we encounter, and 'prune' any sub-trees
	# that will not exceed our current best solution
	
	items.sort(key=lambda x: (float(x[1]) / float(x[2]), x[1]), reverse=True)
	
	start = time.time()
	opt = 1	
	
	indy = [0] * item_count
	weight = 0
	val = 0
	
	for i in xrange(item_count):
		if weight + items[i][2] <= capacity:
			weight += items[i][2]
			val += items[i][1]
			indy[i] = 1
	
	best_v = val
	best = indy[:]

	curr, indy = zero_one_shuffle(indy)
	
	crawling = True
	while crawling:
		if not indy:
			break

		weight = 0
		val = 0
	
		#check max possible at node
		#get weight & val up to node
		for i in xrange(curr):
			if indy[i] == 1:
				weight += items[i][2]
				val += items[i][1]
	
		#calc below node
		ratio = float(capacity - weight) / float(items[curr][2])
		max_poss = ratio * items[curr][1] + val
		if max_poss > best_v:
			#traverse sub-tree
			for i in xrange(curr, item_count):
				if weight + items[i][2] <= capacity:
					weight += items[i][2]
					val += items[i][1]
					indy[i] = 1
				else:
					indy[i] = 0
			if val > best_v:
				best_v = val
				best = indy[:]
		else:
			#prune
			for i in xrange(curr, item_count):
				indy[curr] = 1

		curr, indy = zero_one_shuffle(indy)
					
		if time.time() - start > 3600:
			opt = 0
			break

	b3 = 0
	solind = [0]*item_count
	for i in xrange(item_count):
		if best[i] == 1:
			b3 += items[i][1]
			solind[items[i][0]] = 1
	
	# prepare the solution in the specified output format
	output_data = str(b3) + ' ' + str(opt) + '\n'
	output_data += ' '.join(map(str, solind))
	return output_data


def solve_it(input_data):
	# parse the input
	lines = input_data.split('\n')
	firstLine = lines[0].split()
	item_count = int(firstLine[0])
	capacity = int(firstLine[1])
	items = []
	for i in range(1, item_count+1):
		line = lines[i]
		parts = line.split()
		items.append(Item(i-1, int(parts[0]), int(parts[1])))

#	for item in items:
#		print item

#	t1 = time.time()*1000
#	brute_solution = brute(items, item_count, capacity)
#	print brute_solution
#	print 'Brute: ', time.time()*1000 - t1

#	t1 = time.time()*1000
#	prune_solution = prunes(items, item_count, capacity)
#	print prune_solution
#	print 'Prune: ', time.time()*1000 - t1
	
	return prunes(items, item_count, capacity)
#	return prune_solution


import sys

if __name__ == '__main__':
	if len(sys.argv) > 1:
		file_location = sys.argv[1].strip()
		input_data_file = open(file_location, 'r')
		input_data = ''.join(input_data_file.readlines())
		input_data_file.close()
		print solve_it(input_data)
	else:
		print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

