import argparse, fitz
def printhelp():
    args = argparse.ArgumentParser(description="A CLI based tool to bolden the initial words in a PDF.")
    args.add_argument("-r", type=str, help="A comma separated string to specify the ratio in which word of length N get their M initial words bolded.\nFor example, the string '3:1,4:2,5:2,6:3' boldens the first letter of a 3 len word, 2 letters of a 4 and 5 len word, 3 letters of 6 len word.")
    args.add_argument("-f", type=str, help="<Address of the PDF file>")
    args.add_argument("-d", type=str, help="<Address of the output directory>\\<name>.pdf")
    cli_args = args.parse_args()
    if cli_args.r is not None and cli_args.f is not None and cli_args.d is not None:
        convertPdf(cli_args.r, cli_args.f, cli_args.d)
    else:
        print("All arguments are needed for the conversion process.\nPlease run 'pyoreadr'.")
        args.print_help()

def convertPdf(ratioStr, inpLoc, outDir):
    pdf_doc = fitz.open(inpLoc)
    for page in pdf_doc:
        for word in page.get_text("words"):
            white_rect = fitz.Rect(word[:4])
            page.add_redact_annot(white_rect, "", fill=(1,1,1), cross_out=False)
        page._apply_redactions(images=0, graphics=0, text=0)
    pdf_doc.save(outDir)
    #r = fitz.Rect(w[:4])
    #for page in pdf_doc:
    
    #go thru each page
    #go thru each page's word
    #get each words bbox (make rect from it) and its characteristics
    #get each word's text string, if its not bold then get the initial letters and make them bold
    # get word -> bbox -> rect 