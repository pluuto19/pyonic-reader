import argparse    
def printhelp():
    args = argparse.ArgumentParser(description="A CLI based tool to bolden the initial words in a PDF.")
    args.add_argument("-r", type=str, help="A comma separated string to specify the ratio in which word of length N get their M initial words bolded.\nFor example, the string '3:1,4:2,5:2,6:3' boldens the first letter of a 3 len word, 2 letters of a 4 and 5 len word, 3 letters of 6 len word.")
    args.add_argument("-f", type=str, help="Address of the PDF file.")
    args.add_argument("-d", type=str, help="Address of the output directory.")
    if args.parse_args().r is None:
        args.print_help()
    else:
        print("hello world")