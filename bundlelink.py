#!/usr/local/bin/python3

# 一括でsymlinkを貼る
# $ bundlelink ~/Garage/Toybox/toys/**/bin/* .
# みたいな感じでリンクを張る

import os
import glob
import sys
import argparse


def BundleLink(src_dir, dest_dir, permission, remove_extension):
	if 0 == permission:
		print('permission error')
		retrun

	for f in glob.iglob(os.path.join(src_dir, '*')):
		if os.access(f, permission):
			src = f
			if (remove_extension):
				srclist = src.rsplit('.', 1)
				src = srclist[0]

			dest = os.path.join(dest_dir, os.path.basename(src))
			print('make symlink:', f, '->', dest)
			os.symlink(f, dest)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='bundlelink : make many symlink in a lump.')
	parser.add_argument('src_dir', type=str)
	parser.add_argument('dest_dir', type=str)
	parser.add_argument('-a', 
			action='store_true', dest='permission_a',
			help='select any permission files.')
	parser.add_argument('-r','--readable', 
			action='store_true', dest='permission_r',
			help='select read enable files.')
	parser.add_argument('-w','--writable', 
			action='store_true', dest='permission_w',
			help='select write enable files.')
	parser.add_argument('-x','--executable', 
			action='store_true', dest='permission_x',
			help='select execute enable files.')
	parser.add_argument('--noextension', 
			action='store_true', dest='remove_extension',
			help='leave out extension from symlink name.')
	args = parser.parse_args();

	permission = 0
	if args.permission_r:
		permission |= os.R_OK
	if args.permission_w:
		permission |= os.W_OK
	if args.permission_x:
		permission |= os.X_OK
	if (args.permission_a) or (permission == 0):
		permission = os.R_OK | os.W_OK | os.X_OK
	remove_extension = args.remove_extension

	BundleLink(args.src_dir, args.dest_dir, permission, remove_extension)

