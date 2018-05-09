#coding: utf-8
import os, sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        quit()

    filepath = sys.argv[1]
    new_name = sys.argv[2]

    files = os.listdir(filepath)
