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

# determines and returns the index of the lowest blank row on the page
def lowestBlankRow(page):
    lowestBlank = None
    while lowestBlank == None:
        for tryRow in range(20, -1, -1):
            if page[tryRow] == [None]*56:
                lowestBlank = tryRow
                break
        break
    # prevents Nonetype crashes if there is not a lowest blank row
    if lowestBlank==None: return 0
    return lowestBlank

# determines the highest blank row on a page     
def highestBlankRow(page):
    highestBlank = None
    while highestBlank == None:
        for tryRow in range(0, 21):
            if page[tryRow] == [None]*56:
                highestBlank = tryRow
                break
        break
    # prevents NoneType crashes if there is no highest blank
    if highestBlank==None: return 20
    return highestBlank

# makes sure eraser only erases drawings in its circle
def inEraserBounds(tupX, tupY, eraser, radius):
    if eraser == (None, None) or (tupX, tupY) == (None, None):
        return
    (x, y) = eraser
    radius *= 1.25
    return (x-radius < tupX < x+radius) and (y-radius < tupY < y+radius)

# shortens the list of drawing coordinates by getting rid of erased (four None)
# tuples and then returns the edited tuples list
def cleanTuples(tuples):
    removeIndices = []
    for i in range(len(tuples)-2):
        # it is arbitrary to have two tuples of four Nones in a row
        if ((tuples[i] == (None, None, None, None)) and
           (tuples[i+1] == (None, None, None, None))):
           removeIndices.append(i)
    for j in removeIndices[::-1]:
        tuples.pop(j)
    return tuples

# recreates and returns the word a selected character belongs to
def charToWord(row, col, page):
    if page[row][col] == None:
        return None
    # determines that a word was not clicked
    if (not page[row][col][0].isalpha()) and (page[row][col][0] != "'"):
        return None
    firstHalf = []
    # go backwards from character to get the first half of the word
    if col != 0:
        for i in range(col, -1, -1):
            if page[row][i] == None:
                break
            if 'image' in page[row][i]:
                break
            if page[row][i][0].isalpha() or page[row][i][0] == "'":
               firstHalf.append(page[row][i][0])
            else:
                break
        firstHalf = firstHalf[::-1]
    # opposite process to get the other half of the word
    secondHalf = []
    if col != 55:
        for j in range(col, 56):
            if page[row][j] == None:
                break
            if 'image' in page[row][j]:
                break
            if page[row][j][0].isalpha() or page[row][j][0] == "'":
               secondHalf.append(page[row][j][0])
            else:
                break
    if firstHalf != [] and secondHalf != None:
        secondHalf = secondHalf[1:]
    return firstHalf+secondHalf

