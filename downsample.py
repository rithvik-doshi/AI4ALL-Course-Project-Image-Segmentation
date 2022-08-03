# Copyright Rithvik Doshi 2022
# A quick program that downsamples all your photos real quick.

import os, shutil, sys
import cv2

print("Welcome to the downsampler! Let's get you set up!")

final_dir_name = "imgs_down"
some_identifier = "_ds"
extensions = ["jpg", "png"]
noneflag = False

extension = input("What file types are you looking to downsample? Enter a file extension, such as 'jpg' or 'png'\n")
while extension not in extensions:
	extension = input(f"Enter a valid file extension from the following list: {extensions}\n")

print("Aight then, hang on!")

print("Resetting environment...")

if os.path.exists(final_dir_name):
	shutil.rmtree(final_dir_name)
os.mkdir(final_dir_name)

print("Loading all file paths...")

os.system(f'''find . -type f -name "*.{extension}" -print > pathsfile.txt''')

print("Starting the downsampling...")

with open("pathsfile.txt", 'r') as pathsfile:
	listpaths = [i.rstrip() for i in pathsfile.readlines()]
	nums = len(listpaths)
	if nums == 0:
		print(f"No files with the extension `.{extension}` could be found.")
		noneflag = True
	for num, i in enumerate(listpaths):

		# print(num, i, nums)
		base_filename = os.path.basename(i)
		folder = i.replace(base_filename, "").replace('.', "")
		title, ext = os.path.splitext(base_filename)
		# print(final_dir_name, folder, base_filename, title, ext)

		fol_name = final_dir_name + '/' + folder

		if not os.path.exists(fol_name):
			os.makedirs(fol_name)

		final_path = os.path.join(final_dir_name + folder, title + some_identifier + ext)
		# print(final_path)

		image = cv2.imread(i)
		# print(f"Size of image before downsample: {image.shape}")

		# for i in range(num_times_to_downsample):
		image = cv2.pyrDown(image)

		# print(f"Size of image after pyrDown: {image.shape}")

		status = cv2.imwrite(final_path, image)
		
		# print(f"Image written: {status}")

		if not status:
			raise Exception("Image failed to save. Exiting program.\n")

		percent = 100 * ((num+1) / float(nums))

		bar = '#' * int(percent) + '-' * (100-int(percent))

		print(f"{bar} {percent:.2f}%", end = "\r")


print("\nCleaning up...")

if noneflag:
	if os.path.exists(final_dir_name):
		shutil.rmtree(final_dir_name)

os.remove("pathsfile.txt")

print("Cleaning up successful!")

print(f"Sweet you're done! Go check `./{final_dir_name}` to see your photos in a mirrored directory structure. Additionally, your images will be stored with the unique identifier `{some_identifier}` in their names.\n"
	if not noneflag else f"Try running the program again in a directory containing `.{extension}` files.\n")

pathsfile.close()