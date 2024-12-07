from PIL import Image
import pytesseract as pt
import os

parent_folder = r'D:\00_Project_Saptashati\Gitapess_Images'
file_list = os.listdir(parent_folder)
file_list.sort()

output_data_file = r'D:\00_Project_Saptashati\durgaSaptashati_textOutput_v1.txt'
data_list = []
page_counter = 1

for img_file_name in file_list:
    print(f'{page_counter} - {img_file_name} - Reading Image')
    image_file = f'{parent_folder}\{img_file_name}'

    # ---------------------------------------------------------
    # PyTesseract code
    # ---------------------------------------------------------
    image = Image.open(image_file)
    text = pt.image_to_string(image, lang='hin')
    data_list.append(text)
    print(f'{page_counter} - {img_file_name} - OCR Complete')

    with open(output_data_file, 'w', encoding='utf-8') as file:
        file.writelines(data_list)
        file.writelines(f"--------------------[{page_counter}]--------------------\n")

    print(f'{page_counter} - {img_file_name} - Data loaded in a .txt file')
    page_counter += 1
    # ---------------------------------------------------------


