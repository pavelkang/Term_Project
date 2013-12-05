with open("Ho-Oh.egg") as infile:
    with open("hooh.egg","w") as outfile:
        for i,line in enumerate(infile):
            if "TRef" in line and "D" in line:
                pass # do not copy that
            else:
                outfile.write(line)
