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
