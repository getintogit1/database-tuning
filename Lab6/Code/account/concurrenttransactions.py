#!/usr/bin/python

# for P6 consider using wraps from the functools module to wrap a transaction

from concurrent.futures import ThreadPoolExecutor, wait
import time
import argparse
import random

def transaction(transactionid):
  print 'transaction {} started'.format(transactionid)
  time.sleep(int(random.random() * 100.0) / 1000.0)
  print 'transaction {} terminated'.format(transactionid)

parser = argparse.ArgumentParser()

parser.add_argument('-t', '--numthreads', type=int, default=1)
parser.add_argument('-c', '--maxconcurrent', type=int, default=1)

args = parser.parse_args()

numthreads = args.numthreads
maxconcurrent = args.maxconcurrent

with ThreadPoolExecutor(max_workers=maxconcurrent) as executor:
  futures = { executor.submit(transaction, i): i for i in xrange(numthreads) }
  wait(futures)
