import tkinter as tk
from tkinter import ttk, filedialog, Label
import cv2
import numpy as np
import os
import pandas as pd
from PIL import ImageTk, Image
excel_file = "data.xlsx"
pp_path = "images"
df = pd.read_excel(excel_file)

# Creating a Tkinter window
window = tk.Tk()
window.title("Signature Recognition Application")
file_path = ""
dataset_path = "sign_data/train"
# Create a file selector button
def open_file():
    global file_path
    file_path = filedialog.askopenfilename()


file_button = ttk.Button(window, text="Select File", command=open_file)
file_button.grid(column=0, row=0, padx=10, pady=10, sticky='wens')

# Create correlation value input box
correlation_label = ttk.Label(window, text="Correlation (0-0.9) :")
correlation_label.grid(column=1, row=0, padx=10, pady=10, sticky='wens')

correlation_entry = ttk.Entry(window)
correlation_entry.grid(column=2, row=0, padx=5, pady=5, sticky='wens')
correlation_entry.insert(tk.END, 0.7)
correlation_entry.config(width=5, font=("Arial", 7))

def get_person_info(id):
    person = df.loc[df['ID'] == id]
    if len(person) == 0:
        return f"ID not found! {id}"
    else:
        name = str(person['Name'].values[0])
        acc_no = str(person['ACC/NO'].values[0])
        dob = str(person['DOB'].values[0])
        location = str(person['Location'].values[0])

        # Define labels and their maximum width for alignment
        label_width = 10  # Adjust based on the longest label

        formatted_info = (
            f"{'Name'.ljust(label_width)}: {name}\n"
            f"{'ACC/NO'.ljust(label_width)}: {acc_no}\n"
            f"{'DOB'.ljust(label_width)}: {dob[:10]}\n"
            f"{'Location'.ljust(label_width)}: {location}"
        )

        return formatted_info


        # return name + "\n"+ surname +"\n"+ birth_date[:10] +"\n"+ birth_place

def find_signature():
    result_label.config(text="")
        # Load the image and convert it to grayscale
    if(file_path == ""):
        result_label.config(text="Please choose a Signature!")
        return None
    image = cv2.imread(file_path)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Set the threshold for template matching
    threshold = float(correlation_entry.get())

    # Iterate over the folders in the dataset
    for folder in os.listdir(dataset_path):
        if not folder.endswith("_forg"):
            # Iterate over the signature images in the folder
            for signature_image in os.listdir(os.path.join(dataset_path, folder)):
                # Load the signature image and convert it to grayscale
                signature = cv2.imread(os.path.join(dataset_path, folder, signature_image))
                signature_gray = cv2.cvtColor(signature, cv2.COLOR_BGR2GRAY)

                # Resize the signature image if it is larger than the source image
                if signature_gray.shape[0] > image_gray.shape[0] or signature_gray.shape[1] > image_gray.shape[1]:
                    signature_gray = cv2.resize(signature_gray, (image_gray.shape[1], image_gray.shape[0]))

                # Apply template matching
                result = cv2.matchTemplate(image_gray, signature_gray, cv2.TM_CCOEFF_NORMED)

                loc = np.where(result >= threshold)

                # Check if a match was found
                if len(loc[0]) > 0:
                    result_label.config(text=get_person_info(int(folder[1:])))
                    # # Add image as Tag
                    image = Image.open(pp_path+f"/{folder}.png")
                    image = image.resize((256,256))
                    photo = ImageTk.PhotoImage(image)
                    label = Label(image=photo)
                    label.image = photo     # store the photo object as a property of the label object
                    label.grid(column=2, row=3, padx=10, pady=10, sticky='e')
                    return folder
                 
                
    result_label.config(text="This signature did not match any signature in the datasets!")
    return None

find_button = ttk.Button(window, text="Find Signature", command=find_signature)
find_button.grid(column=0, row=1, padx=10, pady=10, sticky='wens')

result_label = ttk.Label(window)
result_label.grid(column=0, row=3, padx=10, pady=10, sticky='wens')

window.geometry("500x375")

window.mainloop()