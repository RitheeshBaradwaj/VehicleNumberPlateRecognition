def detectPlate(imageFile,algo):

        # Read the image file
        #image = cv2.imread(imageFile)
        imageFile="R:/PROJECTS/VehicleNumberPlateDetection/"+imageFile
        print(imageFile)
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

        '''
        #this is hard coded
        
        defedged = cv2.Canny(gray, 170,200)
        cv2.imshow("4 - Canny Edges default", defedged)
        '''

        '''if algo=="one":
                cannyImg=newedged
        if algo=="two":
                cannyImg=edged'''
                        
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


        # Drawing the selected contour on the original image
        cv2.drawContours(image, [NumberPlateCnt], -1, (0,255,0), 3)
        cv2.imshow("Final Image With Number Plate Detected", image)

        cv2.waitKey(0) #Wait for user input before closing the images displayed