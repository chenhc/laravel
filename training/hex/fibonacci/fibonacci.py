#!/usr/bin/env python
# -*- encoding=utf8 -*-

import sys

if __name__ == '__main__':
	fib = [0, 1]
	for x in xrange(2, 100):
		fib.append(fib[x-1] + fib[x-2])

	while True:
		line = sys.stdin.readline()
		if not line:
			break
		n = int(line.strip())
		print fib[n]
