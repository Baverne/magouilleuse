#!/usr/bin/env python2.7



import os,sys
import argparse
from Magouilleuse import Magouilleuse
from MagIO import MagIO


#import psyco
#psyco.full()

def process_stdin (file_path) :
	print("process_stdin")
	magIO = MagIO( open(file_path))
	print("MagIO created")
	magIO.readLines()
	print("MagIO readLines")
	mag = Magouilleuse()
	print("Magouilleuse created")
	Res = mag.solve ( * magIO.getPeopleSlotsWishesIncapacitiesEqualities() )
	print("Magouilleuse solved")

	for p,j in Res :
		print("%s : %s"%( p, j ))



TIMER = 1
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Process some folder path.")
	parser.add_argument("file_path", type=str, help="Path to the folder containing the input file")
	args = parser.parse_args()
	if TIMER :
		from time import time
		t0 = time()
	process_stdin(args.file_path)
	if TIMER :
		print(time()-t0)
