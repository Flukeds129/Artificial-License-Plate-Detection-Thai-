import cv2
import numpy as np
import os
import test_char
#import paho.mqtt.client as mqtt

broker="m16.cloudmqtt.com"
port=14105
username="wvoywesy"
password="IJXMMEUfM1bj"


# module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False

###################################################################################################
def main(count):

    blnKNNTrainingSuccessful = test_char.loadKNNDataAndTrainKNN()        

    if blnKNNTrainingSuccessful == False:                              
        print("\nerror: KNN traning was not successful\n")  
        return                                                         
    # end if

    imgPlate  = cv2.imread("images{}.JPG".format(count))               

    if imgPlate is None:                           
        print("\nerror: image not read from file \n\n")  
        os.system("pause")                                  
        return                                              
    # end if

    listOfPossiblePlates,License_Number = test_char.detectCharsInPlates(imgPlate)        

    #cv2.imshow("imgPlate", imgPlate)            
    
    print('\nLicense Number is ',License_Number)

    client = mqtt.Client()
    client.username_pw_set(username, password)
    client.connect(broker,port)
    client.publish("License Number",License_Number)
    return
# end main


###################################################################################################
if __name__ == "__main__":
    main()


















