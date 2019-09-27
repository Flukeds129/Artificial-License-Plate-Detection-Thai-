# GenData.py

import sys
import numpy as np
import cv2
import os

# module level variables ##########################################################################
MIN_CONTOUR_AREA = 100

RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30

###################################################################################################
def main():
    imgTrainingNumbers = cv2.imread("training_chars.png")            

    if imgTrainingNumbers is None:                          
        print ("error: image not read from file \n\n")        
        os.system("pause")                                  
        return                                             
    # end if

    imgGray = cv2.cvtColor(imgTrainingNumbers, cv2.COLOR_BGR2GRAY)          
    imgBlurred = cv2.GaussianBlur(imgGray, (5,5), 0)                        

                                                       
    imgThresh = cv2.adaptiveThreshold(imgBlurred,                           
                                      255,                                  
                                      cv2.ADAPTIVE_THRESH_GAUSSIAN_C,       
                                      cv2.THRESH_BINARY_INV,               
                                      11,                                   
                                      2)                                    

    cv2.imshow("imgThresh", imgThresh)     

    imgThreshCopy = imgThresh.copy()        

    imgContours, npaContours, npaHierarchy = cv2.findContours(imgThreshCopy,        
                                                 cv2.RETR_EXTERNAL,                 
                                                 cv2.CHAIN_APPROX_SIMPLE)          

                                
    npaFlattenedImages =  np.empty((0, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))

    intClassifications = []         

                                    
    intValidChars = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,197,199,200,201,202,203,204,205,206,208,209,210,212,213,214,215,216,217,224,225,226,228,227,231,232,233,234,235,236,211]

    for npaContour in npaContours:                          
        if cv2.contourArea(npaContour) > MIN_CONTOUR_AREA:         
            [intX, intY, intW, intH] = cv2.boundingRect(npaContour)         

                                               
            cv2.rectangle(imgTrainingNumbers,          
                          (intX, intY),                
                          (intX+intW,intY+intH),       
                          (0, 0, 255),                  
                          2)                           

            imgROI = imgThresh[intY:intY+intH, intX:intX+intW]                                  
            imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))     

            cv2.imshow("imgROI", imgROI)                   
            cv2.imshow("imgROIResized", imgROIResized)      
            cv2.imshow("training_numbers.png", imgTrainingNumbers)      

            intChar = cv2.waitKey(0)                    

            if intChar == 27:                  
                sys.exit()                     
            elif intChar in intValidChars:			
                if intChar == 161: 
                   intClassifications.append(3585)
                elif intChar == 162:
                   intClassifications.append(3586)
                elif intChar == 163:
                   intClassifications.append(3587)   
                elif intChar == 164:
                   intClassifications.append(3588)
                elif intChar == 165:
                   intClassifications.append(3589)
                elif intChar == 166:
                   intClassifications.append(3590)
                elif intChar == 167:
                   intClassifications.append(3591)
                elif intChar == 168:
                   intClassifications.append(3592)
                elif intChar == 169:
                   intClassifications.append(3593)
                elif intChar == 170:
                   intClassifications.append(3594)
                elif intChar == 171:
                   intClassifications.append(3595)
                elif intChar == 172:
                   intClassifications.append(3596)
                elif intChar == 173:
                   intClassifications.append(3597)
                elif intChar == 174:
                   intClassifications.append(3598)
                elif intChar == 175:
                   intClassifications.append(3599)
                elif intChar == 176:
                   intClassifications.append(3600)
                elif intChar == 177:
                   intClassifications.append(3601)
                elif intChar == 178:
                   intClassifications.append(3602)
                elif intChar == 179:
                   intClassifications.append(3603)
                elif intChar == 180:
                   intClassifications.append(3604)
                elif intChar == 181:
                   intClassifications.append(3605)
                elif intChar == 182:
                   intClassifications.append(3606)
                elif intChar == 183:
                   intClassifications.append(3607)
                elif intChar == 184:
                   intClassifications.append(3608)
                elif intChar == 185:
                   intClassifications.append(3609)
                elif intChar == 186:
                   intClassifications.append(3610)
                elif intChar == 187:
                   intClassifications.append(3611)
                elif intChar == 188:
                   intClassifications.append(3612)
                elif intChar == 189:
                   intClassifications.append(3613)
                elif intChar == 190:
                   intClassifications.append(3614)
                elif intChar == 191:
                   intClassifications.append(3615)
                elif intChar == 192:
                   intClassifications.append(3616)
                elif intChar == 193:
                   intClassifications.append(3617)
                elif intChar == 194:
                   intClassifications.append(3618)
                elif intChar == 195:
                   intClassifications.append(3619)
                elif intChar == 196:
                   intClassifications.append(3620)
                elif intChar == 197:
                   intClassifications.append(3621)
                elif intChar == 199:
                   intClassifications.append(3623)
                elif intChar == 200:
                   intClassifications.append(3624)
                elif intChar == 201:
                   intClassifications.append(3625)
                elif intChar == 202:
                   intClassifications.append(3626)
                elif intChar == 203:
                   intClassifications.append(3627)
                elif intChar == 204:
                   intClassifications.append(3628)
                elif intChar == 205:
                   intClassifications.append(3629)
                elif intChar == 206:
                   intClassifications.append(3630)   
                elif intChar == 208:
                   intClassifications.append(3632)
                elif intChar == 209:
                   intClassifications.append(3633)
                elif intChar == 210:
                   intClassifications.append(3634)
                elif intChar == 211:
                   intClassifications.append(3635)
                elif intChar == 212:
                   intClassifications.append(3636)
                elif intChar == 213:
                   intClassifications.append(3637)
                elif intChar == 214:
                   intClassifications.append(3638)
                elif intChar == 215:
                   intClassifications.append(3639)
                elif intChar == 216:
                   intClassifications.append(3640)
                elif intChar == 217:
                   intClassifications.append(3641)
                elif intChar == 224:
                   intClassifications.append(3648)
                elif intChar == 225:
                   intClassifications.append(3649)
                elif intChar == 226:
                   intClassifications.append(3650)
                elif intChar == 227:
                   intClassifications.append(3651)
                elif intChar == 228:
                   intClassifications.append(3652)
                elif intChar == 231:
                   intClassifications.append(3655)
                elif intChar == 232:
                   intClassifications.append(3656)
                elif intChar == 233:
                   intClassifications.append(3657)
                elif intChar == 234:
                   intClassifications.append(3658)
                elif intChar == 235:
                   intClassifications.append(3659)
                elif intChar == 236:
                   intClassifications.append(3660)				   
                else :
                   intClassifications.append(intChar)	# append classification char to integer list of chars (we will convert to float later before writing to file)

                npaFlattenedImage = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))  
                npaFlattenedImages = np.append(npaFlattenedImages, npaFlattenedImage, 0)                   
            # end if
        # end if
    # end for

    fltClassifications = np.array(intClassifications, np.float32)                  

    npaClassifications = fltClassifications.reshape((fltClassifications.size, 1))   

    print ("\n\ntraining complete !!\n")

    np.savetxt("classifications.txt", npaClassifications)           
    np.savetxt("flattened_images.txt", npaFlattenedImages)          

    cv2.destroyAllWindows()             

    return

###################################################################################################
if __name__ == "__main__":
    main()
# end if
