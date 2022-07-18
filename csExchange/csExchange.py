
import os
import sys
import traceback
try:
    from myClass import CrossSections
except Exception as e: # openpyxl not install
    print("\n", traceback.format_exception_only(type(e), e)[0])
    sys.exit()

def usage(err):

    basename = os.path.basename(__file__)
    msg = f"""
 Exchange the series of cross-section datas

  python {basename} [-h] [-from type path[!sheet] -to type path[!sheet]]

    type  : NK or CTI or MLIT or JSON
    path  : filename or directory*  *directory be allowed only case in type=MLIT 
    sheet : if use Excel workbook

 For example

  python {basename} -from CTI cti.xlsx!cti -to NK nk.xlsx

 CAUTION !!!  'openpyxl' must be installed."""

    if err != "":
        print(err, "\n\n", msg, file=sys.stderr)
        exit(1)
    else:
        print(msg, file=sys.stderr)
        exit(0)

def parseArgs(argv):

    i = 1; args_src = {}; args_dst = {}
    while i < len(argv):
        arg = argv[i]
        if   arg == "-h": usage("")
        elif arg == "-from":
            args = args_src
            i = i + 1; args["type"] = argv[i]
            i = i + 1; src = argv[i].split("!"); args["file"] = src[0]
            if len(src) == 2: args["sheet"] = src[1]
        elif arg == "-to":
            args = args_dst
            i = i + 1; args["type"] = argv[i]
            i = i + 1; dst = argv[i].split("!"); args["file"] = dst[0]
            if len(dst) == 2: args["sheet"] = dst[1]
        else:
            usage(f"\n ERROR unknown option {arg}")
        i += 1

    return (args_src, args_dst)

if __name__ == "__main__":

    try:
        args = parseArgs(sys.argv)
        obj = CrossSections(args[0])
        obj.export_to(args[1])
        print(f"\n Exchange from {args[0]['file']} to {args[1]['file']}.")
        if args[1]["type"] == "NK":
            print(f" Please each sheet copy to Q2DFNU.xlsm.")
        exit(0)
    except Exception as e:
        print("\n", traceback.format_exception_only(type(e), e)[0])
        exit(1)
