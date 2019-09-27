import os

import cv2
import numpy as np
import math
import random

import test_Readplate
import Preprocess
import PossibleChar

# module level variables ##########################################################################

kNearest = cv2.ml.KNearest_create()

        
MIN_PIXEL_WIDTH = 20 #2#30
MIN_PIXEL_HEIGHT = 70#8#100

MIN_ASPECT_RATIO = 0.25
MAX_ASPECT_RATIO = 1.0

MIN_PIXEL_AREA = 100 #50

        
MIN_DIAG_SIZE_MULTIPLE_AWAY = 0.3
MAX_DIAG_SIZE_MULTIPLE_AWAY = 5.0

MAX_CHANGE_IN_AREA = 0.5

MAX_CHANGE_IN_WIDTH = 0.8
MAX_CHANGE_IN_HEIGHT = 0.2

MAX_ANGLE_BETWEEN_CHARS = 12.0

      
MIN_NUMBER_OF_MATCHING_CHARS = 3

RESIZED_CHAR_IMAGE_WIDTH = 20
RESIZED_CHAR_IMAGE_HEIGHT = 30

MIN_CONTOUR_AREA = 100 #100

###################################################################################################
def loadKNNDataAndTrainKNN():
    allContoursWithData = []                
    validContoursWithData = []              

    try:
        npaClassifications = np.loadtxt("classifications.txt", np.float32)                  
    except:                                                                                
        print("error, unable to open classifications.txt, exiting program\n")  
        os.system("pause")
        return False                                                                        
    # end try

    try:
        npaFlattenedImages = np.loadtxt("flattened_images.txt", np.float32)                 
    except:                                                                                 
        print("error, unable to open flattened_images.txt, exiting program\n")  
        os.system("pause")
        return False                                                                        
    # end try

    npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))      

    kNearest.setDefaultK(1)                                                            

    kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)          

    return True                            
# end function

###################################################################################################


