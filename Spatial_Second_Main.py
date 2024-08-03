import cv2
import numpy as np
import os
import time
import pyodbc
from pathlib import Path
from Database_connect import db_server,db_database,db_username,db_password,sys_info # Secret

image_folder = r"C:\Users\ARoumpattana\Desktop\OCR\KP_OCR\Spatial_Computing_VSCODE_Pole_Red\Dataset_Pole_Red"

        
def Spatial_Computing_Pole_Red(image):
    # Polyline แบบเต็มพิกัด
    verticesAll = np.array([[0, 420], [330, 310], [790, 420], [1200,520], [1650,650],
                            [2000,780], [2100,830], [2800,1150], [2700,2100], [1500, 2100],
                        [950,2050], [420,1375], [290,1220]], dtype=np.int32)
    
    verticesSecOne = np.array([[0, 420], [330, 310], [790, 420], 
                            [750, 500],
                            [100, 700]], dtype=np.int32)

    verticesSecMid = np.array([[100,700], [750,500], [790,420], [1200,520], [1650,650], [2000,780], [2100,830], 
                            [1500,2100], 
                            [950,2050], [420,1375], [290,1220]], dtype=np.int32)
    
    verticesSecTwo = np.array([[2100, 830], [2800, 1150],
                            [2700, 2100], [1500, 2100]], dtype=np.int32)


    Sky = np.array([[0,250], [160,190], [180,150], [250,130], [290,100], [330,110], [550,30], [850,30], [880,50], [1400,30],
                        [1600,50],[1800,86],[2000,115],[2700,300],[2700,0],[0,0]], dtype=np.int32)
    
    def draw_Polylines(image, points, color, thickness):
        cv2.polylines(image, [points.reshape((-1, 1, 2))], True, color, thickness)
        # for point in points:
        #         cv2.circle(image, tuple(point), 10, (0, 255, 0), -1)

    #draw_Polylines(image, verticesAll, (0, 0, 255), 5)
    draw_Polylines(image, Sky, (0, 0, 255), 5)

    mask_All = np.zeros_like(image[:, :, 0], dtype=np.uint8)
    cv2.fillPoly(mask_All, [verticesAll], 255)
    mask_Sky = np.zeros_like(image[:, :, 0], dtype=np.uint8)
    cv2.fillPoly(mask_Sky, [Sky], 255)

    combined_mask = cv2.bitwise_or(mask_All, mask_Sky)
    masked_image = cv2.bitwise_and(image, image, mask=combined_mask)
    
    mean_brightness = np.mean(image[combined_mask==255])
    print(f"Mean brightness: {mean_brightness:.2f}")
        
    if mean_brightness >= 100:
        def Section1():
            maskSecOne = np.zeros_like(image[:, :, 0])
            cv2.fillPoly(maskSecOne, [verticesSecOne], 255)  # เอาแค่พื้นที่ใน Polyline SecOne
            masked_image_sec_one = cv2.bitwise_and(image, image, mask=maskSecOne)  # ประมวลผลภาพเฉพาะพื้นที่ SecOne
            draw_Polylines(image, verticesSecOne, (255, 0, 0), 5)
            print("Day time Algorithm")
            
            gray_image_sec_one = cv2.cvtColor(masked_image_sec_one, cv2.COLOR_BGR2GRAY)
            _, thresholded_image_sec_one = cv2.threshold(gray_image_sec_one, 125, 255, cv2.THRESH_BINARY)

            kernel = np.ones((1, 1), np.uint8)
            morphed_image_sec_one = cv2.morphologyEx(thresholded_image_sec_one, cv2.MORPH_CLOSE, kernel)
            morphed_image_sec_one = cv2.morphologyEx(morphed_image_sec_one, cv2.MORPH_OPEN, kernel)
                        
            containers = []
            contours, _ = cv2.findContours(morphed_image_sec_one, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if  1500<= area <=50000:
                    rect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)

                    cv2.drawContours(image, [box], 0, (0, 0, 255), 5)
                    containers.append(box)
                        
            container_area_sec_one = sum([cv2.contourArea(contour) for contour in containers])
            return maskSecOne, container_area_sec_one, morphed_image_sec_one

        def Sectionmid():
            maskSecMid = np.zeros_like(image[:, :, 0])
            cv2.fillPoly(maskSecMid, [verticesSecMid], 255)
            masked_image_sec_mid = cv2.bitwise_and(image,image,mask=maskSecMid)
            draw_Polylines(image, verticesSecMid, (0, 255, 255), 5)
            
            gray_image_sec_mid = cv2.cvtColor(masked_image_sec_mid, cv2.COLOR_BGR2GRAY)
            _, thresholded_image_sec_mid = cv2.threshold(gray_image_sec_mid, 95, 255, cv2.THRESH_BINARY)

            kernel = np.ones((1, 1), np.uint8)
            morphed_image_sec_mid = cv2.morphologyEx(thresholded_image_sec_mid, cv2.MORPH_CLOSE, kernel)
            morphed_image_sec_mid = cv2.morphologyEx(morphed_image_sec_mid, cv2.MORPH_OPEN, kernel)

            containers = []
            contours, _ = cv2.findContours(thresholded_image_sec_mid, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if 20000 <= area <= 780000:
                    rect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
    
                    cv2.drawContours(image, [box], 0, (0, 0, 255), 5)
                    containers.append(box)

            container_area_sec_mid = sum([cv2.contourArea(contour) for contour in containers])
            
            return maskSecMid, container_area_sec_mid, morphed_image_sec_mid

        def Section2():
            maskSecTwo = np.zeros_like(image[:, :, 0])
            cv2.fillPoly(maskSecTwo, [verticesSecTwo], 255)  # เอาแค่พื้นที่ใน Polyline SecTwo
            masked_image_sec_two = cv2.bitwise_and(image, image, mask=maskSecTwo)  # ประมวลผลภาพเฉพาะพื้นที่ SecTwo
            draw_Polylines(image, verticesSecTwo, (0, 255, 0), 5)
            
            gray_image_sec_two = cv2.cvtColor(masked_image_sec_two, cv2.COLOR_BGR2GRAY)
            _, thresholded_image_sec_two = cv2.threshold(gray_image_sec_two, 80, 255, cv2.THRESH_BINARY)

            kernel = np.ones((2, 2), np.uint8)
            morphed_image_sec_two = cv2.morphologyEx(thresholded_image_sec_two, cv2.MORPH_CLOSE, kernel)
            morphed_image_sec_two = cv2.morphologyEx(morphed_image_sec_two, cv2.MORPH_OPEN, kernel)
            
            return maskSecTwo, morphed_image_sec_two
        
        maskSecOne, container_area_sec_one, morphed_image_sec_one = Section1()
        maskSecMid, container_area_sec_mid, morphed_image_sec_mid = Sectionmid()
        maskSecTwo, morphed_image_sec_two = Section2()
    
        # นับจำนวนพิกเซลที่มีค่า 255 (พื้นที่ว่าง) ภายใน Polyline
        empty_pixel_count_sec_one = cv2.countNonZero(morphed_image_sec_one & maskSecOne) - container_area_sec_one
        empty_pixel_count_sec_mid = cv2.countNonZero(morphed_image_sec_mid & maskSecMid) - container_area_sec_mid
        empty_pixel_count_sec_two = cv2.countNonZero(morphed_image_sec_two & maskSecTwo)
        
        # คำนวณพื้นที่
        total_pixel_count_sec_one = cv2.countNonZero(maskSecOne)
        total_pixel_count_sec_mid = cv2.countNonZero(maskSecMid)
        total_pixel_count_sec_two = cv2.countNonZero(maskSecTwo)
    
        percentages = [
            (empty_pixel_count_sec_one / total_pixel_count_sec_one) * 20,
            (empty_pixel_count_sec_mid / total_pixel_count_sec_mid) * 75,
            (empty_pixel_count_sec_two / total_pixel_count_sec_two) * 5
        ]
        day_empty_percentage = sum(percentages)
        day_empty_percentage = 0 if day_empty_percentage < 0 else day_empty_percentage
    
        day_used_area = (100 - day_empty_percentage)
        day_used_area = 100 if day_used_area > 100 else day_used_area
    
        day_Triyangyas = (day_used_area * 28) / 100
        day_Triyangyas = 28 if day_Triyangyas > 28 else day_Triyangyas
        day_Triyangyas = int(day_Triyangyas)
        return {
                    'time': 'day',
                    'day_Triyangyas': day_Triyangyas
        }
        
    else:
        def Section1():
            maskSecOne = np.zeros_like(image[:, :, 0])
            cv2.fillPoly(maskSecOne, [verticesSecOne], 255)  # เอาแค่พื้นที่ใน Polyline SecOne
            masked_image_sec_one = cv2.bitwise_and(image, image, mask=maskSecOne)  # ประมวลผลภาพเฉพาะพื้นที่ SecOne
            draw_Polylines(image, verticesSecOne, (255, 0, 0), 5)
            print("Night time Algorithm")
            
            gray_image_sec_one = cv2.cvtColor(masked_image_sec_one, cv2.COLOR_BGR2GRAY)
            adaptive_thresh_sec_one = cv2.adaptiveThreshold(gray_image_sec_one , 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 9, 7)

            kernel = np.ones((50, 50), np.uint8)
            morphed_image_sec_one = cv2.morphologyEx(adaptive_thresh_sec_one, cv2.MORPH_CLOSE, kernel)
            morphed_image_sec_one = cv2.morphologyEx(morphed_image_sec_one, cv2.MORPH_OPEN, kernel)
            
            return maskSecOne, morphed_image_sec_one

        def Sectionmid():
            maskSecMid = np.zeros_like(image[:, :, 0])
            cv2.fillPoly(maskSecMid, [verticesSecMid], 255)
            masked_image_sec_mid = cv2.bitwise_and(image,image,mask=maskSecMid)
            draw_Polylines(image, verticesSecMid, (0, 255, 255), 5)
            
            gray_image_sec_mid = cv2.cvtColor(masked_image_sec_mid, cv2.COLOR_BGR2GRAY)
            adaptive_thresh_sec_mid = cv2.adaptiveThreshold(gray_image_sec_mid, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 9, 9)

            kernel = np.ones((40, 40), np.uint8)
            morphed_image_sec_mid = cv2.morphologyEx(adaptive_thresh_sec_mid, cv2.MORPH_CLOSE, kernel)
            morphed_image_sec_mid = cv2.morphologyEx(morphed_image_sec_mid, cv2.MORPH_OPEN, kernel)

            return maskSecMid,  morphed_image_sec_mid

        def Section2():
            maskSecTwo = np.zeros_like(image[:, :, 0])
            cv2.fillPoly(maskSecTwo, [verticesSecTwo], 255)  # เอาแค่พื้นที่ใน Polyline SecTwo
            masked_image_sec_two = cv2.bitwise_and(image, image, mask=maskSecTwo)  # ประมวลผลภาพเฉพาะพื้นที่ SecTwo
            draw_Polylines(image, verticesSecTwo, (0, 255, 0), 5)
            
            gray_image_sec_two = cv2.cvtColor(masked_image_sec_two, cv2.COLOR_BGR2GRAY)
            adaptive_thresh_sec_two = cv2.adaptiveThreshold(gray_image_sec_two, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 7, 7)

            kernel = np.ones((50, 50), np.uint8)
            morphed_image_sec_two = cv2.morphologyEx(adaptive_thresh_sec_two, cv2.MORPH_CLOSE, kernel)
            morphed_image_sec_two = cv2.morphologyEx(morphed_image_sec_two, cv2.MORPH_OPEN, kernel)
            
            return maskSecTwo, morphed_image_sec_two

        maskSecOne, morphed_image_sec_one = Section1()
        maskSecMid, morphed_image_sec_mid = Sectionmid()
        maskSecTwo, morphed_image_sec_two = Section2()
        
        # นับจำนวนพิกเซลที่มีค่า 255 (พื้นที่ว่าง) ภายใน Polyline
        used_pixel_count_sec_one = cv2.countNonZero(morphed_image_sec_one & maskSecOne)
        used_pixel_count_sec_mid = cv2.countNonZero(morphed_image_sec_mid & maskSecMid)
        used_pixel_count_sec_two = cv2.countNonZero(morphed_image_sec_two & maskSecTwo)

        # คำนวณพื้นที่
        total_pixel_count_sec_one = cv2.countNonZero(maskSecOne)
        total_pixel_count_sec_mid = cv2.countNonZero(maskSecMid)
        total_pixel_count_sec_two = cv2.countNonZero(maskSecTwo)

        percentages = [
            (used_pixel_count_sec_one / total_pixel_count_sec_one) * 45,
            (used_pixel_count_sec_mid / total_pixel_count_sec_mid) * 45,
            (used_pixel_count_sec_two / total_pixel_count_sec_two) * 20
        ]
        night_used_area = sum(percentages)
        
        night_empty_percentage = 100 - night_used_area
        night_Triyangyas = (night_used_area*28)/100

        night_used_area = 100 if night_used_area > 100 else night_used_area
        night_Triyangyas = 28 if night_Triyangyas > 28 else night_Triyangyas
        night_empty_percentage = 0 if night_empty_percentage < 0 else night_empty_percentage
        night_empty_percentage = 100 if night_empty_percentage > 100 else night_empty_percentage

        night_Triyangyas = int(night_Triyangyas)
        return {
                'time': 'night',
                'night_Triyangyas': night_Triyangyas
        }
        

def read_images(image_folder):
    source = Path(image_folder)
    cctv_id = os.path.basename(source)[:11]
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+db_server+';DATABASE='+db_database+';UID='+db_username+';PWD='+ db_password)
    cursor = cnxn.cursor()
    
    if os.path.exists(image_folder):
        while True:
            try:
                files = os.listdir(image_folder)
                if not files:
                    print("Waiting for new images to be added...")
                    time.sleep(2)
                    continue
                
                processed_image_count = 1
                for file in files:
                    image_path = os.path.join(image_folder, file)
                    image = cv2.imread(image_path)
                    if image is None:
                        print(f"Unable to read image: {image_path}")
                        continue
                    
                    print(f"Image No.: {processed_image_count}")
                    result = Spatial_Computing_Pole_Red(image)
                    if result['time'] == 'day':
                        Triyangyas = result['day_Triyangyas']
                    else:
                        Triyangyas = result['night_Triyangyas']
                    
                    otran_sqlstr_1 = f"INSERT INTO OCR_TRANSACTIONS (otrans_id,otrans_cctv_id,otrans_source_path,otrans_source_name,otrans_sys_info"
                    otran_sqlstr_2 = f",otrans_detects) VALUES (NEXT VALUE FOR OTRANS_SEQ,'" + cctv_id + "','" + str(source) + "','" + os.path.basename(image_path) + "','" + str(sys_info) + "','" + str(Triyangyas) + "'"
                    otran_sqlstr_3 = f")"
                    otran_sqlstr = otran_sqlstr_1 + otran_sqlstr_2 + otran_sqlstr_3
                    
                    print(otran_sqlstr)
                    cursor.execute(otran_sqlstr)
                    processed_image_count += 1
                    time.sleep(2)
                    os.remove(image_path)
                
                cnxn.commit()
            except Exception as e:
                print(f"Error: {e}")
    else:
        print("The specified folder does not exist.")
    
    cursor.close()
    cnxn.close()

read_images(image_folder)
