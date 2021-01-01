from Tables import *
from Page import *

# erases former text image representation and replaces it with current text
# image representation
def textTransition(page, images):
    for imageData in images:
        page = cleanAllImageText(imageData, page)
    for imageData in images:
        page = imageOnText(imageData, page)
    return page

# returns list indicating the images below
def imagesBelow(imageTagsBelow, images):
    shiftDownIndexes = []
    for tag in imageTagsBelow:
        for img in images:
            if tag in img:
                shiftDownIndexes.append(images.index(img))
    return shiftDownIndexes

# determines whether an image can be placed in a spot by checking if the 2D list
# page is empty within the corners of the image
def legalImagePlacement(imageData, page):
    # image corners
    topLeft = imageData[0]
    bottomRight = imageData[1]
    for row in range(topLeft[0], bottomRight[0]):
        if row > 20:
            return False
        for col in range(topLeft[1], bottomRight[1]):
            if col > 55:
                return False
            if page[row][col] == None:
                continue
            elif (page[row][col][0] != ' ' or 'image' in page[row][col] or
                  'table' in page[row][col]):
                return False
    return True

# determines if resizing or dragging the image makes it bump into other text
# or images
def legalImageMovement(imageData, page):
    # imageTag is the name of the strings representing the image on the 2D list
    # of text
    imageTag = imageData[3]
    topLeft = imageData[0]
    bottomRight = imageData[1]
    for row in range(topLeft[0], bottomRight[0]):
        if row > 20:
            return False
        for col in range(topLeft[1], bottomRight[1]):
            if col > 55:
                return False
            if page[row][col] == None:
                continue
            if page[row][col] == imageTag:
                continue
            elif (page[row][col][0] != ' ' or 'image' in page[row][col] or
                  'table' in page[row][col]):
                return False
    return True

# efficient way of removing all string representations of an image on the 2D
# list of text when the strings are to be moved and returns edited list
# only used when only one image is being altered
def cleanImageText(imageData, page):
    topLeft = imageData[0]
    bottomRight = imageData[1]
    imageTag = imageData[3]
    # only spans the 2D list area where the image used to be
    for row in range(topLeft[0], bottomRight[0]):
        for col in range(topLeft[1], bottomRight[1]):
            if page[row][col] == imageTag:
                page[row][col] = None
    return page

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

# determines/returns the index of an image in the list containing images and 
# what action is to be performed on the image (moving or resizing) depending on
# what section of the image was clicked
def getImageData(whichImage, images, row, col):
    imageIndex = None
    imageAction = None
    for data in images:
        if data[3] == whichImage:
            imageIndex = images.index(data)
            break
    # checks if the bottom right fourth of the image was clicked, this means
    # the image is to be resized
    if ((row > (images[imageIndex][0][0]+images[imageIndex][1][0])/2) and
        (col > (images[imageIndex][0][1]+images[imageIndex][1][1])/2)):
        imageAction = 'resizing'
    # clicking on the image elsewhere means preparing to move it
    else:
        imageAction = 'moving'
    return (imageIndex, imageAction)

# used when bulleting/numbering lists to prevent a row with an image from
# being bulleted, determines if an image takes up part of the row
def imageInRow(page, row):
    for char in page[row]:
        if char == None:
            continue
        elif 'image' in char:
            return True
    return False

# moves tables and images up for actions like deleting upwards or moving
# an image up against text to move it up
def moveImagesUp(page, images, highestBlank, row, exception, tables):
    # moves images up
    imageTagsAbove = set()
    for imageInfo in images:
        if images==[]: break
        # exception for deleting to avoid text spacing error
        if exception and row <= imageInfo[1][0]:
            imageTagsAbove.add(imageInfo[3])
        # limits to images that can only be moved up legally
        elif row >= imageInfo[1][0] and not imageInfo[1][0] < highestBlank:
            imageTagsAbove.add(imageInfo[3])
    shiftUpIndexes = []
    for tag in imageTagsAbove:
        if images==[]: break
        for img in images:
            if tag in img:
                shiftUpIndexes.append(images.index(img))
    for image in shiftUpIndexes:
        if images==[]: break
        imageData = images[image]
        highestBlank = highestBlankRow(page)
        if imageData[1][0] > highestBlank and not imageData[0][0] == 0: 
            imageData[0][0] -= 1
            imageData[1][0] -= 1
    # moves tables up
    tableTagsAbove = set()
    for tableInfo in tables:
        if tableInfo[0]==[]: break
        # avoids text shifting error
        if exception and row <= tableInfo[0][-1][-1][0]:
            tableTagsAbove.add(tableInfo[1])
        # limits to tables that can be moved up legally
        elif (row >= tableInfo[0][-1][-1][0] and 
              not tableInfo[0][-1][-1][0] < highestBlank):
            tableTagsAbove.add(tableInfo[1])
    shiftUpIndexes = []
    for tag in tableTagsAbove:
        for table in tables:
            if tag in table:
                shiftUpIndexes.append(tables.index(table))
    for table in shiftUpIndexes:
        tableData = tables[table]
        highestBlank = highestBlankRow(page)
        if (tableData[0][-1][-1][0] > highestBlank and 
            not tableData[0][0][0][0] == 0): 
            for row in range(len(tableData[0])):
                 tableData[0][row][0][0] -= 1
                 tableData[0][row][-1][0] -= 1
    return

# moves images and tables down for actions like entering or new text pushing
# downwards or other images being pushed down
def moveImagesDown(page, images, row, lowestBlank, exception, tables):
    # moves images down
    imageTagsBelow = set()
    for imageInfo in images:
        # limits to images below the object/action moving them down
        if row <= imageInfo[0][0]:
            imageTagsBelow.add(imageInfo[3])
    shiftDownIndexes = imagesBelow(imageTagsBelow, images)
    for image in shiftDownIndexes:
        imageData = images[image]
        page = cleanAllImageText(imageData, page)
        if imageData[1][0]-1 < lowestBlank: 
            imageData[0][0] += 1
            imageData[1][0] += 1
        elif exception == True:
            imageData[0][0] += 1
            imageData[1][0] += 1
    # moves tables down
    tableTagsBelow = set()
    for tableInfo in tables:
        # limits to tabels below the object/action moving them down
        if row <= tableInfo[0][0][0][0]:
            tableTagsBelow.add(tableInfo[1])
    shiftDownIndexes = tablesBelow(tableTagsBelow, tables)
    for table in shiftDownIndexes:
        tableData = tables[table]
        page = cleanTable(page, tableData[1])
        if tableData[0][-1][-1][0]-1 < lowestBlank:
            for row in range(len(tableData[0])):
                 tableData[0][row][0][0] += 1
                 tableData[0][row][-1][0] += 1
    # clean former text representations off before creating new ones
    resetImagesTables(page, images, tables)
    return

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

# other (import inapplicable)

# checks which tables are below
def tablesBelow(tableTagsBelow, tables):
    shiftDownIndexes = []
    for tag in tableTagsBelow:
        for table in tables:
            if tag in table:
                shiftDownIndexes.append(tables.index(table))
    return shiftDownIndexes

# cleans 2D list text representation of a table for when it changes
def cleanTable(page, tableTag):
    for row in range(21):
        for col in range(56):
            if page[row][col] == tableTag:
                page[row][col] = None
    return page