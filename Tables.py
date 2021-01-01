from Images import *
from Page import *

# creates and returns the multidimensional list representing a table
def makeTable(rows, cols, rowPlaced, serialNum):
    table = []
    corner = [rowPlaced, 0]
    for i in range(rows):
        tableRow = []
        leftSide = corner[:]
        leftSide[0] = i+corner[0]
        tableRow.append(leftSide)
        for j in range(cols):
            tableRow.append([])
        rightSide = leftSide[:]
        rightSide[0] += 1
        rightSide[1] = corner[1] + 55
        tableRow.append(rightSide)
        table.append(tableRow)
    # serial number for the table's text representation
    tableData = [table, ' ■table'+str(serialNum)]
    return tableData

# checks if a table placement or movement is legal
def legalTable(page, table):
    if table[0] == []:
        return
    topRow = table[0][0][0][0]
    bottomRow = table[0][-1][-1][0]
    if bottomRow >= 22:
        return False
    for row in range(topRow, bottomRow):
        if page[row] != [None]*56:
            return False
    return True

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

# cleans 2D list text representation of a table for when it changes
def cleanTable(page, tableTag):
    for row in range(21):
        for col in range(56):
            if page[row][col] == tableTag:
                page[row][col] = None
    return page

# determines and returns the index of the table that was clicked
def whichTable(tables, tableTag):
    for table in tables:
        if table[1] == tableTag:
            return tables.index(table)

# determines and returns which cell of a table is currently being typed in,
# represented by the row and column of the table structure
def whichCell(table, row, col):
    tableRow = None
    tableCol = None
    for r in range(len(table)):
        if row >= table[r][0][0] and row <= table[r][-1][0]:
            tableRow = r
    colsPerRow = len(table[0])-2
    # add one to tableCol because the first element of every row is a coordinate 
    # list, not a cell string
    tableCol = int(col//(56/colsPerRow)+1)
    return [tableRow, tableCol]

# updates the location of cell rows in a table when one cell expands
def stretchTable(table, onRow):
    table[onRow][-1][0] += 1
    for row in range(onRow+1, len(table)):
        table[row][0][0] += 1
        table[row][-1][0] += 1
    return table

# edits and returns table based on input (adding or deleting rows and columns)
def editTable(page, table, choice, tRow, tCol, fullTable, row, images, tables):
    if table==[]: return
    # inserts a row at a clicked on location
    tRowC=row
    newRow=[[tRowC,0]]+[[] for i in range(len(table[0])-2)]+[[tRowC+1, 55]]
    if choice == 'InsertRow':
        table.insert(tRow, newRow)
        # adjust coordinates for other rows below insertion
        for row in range(tRow+1, len(table)):
            table[row][0][0] += 1
            table[row][-1][0] += 1
    # deletes a row at a clicked on location
    if choice == 'DeleteRow':
        if table==[]:
            return
        # adjust coordinates for other rows below deleted row
        # prevent an illegal row deletion (e.g. deleting row 2 when there are
        # not even 2 rows)
        if tRow >= len(table):
            return
        delRowHeight = table[tRow][-1][0]-table[tRow][0][0]
        rowOnTable = int(table[tRow][0][0])
        for row in range(tRow+1, len(table)):
            table[row][0][0] -= delRowHeight
            table[row][-1][0] -= delRowHeight
        # ensures only rows at the chosen index are popped
        if tRow < len(table): table.pop(tRow)             
    # insert a column at a clicked on location, limit of 16 columns
    if choice == 'InsertCol' and len(table[0]) < 16:
        for row in range(len(table)):
            table[row].insert(tCol, [])
    if choice == 'DeleteCol' and not table[0][tCol]==table[0][-1]:
        for row in range(len(table)):
            table[row].pop(tCol)
    # undoes a row insertion if it is illegal by recursively deleting it
    fullTable[0] = table
    if not legalTable(page, fullTable):
        if fullTable[0]==[]: return
        lowestBlank = lowestBlankRow(page)
        insertRow = table[-1][-1][0]-1
        # moves down the rest of the text under the table as a row is inserted
        if insertRow < lowestBlank:
            page.pop(lowestBlank)
            page.insert(insertRow, [None]*56)
            moveImagesDown(page, images, insertRow, lowestBlank, False, tables)
            resetImagesTables(page, images, tables)
            return
        # recursively delete an illegal row insertion
        return editTable(page, table,'DeleteRow', tRow, tCol, fullTable, row,
                        images, tables)
    return table
    
# checks which tables are below
def tablesBelow(tableTagsBelow, tables):
    shiftDownIndexes = []
    for tag in tableTagsBelow:
        for table in tables:
            if tag in table:
                shiftDownIndexes.append(tables.index(table))
    return shiftDownIndexes

