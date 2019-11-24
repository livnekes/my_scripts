import argparse
import re

def main():
    parser = argparse.ArgumentParser("find regex in file")
    parser.add_argument("-f", dest = "file", help = "The name of the file")
    parser.add_argument("-r", dest = "regex_str", help = "The regex")
    args = parser.parse_args()

    f = open(args.file, "r")
    fl = f.readlines()
    for x in fl:
        if re.search(re.escape(args.regex_str), x):
            print x
if __name__== "__main__":
    #python test.py -f cube_solver.py
    main()