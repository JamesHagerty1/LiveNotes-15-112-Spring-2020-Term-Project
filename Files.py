import csv
from tkinter.filedialog import askopenfilename

# file writing technique adapted from:                 
# https://www.youtube.com/watch?v=s1XiCh-mGCA
# saves all of the notebook data into a file that can be reopened later
def saveFile(nameFile, typedText, drawingTuples, speechNotes, pageImages,
             pageTables):
    if nameFile == None:
        return
    with open(nameFile+'.csv', 'w', newline='') as file:
        fileMaker = csv.writer(file)
        for page in typedText:
            fileMaker.writerow(['START'])
            for line in page:
                lineCopy = line[:]
                # prevents typed commas from being deleted when the file
                # is opened later and its lines are .split(',')
                for i in range(len(lineCopy)):
                    if lineCopy[i] == ',':
                        lineCopy[i] = 'COMMA'
                fileMaker.writerow(lineCopy)
            fileMaker.writerow(['END'])
        for drawing in drawingTuples:
            fileMaker.writerow(['START2'])
            for tup in drawing:
                fileMaker.writerow(tup)
            fileMaker.writerow(['END2'])
        for speechPage in speechNotes:
            fileMaker.writerow(['START3'])
            fileMaker.writerow(speechPage)
            fileMaker.writerow(['END3'])
        for images in pageImages:
            fileMaker.writerow(['START4'])
            for image in images:
                fileMaker.writerow(image)
            fileMaker.writerow(['END4'])
        for tables in pageTables:
            fileMaker.writerow(['START5'])
            for table in tables:
                fileMaker.writerow(table)
            fileMaker.writerow(['END5'])
    return

# reads CSV files tailored for and created in the app and opens them, returns
# all data structures from the saved file
def openFile(filename):
    with open(filename, "rt") as f:
        pages = f.read()
    pages = pages.split('\n')
    allPages = []
    page = []
    pageLine = []
    tuplesStart = None
    # recreates text data from saved file
    for line in pages:
        if line == 'START2':
            # determines where to start recreating drawings
            tuplesStart = pages.index(line)
            break
        if line == 'START':
            continue
        elif line == 'END':
            allPages.append(page)
            page = []
        else:
            for char in line.split(','):
                if char == '':
                    pageLine.append(None)
                # ensures that text commas will not be deleted later when the
                # line is read with .split(',') when opening the file
                elif char == 'COMMA':
                    pageLine.append(',')
                else:
                    pageLine.append(char)
            page.append(pageLine)
            pageLine = []
    # recreates drawings data from saved file
    allPagesDraw = []
    pageDraw = []
    pageLine = []
    speechStart = None
    for line in pages[tuplesStart:]:
        if line == 'START3':
            # determines where to start recreating speech text
            speechStart = pages.index(line)
            break
        if line == 'START2':
            continue
        elif line == 'END2':
            allPagesDraw.append(pageDraw)
            pageDraw = []
        else:
            if line == ',,,':
                vals = [None, None, None, None]
            else:
                vals = line.split(',')
            for i in range(len(vals)):
                if (vals[i] != None) and (i != 3) and (len(vals) == 4):
                    vals[i] = float(vals[i])
            tup = tuple(vals)
            if len(tup) == 4:
                pageDraw.append(tup)
    allSpeechPages = []
    imageStart = None
    # recreates speech text from saved file
    for speechPage in pages[speechStart:]:
        if speechPage == 'START4':
            # determines where to start recreating images
            imageStart = pages.index(speechPage)
            break
        if speechPage != 'START3' and speechPage != 'END3' and speechPage != "":
            allSpeechPages.append([speechPage])
    # recreates images from saved file
    allImagePages = []
    tableStart = None
    for page in pages[imageStart:]:
        if page == 'START5':
            tableStart = pages.index(page)
            break
        if page == 'START4':
            imagePage = []
            continue
        if page == 'END4':
            allImagePages.append(imagePage)
            continue
        else:
            picture = []
            # convert string of image corner coordinates into lists as they
            # were in the original image data
            coordList = []
            for elem in page.split(','):
                if page.split(',').index(elem) < 4:
                    newElem = ''
                    for char in elem:
                        if char.isdigit():
                            newElem += char
                    newElem = int(newElem)
                    coordList.append(newElem)
                    if len(coordList) == 2:
                        picture.append(coordList)
                        coordList = []
                # recreates the rest of the image data
                elif page.split(',').index(elem) == 4:
                    picture.append(None)
                else:
                    picture.append(elem)
            imagePage.append(picture)
    # recreates tables from saved file
    allTablesPages = []
    for page in pages[tableStart:]:
        if page == '':
            break
        if page == 'START5':
            tablePage = []
            continue
        if page == 'END5':
            allTablesPages.append(tablePage)
            continue
        else:
            oneTable = []
            tableComponents = page.split(' ■table')
            tableCells = eval(tableComponents[0][:-1])
            tableCells = eval(tableCells)
            tableID = ' ■table'+tableComponents[-1]
            oneTable.append(tableCells)
            oneTable.append(tableID)
            tablePage.append(oneTable)
    return allPages, allPagesDraw, allSpeechPages, allImagePages, allTablesPages