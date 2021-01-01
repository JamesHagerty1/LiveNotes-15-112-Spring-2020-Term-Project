# various math symbol characters from:
# https://www.rapidtables.com/math/symbols/Basic_Math_Symbols.html
# replaces 'aprx' on a page with '≈':
def findAprx(page, row):
    for i in range(len(page[row])):
        if page[row][i] == None:
            continue
        # determines that 'aprx' is there for the edges of the page
        if (page[row][0] != None and page[row][1] != None and
            page[row][2] != None and page[row][3] != None):
            # all capital/lowecase letter spellings of 'aprx' count
            if (page[row][0][0].lower()=='a' and 
                page[row][1][0].lower()=='p' and
                page[row][2][0].lower()=='r' and
                page[row][3][0].lower()=='x' and
                (page[row][4]==None or page[row][4][0]==' ')):
                page[row][1]='≈'+page[row][i+3][1:]
                page[row][0]=' '+page[row][i][1:]
                page[row][2]=' '+page[row][i+2][1:]
                page[row][3]=' '+page[row][i+1][1:]
        # determines that 'aprx' is there to swap with '≈'
        if (page[row][i][0].lower() == 'a' and not i+3 > 55 and
            not i-1 < 0):
            if page[row][i+1]==None: 
                continue
            elif (page[row][i+1][0].lower()=='p' and
                  page[row][i+2][0].lower()=='r' and
                  page[row][i+3][0].lower()=='x' and                  
                  (page[row][i-1]==None or page[row][i-1][0]==' ' )):
                page[row][i]='≈'+page[row][i+3][1:]
                page[row][i+1]=' '+page[row][i+1][1:]
                page[row][i+2]=' '+page[row][i+2][1:]
                page[row][i+3]=' '+page[row][i][1:]

# replaces 'root' on a page with '√'
def findRoot(page, row):
    for i in range(len(page[row])):
        if page[row][i] == None:
            continue
        # determines that 'root' is there for the edges of the page
        if (page[row][0] != None and page[row][1] != None and
            page[row][2] != None and page[row][3] != None):
            # all capital/lowecase letter spellings of 'root' count
            if (page[row][0][0].lower()=='r' and 
                page[row][1][0].lower()=='o' and
                page[row][2][0].lower()=='o' and
                page[row][3][0].lower()=='t' and
                (page[row][4]==None or page[row][4][0]==' ')):
                page[row][3]='√'+page[row][i+3][1:]
                page[row][0]=' '+page[row][i][1:]
                page[row][1]=' '+page[row][i+1][1:]
                page[row][2]=' '+page[row][i+2][1:]
        # determines that 'root' is there to swap with '√'
        if (page[row][i][0].lower() == 'r' and not i+3 > 55 and
            not i-1 < 0):
            if page[row][i+1]==None: 
                continue
            elif (page[row][i+1][0].lower()=='o' and
                  page[row][i+2][0].lower()=='o' and
                  page[row][i+3][0].lower()=='t' and                  
                  (page[row][i-1]==None or page[row][i-1][0]==' ' )):
                page[row][i+3]='√'+page[row][i+3][1:]
                page[row][i]=' '+page[row][i][1:]
                page[row][i+1]=' '+page[row][i+1][1:]
                page[row][i+2]=' '+page[row][i+2][1:]

# replaces 'pi' on a page with 'π'
def findPi(page, row):
    for i in range(len(page[row])):
        if page[row][i] == None:
            continue
        # determines 'pi' is there for edges of the page
        if page[row][0] != None and page[row][1] != None:
            # all capital/lowecase letter spellings of 'pi' count
            if (page[row][0][0].lower()=='p' and 
                page[row][1][0].lower()=='i' and
                (page[row][2]==None or page[row][2][0]==' ')):
                page[row][0]='π'+page[row][i+1][1:]
                page[row][1]=' '+page[row][i+1][1:]
        # determines that 'pi' is there to swap with 'π'
        if (page[row][i][0].lower() == 'p' and not i+1 > 55 and
            not i-1 < 0):
            if page[row][i+1]==None: 
                continue
            elif (page[row][i+1][0].lower()=='i' and 
                  (page[row][i-1]==None or page[row][i-1][0]==' ' )):
                page[row][i]='π'+page[row][i+1][1:]
                page[row][i+1]=' '+page[row][i+1][1:]

# exponent text characters generated from:
# https://lingojam.com/SuperscriptGenerator
# replaces numbers with an exponent format of themselves
def powers(page, row):
    nums=['⁰','¹','²','³','⁴','⁵','⁶','⁷','⁸','⁹']
    stopPower = False
    for i in range(len(page[row])):
        if page[row][i] != None and page[row][i][0]=='^':
            while not stopPower:
                for j in range(i+1, 56):
                    # determines the end of an exponent
                    if page[row][j]==None:
                        stopPower=True
                        break
                    if page[row][j][0] not in '0123456789':
                        if page[row][j-1][0] in '0123456789':
                            page[row][j-1]=' '+page[row][j-1][1:]
                        stopPower=True
                        break
                    # write the exponent form
                    else:
                        num=nums[int(page[row][j][0])]
                        # back one character to delete the original format '^'
                        page[row][j-1]=num+page[row][j-1][1:]
                        if j+1 < 56 and page[row][j+1] not in nums:
                            page[row][j]=' '+page[row][j][1:]
                        elif j==55:
                            page[row][j]=' '+page[row][j][1:]
                stopPower=True