def detectCharsInPlates(imgPlate):
    intPlateCounter = 0
    imgContours = None
    contours = []
   
    imgGrayscale, imgThresh = Preprocess.preprocess(imgPlate)     

    if test_Readplate.showSteps == True: # show steps ###################################################
        cv2.imshow("1a", imgPlate)
        cv2.imshow("1b", imgGrayscale)
        cv2.imshow("1c", imgThresh)
        # end if # show steps #####################################################################

                
    imgThresh = cv2.resize(imgThresh, (0, 0), fx = 3, fy = 3)

                
    thresholdValue, imgThresh = cv2.threshold(imgThresh, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    if test_Readplate.showSteps == True: # show steps ###################################################
        cv2.imshow("1d", imgThresh)
        # end if # show steps #####################################################################

                
                
    listOfPossibleCharsInPlate = findPossibleCharsInPlate(imgGrayscale, imgThresh)

    if test_Readplate.showSteps == True: # show steps ###################################################
        height, width, numChannels = imgPlate.shape
        imgContours = np.zeros((height, width, 3), np.uint8)
        del contours[:]                                         # clear the contours list

        for possibleChar in listOfPossibleCharsInPlate:
            contours.append(possibleChar.contour)
            # end for

        cv2.drawContours(imgContours, contours, -1, test_Readplate.SCALAR_WHITE)

        cv2.imshow("2", imgContours)
        # end if # show steps #####################################################################

                
    listOfListsOfMatchingCharsInPlate = findListOfListsOfMatchingChars(listOfPossibleCharsInPlate)

    if test_Readplate.showSteps == True: # show steps ###################################################
        imgContours = np.zeros((height, width, 3), np.uint8)
        del contours[:]

        for listOfMatchingChars in listOfListsOfMatchingCharsInPlate:
            intRandomBlue = random.randint(0, 255)
            intRandomGreen = random.randint(0, 255)
            intRandomRed = random.randint(0, 255)

            for matchingChar in listOfMatchingChars:
                contours.append(matchingChar.contour)
                # end for
            cv2.drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
            # end for
        cv2.imshow("3", imgContours)
        # end if # show steps #####################################################################

    if (len(listOfListsOfMatchingCharsInPlate) == 0):	
        
        
        if test_Readplate.showSteps == True: # show steps ###############################################
            print("chars found in plate number " + str(
                intPlateCounter) + " = (none), click on any image and press a key to continue . . .")
            intPlateCounter = intPlateCounter + 1
            cv2.destroyWindow("4")
            cv2.destroyWindow("5")
            cv2.destroyWindow("6")
            cv2.waitKey(0)
            # end if # show steps #################################################################

        strChars = "Not found license number"
        return imgPlate,strChars
		
    elif not (len(listOfListsOfMatchingCharsInPlate) == 0):
       for i in range(0, len(listOfListsOfMatchingCharsInPlate)):                              
           listOfListsOfMatchingCharsInPlate[i].sort(key = lambda matchingChar: matchingChar.intCenterX)       
           listOfListsOfMatchingCharsInPlate[i] = removeInnerOverlappingChars(listOfListsOfMatchingCharsInPlate[i])            
        # end for

       if test_Readplate.showSteps == True: # show steps ###################################################
        imgContours = np.zeros((height, width, 3), np.uint8)

        for listOfMatchingChars in listOfListsOfMatchingCharsInPlate:
            intRandomBlue = random.randint(0, 255)
            intRandomGreen = random.randint(0, 255)
            intRandomRed = random.randint(0, 255)

            del contours[:]

            for matchingChar in listOfMatchingChars:
                contours.append(matchingChar.contour)
                # end for

            cv2.drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
            # end for
        cv2.imshow("4", imgContours)
        # end if # show steps #####################################################################

             
       intLenOfLongestListOfChars = 0
       intIndexOfLongestListOfChars = 0

         
       for i in range(0, len(listOfListsOfMatchingCharsInPlate)):
           if len(listOfListsOfMatchingCharsInPlate[i]) > intLenOfLongestListOfChars:
               intLenOfLongestListOfChars = len(listOfListsOfMatchingCharsInPlate[i])
               intIndexOfLongestListOfChars = i
            # end if
        # end for

         
       longestListOfMatchingCharsInPlate = listOfListsOfMatchingCharsInPlate[intIndexOfLongestListOfChars]

       if test_Readplate.showSteps == True: # show steps ###################################################
           imgContours = np.zeros((height, width, 3), np.uint8)
           del contours[:]

           for matchingChar in longestListOfMatchingCharsInPlate:
               contours.append(matchingChar.contour)
            # end for

           cv2.drawContours(imgContours, contours, -1, test_Readplate.SCALAR_WHITE)

           cv2.imshow("5", imgContours)
           # end if # show steps #####################################################################

       strChars = recognizeCharsInPlate(imgThresh, longestListOfMatchingCharsInPlate)

       if test_Readplate.showSteps == True: # show steps ###################################################
           print("chars found in plate number " + str(
               intPlateCounter) + " = " + strChars + ", click on any image and press a key to continue . . .")
           intPlateCounter = intPlateCounter + 1
           cv2.waitKey(0)
        # end if # show steps #####################################################################

     

       if test_Readplate.showSteps == True:
           print("\nchar detection complete, click on any image and press a key to continue . . .\n")
           cv2.waitKey(0)

       return imgPlate,strChars
	   # end if
# end function

def findPossibleCharsInPlate(imgGrayscale, imgThresh):
    listOfPossibleChars = []                        
    contours = []
    imgThreshCopy = imgThresh.copy()

            
    contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:                        
        possibleChar = PossibleChar.PossibleChar(contour)

        if checkIfPossibleChar(possibleChar):              
            listOfPossibleChars.append(possibleChar)       

    return listOfPossibleChars
# end function

def checkIfPossibleChar(possibleChar):

    if (possibleChar.intBoundingRectArea > MIN_PIXEL_AREA and
        possibleChar.intBoundingRectWidth > MIN_PIXEL_WIDTH and 
        possibleChar.intBoundingRectHeight > MIN_PIXEL_HEIGHT and
        MIN_ASPECT_RATIO < possibleChar.fltAspectRatio and possibleChar.fltAspectRatio 
        < MAX_ASPECT_RATIO):
        return True
    else:
        return False
    # end if
# end function

def findListOfListsOfMatchingChars(listOfPossibleChars):
            
    listOfListsOfMatchingChars = []                 

    for possibleChar in listOfPossibleChars:                        
        listOfMatchingChars = findListOfMatchingChars(possibleChar, listOfPossibleChars)        

        listOfMatchingChars.append(possibleChar)                

        if len(listOfMatchingChars) < MIN_NUMBER_OF_MATCHING_CHARS:     
            continue                            
                                                
        # end if

                                                
        listOfListsOfMatchingChars.append(listOfMatchingChars)      

        listOfPossibleCharsWithCurrentMatchesRemoved = []

                                               
        listOfPossibleCharsWithCurrentMatchesRemoved = list(set(listOfPossibleChars) - set(listOfMatchingChars))

        recursiveListOfListsOfMatchingChars = findListOfListsOfMatchingChars(listOfPossibleCharsWithCurrentMatchesRemoved)      

        for recursiveListOfMatchingChars in recursiveListOfListsOfMatchingChars:        
            listOfListsOfMatchingChars.append(recursiveListOfMatchingChars)            
        # end for

        break       # exit for

    # end for

    return listOfListsOfMatchingChars
# end function

def findListOfMatchingChars(possibleChar, listOfChars):
            
    listOfMatchingChars = []                

    for possibleMatchingChar in listOfChars:               
        if possibleMatchingChar == possibleChar:    
                                                    
            continue                                
        # end if
                    
        fltDistanceBetweenChars = distanceBetweenChars(possibleChar, possibleMatchingChar)

        fltAngleBetweenChars = angleBetweenChars(possibleChar, possibleMatchingChar)

        fltChangeInArea = float(abs(possibleMatchingChar.intBoundingRectArea - possibleChar.intBoundingRectArea)) / float(possibleChar.intBoundingRectArea)

        fltChangeInWidth = float(abs(possibleMatchingChar.intBoundingRectWidth - possibleChar.intBoundingRectWidth)) / float(possibleChar.intBoundingRectWidth)
        fltChangeInHeight = float(abs(possibleMatchingChar.intBoundingRectHeight - possibleChar.intBoundingRectHeight)) / float(possibleChar.intBoundingRectHeight)

                
        if (fltDistanceBetweenChars < (possibleChar.fltDiagonalSize * MAX_DIAG_SIZE_MULTIPLE_AWAY) and
            fltAngleBetweenChars < MAX_ANGLE_BETWEEN_CHARS and
            fltChangeInArea < MAX_CHANGE_IN_AREA and
            fltChangeInWidth < MAX_CHANGE_IN_WIDTH and
            fltChangeInHeight < MAX_CHANGE_IN_HEIGHT):

            listOfMatchingChars.append(possibleMatchingChar)        
        # end if
    # end for

    return listOfMatchingChars                  # return result
# end function

###################################################################################################
# use Pythagorean theorem to calculate distance between two chars
def distanceBetweenChars(firstChar, secondChar):
    intX = abs(firstChar.intCenterX - secondChar.intCenterX)
    intY = abs(firstChar.intCenterY - secondChar.intCenterY)

    return math.sqrt((intX ** 2) + (intY ** 2))
# end function

###################################################################################################
# use basic trigonometry (SOH CAH TOA) to calculate angle between chars
def angleBetweenChars(firstChar, secondChar):
    fltAdj = float(abs(firstChar.intCenterX - secondChar.intCenterX))
    fltOpp = float(abs(firstChar.intCenterY - secondChar.intCenterY))

    if fltAdj != 0.0:                           
        fltAngleInRad = math.atan(fltOpp / fltAdj)      
    else:
        fltAngleInRad = 1.5708                          
    # end if

    fltAngleInDeg = fltAngleInRad * (180.0 / math.pi)       

    return fltAngleInDeg
# end function

###################################################################################################

def removeInnerOverlappingChars(listOfMatchingChars):
    listOfMatchingCharsWithInnerCharRemoved = list(listOfMatchingChars)               

    for currentChar in listOfMatchingChars:
        for otherChar in listOfMatchingChars:
            if currentChar != otherChar:        
                                                                            
                if distanceBetweenChars(currentChar, otherChar) < (currentChar.fltDiagonalSize * MIN_DIAG_SIZE_MULTIPLE_AWAY):
                                
                    if currentChar.intBoundingRectArea < otherChar.intBoundingRectArea:         
                        if currentChar in listOfMatchingCharsWithInnerCharRemoved:             
                            listOfMatchingCharsWithInnerCharRemoved.remove(currentChar)        
                        # end if
                    else:                                                                      
                        if otherChar in listOfMatchingCharsWithInnerCharRemoved:                
                            listOfMatchingCharsWithInnerCharRemoved.remove(otherChar)           
                        # end if
                    # end if
                # end if
            # end if
        # end for
    # end for

    return listOfMatchingCharsWithInnerCharRemoved
# end function

###################################################################################################
def recognizeCharsInPlate(imgThresh, listOfMatchingChars):
    strChars = "" 

    listOfMatchingChars             

    height, width = imgThresh.shape

    imgThreshColor = np.zeros((height, width, 3), np.uint8)

    listOfMatchingChars.sort(key = lambda matchingChar: matchingChar.intCenterX)        

    cv2.cvtColor(imgThresh, cv2.COLOR_GRAY2BGR, imgThreshColor)                    

    for currentChar in listOfMatchingChars:                                       
        pt1 = (currentChar.intBoundingRectX, currentChar.intBoundingRectY)
        pt2 = ((currentChar.intBoundingRectX + currentChar.intBoundingRectWidth), 
        (currentChar.intBoundingRectY + currentChar.intBoundingRectHeight))

        cv2.rectangle(imgThreshColor, pt1, pt2, test_Readplate.SCALAR_GREEN, 2)         

        imgROI = imgThresh[currentChar.intBoundingRectY : currentChar.intBoundingRectY + 
                           currentChar.intBoundingRectHeight,
                           currentChar.intBoundingRectX : currentChar.intBoundingRectX + 
                           currentChar.intBoundingRectWidth]

        imgROIResized = cv2.resize(imgROI, (RESIZED_CHAR_IMAGE_WIDTH, RESIZED_CHAR_IMAGE_HEIGHT))          

        npaROIResized = imgROIResized.reshape((1, RESIZED_CHAR_IMAGE_WIDTH * RESIZED_CHAR_IMAGE_HEIGHT))       

        npaROIResized = np.float32(npaROIResized)               

        retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k =2)              

        strCurrentChar = str(chr(int(npaResults[0][0])))            

        strChars = strChars + strCurrentChar                       
    # end for
    if test_Readplate.showSteps == True: # show steps #######################################################
        cv2.imshow("6", imgThreshColor)
    # end if # show steps #########################################################################

    return strChars
# end function
