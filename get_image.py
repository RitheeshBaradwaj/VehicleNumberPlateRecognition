def get_image():
    root.withdraw() #hide main window
    fileName = filedialog.askopenfilename(
        filetypes = [ ("jpeg files","*.jpg"),("All files", ".*") ],
        initialdir="R:/PROJECTS/VehicleNumberPlateDetection", #this one should be changed according to local reference
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