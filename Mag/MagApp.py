#!/usr/bin/env python2.7



import os,sys

from Magouilleuse import Magouilleuse
from MagIO import MagIO

#import psyco
#psyco.full()

def process_stdin () :
	magIO = MagIO( sys.stdin )
	magIO.readLines()
	mag = Magouilleuse()
	Res = mag.solve ( * magIO.getPeopleSlotsWishesIncapacitiesEqualities() )

	for p,j in Res :
		print("%s : %s"%( p, j ))



TIMER = 1
if __name__ == "__main__":
	if TIMER :
		from time import time
		t0 = time()
	process_stdin()
	if TIMER :
		print(time()-t0)
