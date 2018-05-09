#coding: utf-8

import ffmpeg
import sys, os
from mutagen.mp3 import MP3

def split_file(dirpath, filename):
    abspath = dirpath + filename
    size = os.path.getsize(abspath)

    print(f"Splitting file >> {filename}({size} bytes)")

    try:
        audio = MP3(abspath)
        size = audio.info.length
        print(f"\t\t{size}seconds... {int(size/3600)}hours {int((size%3600)/60)}mins {int(size%60)}secs")
    except Exception as e:
        print(e)
        return


    min10 = 10 * 60 #seconds
    seek = 0
    index = 1
    path, ext = os.path.splitext(filename)

    while seek < size:
        if size - seek < min10:
            duration = int(size - seek)
        else:
            duration = min10
        output = f"{path}_{index}{ext}"

        print(f"\tNo.{index} \n\tffmpeg -ss {seek} -i {dirpath+filename}\n\t\t-t {duration} {dirpath+output}")

        (ffmpeg
            .input(dirpath+filename)
            .output(dirpath+output, ss=seek, t=duration)
            .run()
        )

        seek += min10
        index += 1
    return


def main(file_or_directory_name=""):
    if os.path.isfile(file_or_directory_name):
        head, tail = os.path.split(file_or_directory_name)
        head += '/'
        split_file(head, tail)
    else:
        files = os.listdir(file_or_directory_name)
        if file_or_directory_name[-1] != '/':
            file_or_directory_name += '/'
        for f in files:
            if os.path.isfile(file_or_directory_name+f): #再帰処理は行いません
                split_file(file_or_directory_name, f)

                
if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    #arg1: Filename should be 'split_file'
    #arg2: Directory name or file name

    if argc != 2:
        print(f"Usage: {argvs[0]}")
        print("\t1 argument missing.")
        print("\tFilename or directory name are required.")
        quit()
    else:
        print("Program start.")
        main(argvs[1])
        print("Program finish.")
