#!/bin/python

import obspy as ob
import glob
import matplotlib.pyplot as plt

files = glob.glob('*.RESP')
files.sort()

for file in files:
	outf = file.replace('.RESP', '.png')
	try:
		inv  = ob.read_inventory(file)
	except:
		continue
	resp = inv[0][0][0].response

	fig, (ax1, ax2) = plt.subplots(2)
	ax              = list([ax1,ax2])

	resp.plot(0.1, output="VEL", axes=ax, show=False)

	fig.suptitle(file)
	ax[0].grid(b=True, which='major', color='k', linestyle='--',linewidth=0.25)
	ax[1].grid(b=True, which='major', color='k', linestyle='--',linewidth=0.25)
	ax[0].grid(b=True, which='minor', color='k', linestyle='--',linewidth=0.25)
	ax[1].grid(b=True, which='minor', color='k', linestyle='--',linewidth=0.25)
	fig.savefig(outf)