# edits selected text based on different actions, returns page of edited text
def changeText(corners, page, action):
    # reverses corners if the topLeft is in the place of the bottomRight
    if ((corners[0][0] > corners[1][0]) or 
                (corners[0][1] > corners[1][1])):
                corners = corners[::-1]
    if action == 'Delete':
        for row in range(corners[0][0], corners[1][0]+1):
            for col in range(corners[0][1], corners[1][1]):
                # prevents hidden table text representation deletion
                if (not page[row][col]==None and not 'table' in page[row][col]):
                    page[row][col] = None
    if action == 'Bold' or action == 'unBold': tag = ' b'
    if action == 'Italic' or action == 'unItalic': tag = ' i'
    # adds a string tag indicating bolding or italiscizing to selected text
    if action == 'Bold' or action == 'Italic':
        for row in range(corners[0][0], corners[1][0]+1):
            for col in range(corners[0][1], corners[1][1]):
                if page[row][col] == None:
                    continue
                else:
                    if (not tag in page[row][col] and 
                       not 'image' in page[row][col] and
                       not 'table' in page[row][col]):
                        page[row][col] += tag    
    # removes the bold string tag or italic string tag from selected text
    if action == 'unBold' or action == 'unItalic':
        for row in range(corners[0][0], corners[1][0]+1):
            for col in range(corners[0][1], corners[1][1]):
                if page[row][col] == None:
                    continue
                else:
                    if tag in page[row][col]:
                        page[row][col] = page[row][col].replace(tag, '')
    if action == 'Underline' or action == 'unUnderline': tag = ' u1'
    if action == 'Overstrike' or action == 'unOverstrike': tag = ' o1'
    # adds a string tag indicating underlining or overstriking to selected text
    if action == 'Underline' or action == 'Overstrike':
        for row in range(corners[0][0], corners[1][0]+1):
            for col in range(corners[0][1], corners[1][1]):
                if page[row][col] == None:
                    continue
                else:
                    if ((not tag in page[row][col]) and 
                        (not ' uo' in page[row][col]) and
                        (not 'image' in page[row][col]) and
                        (not 'table' in page[row][col])):
                        page[row][col] += tag    
    # removes the underline or overstrike string tag from selected text
    if action == 'unUnderline' or action == 'unOverstrike':
        for row in range(corners[0][0], corners[1][0]+1):
            for col in range(corners[0][1], corners[1][1]):
                if page[row][col] == None:
                    continue
                else:
                    if tag in page[row][col] or ' uo' in page[row][col]:
                        page[row][col] = page[row][col].replace(tag, '')
                        page[row][col] = page[row][col].replace(' uo', '')
    return page

# returns row and col of either left, top corner of selected text or
# row and col of right, bottom corner of selected text
def textCorners(x, y, width, page):
    # returns None, None if the click was out of the notebook page
    if (x < width/2.5+32) or (y < 60) or (x > 1200) or (y > 690):
        return None, None
    else: 
        # converts the x and y coordinates to the row and column on the page
        row = int(int(y)/30 - 2)
        colArea = width - (width/2.5+32)
        colSpace = colArea/56
        col = int((x - width/2.5+32)/colSpace)-5
    if row > 20:
        row = 20
    if col > 56:
        col = 56
    return row, col

# returns a word that is clicked on 
def getWord(x, y, width, page):
    (row, col) = textCorners(x, y, width, page)
    if ((row, col) == (None, None) or 
        page[row][col] == None or 
        'image' in page[row][col]):
        return
    else:
        return charToWord(row, col, page)

# finds out and returns where a line turns blank before reaching a sentence 
# word limit to cleanly splice and display text lines for dictionary definitions
def tailBlank(text):
    index = None
    while index == None:
        for i in range(len(text)-1, 0, -1):
            if text[i] == ' ':
                index = i
                break
        break
    return index

# removes all strings representing an image on the 2D list of text and returns
# edited list
# used for more complex image movement operations where more text than just the
# image of focus is being changed/moved
def cleanAllImageText(imageData, page):
    imageTag = imageData[3]
    for row in range(21):
        for col in range(56):
            if page[row][col] == imageTag:
                page[row][col] = None
    return page

# modifies the 2D list of text to represent the space of an image by its
# serial number
def imageOnText(imageData, page):
    topLeft = imageData[0]
    bottomRight = imageData[1]
    imageTag = imageData[3]
    # places an image within its corners on the 2D list
    for row in range(topLeft[0], bottomRight[0]):
        for col in range(topLeft[1], bottomRight[1]):
            page[row][col] = imageTag
    return page

# other (imports inapplicable)

# cleans 2D list text representation of a table for when it changes
def cleanTable(page, tableTag):
    for row in range(21):
        for col in range(56):
            if page[row][col] == tableTag:
                page[row][col] = None
    return page

# creates 2D list text representation of a table
def tableOnText(page, table):
    if table[0]==[] or None in table:
        return page
    topLeft = table[0][0][0]
    bottomRight = table[0][-1][-1]
    tableTag = table[1]
    for row in range(topLeft[0], bottomRight[0]):
        for col in range(topLeft[1], bottomRight[1]+1):
            page[row][col] = tableTag
    return page