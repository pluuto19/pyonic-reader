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
    break_points = {}
    bold_font = fitz.Font("courier-bold")
    norm_font = fitz.Font("courier")
    pdf_doc = fitz.open(inpLoc)
    space_width = 20.0
    
    for page in pdf_doc:
        page_words = []
        for word in page.get_text("words"):
            page_words.append(word)
            white_rect = fitz.Rect(word[:4])
            page.add_redact_annot(white_rect, "", fill=(1,1,1), cross_out=False)
        page.apply_redactions()
        
        last_word_end = None
        for i in range(len(page_words)):
            word = page_words[i]
            x0, y0, text = word[0], word[1], word[4]
            bold_str = text[:3]
            norm_str = text[3:]
            if not last_word_end: #first word of the line
                print("first word of line")
                last_word_end = (x0 + bold_font.text_length(bold_str, 11) + norm_font.text_length(norm_str, 11) ,y0) #end coord of this first word
                print(last_word_end[0], last_word_end[1])
                last_y = y0
                page.insert_text((x0, y0), bold_str, fontsize=11, fontname="courier-bold", color=(0,0,0))
                page.insert_text((x0+bold_font.text_length(bold_str, 11), y0), norm_str, fontsize=11, fontname="courier", color=(0,0,0))
            else: # some other word of the line which will use last_word_end and update it
                this_x0 = last_word_end[0] + space_width
                #if this_x0 + bold_font.text_length(bold_str, 11) + norm_font.text_length(norm_str, 11) >= page.rect[2]:   
                page.insert_text((this_x0, y0), bold_str, fontsize=11, fontname="courier-bold", color=(0,0,0))
                page.insert_text((this_x0 + bold_font.text_length(bold_str, 11), y0), norm_str, fontsize=11, fontname="courier", color=(0,0,0))
                last_word_end = (this_x0 + bold_font.text_length(bold_str, 11) + norm_font.text_length(norm_str, 11), y0)
                if i+1 < len(page_words) and page_words[i+1][1] != y0:
                    last_word_end = None
                
    pdf_doc.save(outDir)

# resetting last_word_end to None by comparing current y to next y at the end of loop so when the itr starts, it is None
# if a word exceeds the page's boundary then take it to the next y with starting x position, if next y + text height is greater than page's y boundary then take it to next page. create a buffer to accomodate previous page's words
# if next y + word_height is not larger then page's y boundary then take it to the next word's y postion and x position
# keep updating last_word_end 