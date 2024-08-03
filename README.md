# Vehicle Detection in Specific Areas

## Overview
This project is designed to process images for vehicle detection within specific areas using image processing techniques. The script adapts to different lighting conditions and integrates with a SQL Server database to store the detection results. 

## Features
- **Vehicle Detection:** Detects vehicles within predefined areas of the image.
- **Spatial Algorithm:** Utilizes spatial algorithms to analyze and process images based on time of day.
- **Day/Night Processing:** Applies different algorithms for vehicle detection based on brightness.
- **Database Integration:** Saves detection results to a SQL Server database. (Database connection details are abstracted for security reasons.)
- **Image Management:** Processes images from a specified directory and removes them after processing.

## Requirements
- Python 3.x
- OpenCV
- NumPy
- pyodbc

## Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/yourrepository.git
    cd yourrepository
    ```

2. Install the required Python packages:
    ```bash
    pip install opencv-python numpy pyodbc
    ```

3. Ensure that you have a SQL Server instance running and configure the connection details in the script.

## Usage
1. **Prepare Your Images:** Place your images in the designated input folder (`image_folder`).

2. **Run the Script:**
    ```bash
    python vehicle_detection.py
    ```

3. **Database Configuration:** Configure your database connection details in the script where indicated. The connection details are hidden in this script for security reasons.

4. **Check Results:** The script processes images, detects vehicles, and saves results to the database. It prints timestamps and file names of processed images.

## Code Explanation
- **Image Resizing:** Scales images to improve processing efficiency.
- **Spatial Algorithm:** Applies spatial processing to detect vehicles within specific areas of the image.
- **Day/Night Detection:** Adjusts vehicle detection methods based on the image's brightness.
- **Database Integration:** Stores results in a SQL Server database. (Note: Connection details are not included in this script for security reasons.)

## Example Output
The script outputs vehicle detection results in percentage terms, depending on whether the images are taken during the day or night.

## Troubleshooting
- **Image Not Read:** Ensure the image path is correct and the file is not corrupted.
- **Database Connection Errors:** Verify your SQL Server configuration and connection details.

