import numpy as np
import cv2
import pytesseract
from PIL import Image
import pyttsx3
from googletrans import Translator

# Load and then gray scale image

def get_numberplate(image,contours):
    # Get the cropped image using contours
    x,y,w,h = cv2.boundingRect(contours)
    #print(x,y,w,h)
    cropped = image[y:y+h , x:x+w]

    cv2.imshow('Required Area',cropped)
    pytesseract.pytesseract.tesseract_cmd ='C:/Program Files/Tesseract-OCR/tesseract.exe'   

    result = pytesseract.image_to_string(cropped)
    print("Extracted Number Plate :",result)
    # importing the pyttsx library
    import pyttsx3
    # initialisation 
    engine = pyttsx3.init() 
    engine.say(str(result))
    engine.runAndWait() 
    
    cv2.waitKey(0)    

    cv2.destroyAllWindows()
import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import os
import numpy as np
import imutils

selected_file = ""

def get_image():
    root.withdraw() #hide main window
    fileName = filedialog.askopenfilename(
        filetypes = [ ("jpeg files","*.jpg"),("All files", ".*") ],
        initialdir="R:/PROJECTS/VehicleNumberPlateDetection/Images(Input)", #this one should be changed according to local reference
        title="Select your image")

    global selected_file 
    selected_file = os.path.basename(fileName) #to get exact name of the file within same directory
    
    if fileName != None:
        print("The Selected image is ", selected_file)

    tk.messagebox.showinfo("Info","You selected a Image") #message box

    new_window = tk.Toplevel(root)

    selected_image = ImageTk.PhotoImage(file = fileName) #to compatible with different image formats
    label_img = tk.Label(new_window, image = selected_image)
    btn = Button(new_window, width="20", text="Confirm", bg="green", command = new_window.withdraw )
    label_img.image = selected_image

    label_img.grid(row=0,column=1)
    btn.grid(row=1,column=1)

    root.deiconify() #retrieve main window again
    b2.config(state="normal") #detect button enable
def detectPlate(imageFile,algo):

        # Read the image file
        #image = cv2.imread(imageFile)
        imageFile="R:/PROJECTS/VehicleNumberPlateDetection/Images(Input)/"+imageFile
        #print(imageFile)
        image = cv2.imread(imageFile)
        #image=Image.open(imageFile)
        # Resize the image - change width to 500
        image = imutils.resize(image, width=500)

        # Display the original image
        cv2.imshow("Original Image", image)


        # RGB to Gray scale conversion
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow("1 - Grayscale Conversion", gray)

        # Noise removal with iterative bilateral filter(removes noise while preserving edges)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        cv2.imshow("2 - Bilateral Filter", gray)

        high_thresh, thresh_im=cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        lowThresh = 0.5*high_thresh

        # compute the median of the single channel pixel intensities
        v = np.median(image)
        sigma=0.33
        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))

        # Find Edges of the grayscale image(aperture thresh calculated by median intensity of image)
        edged = cv2.Canny(gray, lower,upper)
        cv2.imshow("4 - Canny Edges autocanny", edged)

        #using otsu algo
        newedged = cv2.Canny(gray, lowThresh,high_thresh)
        
        cv2.imshow("4 - Canny Edges otsu", newedged)
        
                        
        # Find contours based on Edges
        ( cnts, _) = cv2.findContours(newedged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:30] #sort contours based on their area keeping minimum required area as '30' (anything smaller than this will not be considered)
        NumberPlateCnt = None #we currently have no Number plate contour

        # loop over our contours to find the best possible approximate contour of number plate
        count = 0
        for c in cnts:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)

                #cv2.drawContours(image, [approx], -1, (0, 255, 0), 3)
                #cv2.imshow("all conts", image)

                if len(approx) == 4:  # Select the contour with 4 corners
                    NumberPlateCnt = approx
                    #This is our approx Number Plate Contour
                    break

        #print(NumberPlateCnt)
        # Drawing the selected contour on the original image
        cv2.drawContours(image, [NumberPlateCnt], -1, (0,255,0), 3)
        cv2.imshow("Final Image With Number Plate Detected", image)
        get_numberplate(image,NumberPlateCnt)
        

        cv2.waitKey(0) #Wait for user input before closing the images displayed
root = tk.Tk()

label_1 = Label(root,width="40",height="2", text="Number Plate Detection", bg="cyan")
load =Image.open('R:/PROJECTS/VehicleNumberPlateDetection/icon_image.jpg')

img_label = ImageTk.PhotoImage(load,master=root)
lab_im = tk.Label(root, image = img_label, width="600", height="300")
lab_im.image = img_label

#image selection button
b1 = Button(root, text="Select Image", width="10", command = get_image, bg="white", fg="blue", anchor="n", padx="20", pady="15")
#dropdown selection
variable = StringVar(root)
variable.set("Select the Algorithm")
w = OptionMenu(root, variable, "one")
algo = variable.get()
#plate detection button
b2 = Button(root, text="Detect Number Plate", width="20", height="1", command= lambda: detectPlate(selected_file,algo), fg="black", bg="white", state=DISABLED )
label_1.grid(row=0,column=1)
lab_im.grid(row=1,column=1)
b1.grid(row=2,column=1);

w.grid(row=4, column=1)

b2.grid(row=5,column=1);

root.mainloop()

