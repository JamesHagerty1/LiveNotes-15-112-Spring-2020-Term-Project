from Images import *
from Tables import *

# iterates over a copied text block and a page to see if there is space to
# paste that text block
def isLegalPaste(row, col, text, page):
    if text == [] or row==None or col==None:
        return
    # check if copied text will bump into text in the row it is being pasted
    blankColSpace = 0
    for c in range(col, 56):
        if page[row][c] == None: 
            blankColSpace += 1
        elif (page[row][c][0] == ' ' and not 'image' in page[row][c] and 
              not 'table' in page[row][c]):
            blankColSpace += 1 
        else:
            break
    if blankColSpace < len(text[0]):
        return False
    # check if there are enough rows to fit the height of the copied text block
    blankRowsBelow = 0
    for r in range(row, 21):
        if page[r] == [None]*56:
            blankRowsBelow += 1
    if blankRowsBelow < len(text):
        return False
    return True

# trims blank edges off of a copy/cut/paste selected text block and returns the
# edited text block
def trimTextBlock(textBlock):
    blankRows = []
    # remove blank rows
    r = 0
    for row in textBlock:
        if row == [None]*len(row):
            blankRows.append(r)
        r += 1
    # pop blank rows in a backwards order to avoid popping non blank rows
    for rowPop in blankRows[::-1]:
        textBlock.pop(rowPop)
    if textBlock == []:
        return textBlock
    # remove blank cols on the edges but not those in between text
    # remove blank cols from left end
    blankCols = []
    for col in range(len(textBlock[0])):
        allNone = True
        # breaks iteration if the the left edge has been cleared
        if col != 0 and col-1 not in blankCols:
            allNone = False
            break
        for row in textBlock:
            if row[col] != None:
                allNone = False
        if allNone:
            blankCols.append(col)
    # remove blank cols from right end
    colEnd = len(textBlock[0])-1
    for col in range(colEnd, -1, -1):
        allNone = True
        # breaks iteration if the right end has been cleared
        if col != colEnd and col+1 not in blankCols:
            allNone = False
            break
        for row in textBlock:
            if row[col] != None:
                allNone = False
        if allNone:
            blankCols.append(col)
    # pop blank cols in a backwards order to avoid popping non blank cols
    blankCols = sorted(blankCols)
    blankCols = blankCols[::-1]
    for colPop in blankCols:
        for row in range(len(textBlock)):
            textBlock[row].pop(colPop)
    return textBlock
            
# determines the closest, next column to the cursor that is not filled by an
# image (for text wrapping)
def colTextWrap(page, row, col):
    for i in range(col, 56):
        if (page[row][i] == None):
            return i
        elif not 'image' in page[row][i]:
            return i
    return col-1

# cleans former text representations of tables and images and recreates them
# according to their updated positions
def resetImagesTables(page, images, tables):
    for imageData in images:
        page = cleanAllImageText(imageData, page)
        page = imageOnText(imageData, page)
    for tableData in tables:
        page = cleanTable(page, tableData[1])
        page = tableOnText(page, tableData)