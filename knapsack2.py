# Phillip Stewart
# I think this was a codeEval challenge and I adapted an old script for it..

import sys

def brute(items, capacity):
	# Runs through all valid selections and selects best
	# sorts by weight, and then
	# uses index list of 1s and 0s to select items
	# adds lightest first, then index list is incremented
	# when weight goes over, some jenga inrementation is used
	# to save some unnecessary checking
	# for example, upon reaching an item larger than the capacity,
	# no more incrementing is done, as all valid have been checked
	#  -it's sloppy, but the logic is sound
	
	item_count = len(items)

	items.sort(key=lambda x: x[1], reverse=True)

	indy = [0]*item_count
	indy[-1] = 1
	taken = [0]*item_count
	best_v = 0
	
	ticking = True
	while(ticking):
		weight = 0
		value = 0
		for i in range(item_count):
			if indy[i] == 1:
				weight += items[i][1]
				value += items[i][2]
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

	packed_items = []
	for i in xrange(len(taken)):
		if taken[i] == 1:
			packed_items.append(items[i][0])
	
	return sorted(packed_items)


def unfuck(line):
	X, junk = line.strip().split(':')
	capacity = int(X)
	items = []
	for thing in junk.strip('() ').split(') ('):
		a,b,c = thing.split(',')
		a = int(a)
		b = float(b)
		c = int(c.strip('$'))
		items.append( (a,b,c) )
	return capacity, items


def main(args):
	if len(args) != 2:
		print 'Usage ~$ ' + args[0] + ' filename.txt'
		sys.exit(0)
	else:
		filename = args[1]
		
	with open(filename, 'r') as f:
		for line in f:
			if len(line) < 8:
				continue
			
			capacity, items = unfuck(line)
			nums = brute(items, capacity)
			if nums:
				print ','.join([str(x) for x in nums])
			else:
				print '-'


if __name__ == "__main__":
	main(sys.argv)
