import os
import cv2
import face_recognition
import face_recognition as fr
import numpy as np
from tkinter import filedialog
from tkinter import *


# Function to get encoded faces from the face repository
def get_encoded_faces():
    encoded = {}

    # Walk through the face_repository directory
    for dirpath, dnames, fnames in os.walk("./face_repository"):
        # For each file in the directory
        for f in fnames:
            # If the file is a.jpg or.png
            if f.endswith(".jpg") or f.endswith(".png"):
                # Load the image file
                face = fr.load_image_file("face_repository/" + f)
                # Get the face encoding
                encoding = fr.face_encodings(face)[0]
                # Store the encoding in the encoded dictionary with the filename as the key
                encoded[f.split(".")[0]] = encoding

    return encoded


# Function to encode an unknown image
def unknown_image_encoded(img):
    # Load the image file
    face = fr.load_image_file("face_repository/" + img)
    # Get the face encoding
    encoding = fr.face_encodings(face)[0]

    return encoding


# Function to classify faces in an image
def classify_face(im):
    # Get the encoded faces from the face repository
    faces = get_encoded_faces()
    # Get the list of encoded faces
    faces_encoded = list(faces.values())
    # Get the list of known face names
    known_face_names = list(faces.keys())

    # Load the image file
    img = cv2.imread(im, 1)

    # Get the face locations in the image
    face_locations = face_recognition.face_locations(img)
    # Get the unknown face encodings
    unknown_face_encodings = face_recognition.face_encodings(img, face_locations)

    # Initialize an empty list to store the names of the faces
    face_names = []

    # For each unknown face encoding
    for i, face_encoding in enumerate(unknown_face_encodings):
        # Compare the unknown face encoding to the known face encodings
        matches = face_recognition.compare_faces(faces_encoded, face_encoding)
        # Initialize the name of the face as unknown
        name = "Unknown Civilian"

        # Calculate the face distances
        face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
        # Get the index of the best match
        best_match_index = np.argmin(face_distances)
        # If the best match is a match
        if matches[best_match_index]:
            # Set the name of the face to the name of the best match
            name = known_face_names[best_match_index]

        # Get the face location
        (top, right, bottom, left) = face_locations[i]

        # Adjust the rectangle's width and height
        if name == "Unknown Civilian":
            cv2.rectangle(img, (left, top), (right, bottom), (255, 0, 0), 2)
        else:
            cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)

        # Add the name of the face to the list of face names
        face_names.append(name)

        # For each face location and name
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Draw a rectangle around the face
            if name == "Unknown Civilian":
                cv2.rectangle(img, (left, top), (right, bottom), (255, 0, 0), 2)
            else:
                cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a filled rectangle below the face
            if name == "Unknown Civilian":
                cv2.rectangle(img, (left, bottom), (right, bottom + 15), (255, 0, 0), cv2.FILLED)
            else:
                cv2.rectangle(img, (left, bottom), (right, bottom + 15), (0, 0, 255), cv2.FILLED)
            # Set the font
            font = cv2.FONT_HERSHEY_DUPLEX
            # Add the name of the face to the image
            cv2.putText(img, name, (left, bottom + 10), font, 0.5, (300, 300, 300), 1)

    # Display the image
    while True:
        cv2.imshow('Detecting criminals...', img)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            return face_names


# Create a tkinter window
root = Tk()
root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                           filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

# Print the names of the faces in the selected
face_names = classify_face(root.filename)
known_faces = [name for name in face_names if name != "Unknown Civilian"]
print('Detected criminals faces : \n', known_faces)

# Close the tkinter window
root.destroy()
