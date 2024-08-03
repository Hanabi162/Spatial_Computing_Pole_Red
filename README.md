# Vehicle Detection in Specific Areas

## Overview
This project focuses on detecting vehicles in specific areas of an image using OpenCV and NumPy. The script processes images to detect vehicles in different predefined zones and adjusts the processing methods based on whether the image is taken during the day or night. The results are then saved to a SQL Server database.

## Features
- **Vehicle Detection:** Detects and counts vehicles within predefined areas of an image.
- **Spatial Algorithm:** Utilizes spatial algorithms to process images based on the time of day.
- **Day/Night Processing:** Differentiates between day and night processing using brightness levels to apply appropriate detection algorithms.
- **Database Integration:** Saves detection results to a SQL Server database (connection details are abstracted for security).
- **Image Management:** Processes images from a specified directory and deletes them after processing.

## Usage
1. **Prepare Your Images:** Place your images in the designated input folder specified in the `image_folder` variable in the script.

2. **Run the Script:**
    ```bash
    python vehicle_detection.py
    ```

3. **Database Configuration:** Update the database connection details in the script where indicated. Connection details are hidden for security reasons.

4. **Check Results:** The script will process each image, detect vehicles, and save the results to the database. It also prints timestamps and file names of processed images.

## Code Explanation
- **Image Resizing:** The script does not explicitly resize images but processes them directly for vehicle detection.
- **Spatial Algorithm:** 
  - **Daytime Algorithm:** Uses a brightness threshold to determine if the image is taken during the day and applies morphological operations to detect vehicles.
  - **Nighttime Algorithm:** Applies adaptive thresholding and morphological operations to detect vehicles in low-light conditions.
- **Day/Night Detection:** Determines the time of day based on the mean brightness of the image to choose the appropriate detection algorithm.
- **Database Integration:** Results are stored in a SQL Server database. The exact SQL queries are not displayed for security reasons.

## Example Output
- **Daytime Results:** Calculates and prints the percentage of used area and vehicle count for daytime images.
- **Nighttime Results:** Calculates and prints the percentage of used area and vehicle count for nighttime images.

## Troubleshooting
- **Unable to Read Image:** Ensure that the image path is correct and that the image files are not corrupted.
- **Database Connection Issues:** Verify your SQL Server configuration and make sure the connection details are properly configured in the script.
