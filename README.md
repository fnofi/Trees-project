main.py - creates an interactive Python application using the Tkinter and YOLO libraries for analyzing satellite images. The main functions of the application:
1. Satellite image tiles are loaded from the Google Maps API based on coordinates (latitude and longitude) and scale. The images are displayed in a 3x3 grid in the interface.
2. The "Right", "Left", "Top" and "Bottom" buttons allow you to move around the map by changing the coordinates of the images. After changing the coordinates, the updated tiles are loaded from the API and displayed on the screen.
3. The "Predict" button launches the YOLO model, trained to detect trees, on the current set of images. The model analyzes the images, and the results are saved and displayed in the interface.
4. After the prediction, YOLO counts the number of detected trees in all images and displays the result in the interface.

![Trees](https://github.com/user-attachments/assets/f9b66e95-e8b0-4dca-af6a-b7b49f03b2d7)
