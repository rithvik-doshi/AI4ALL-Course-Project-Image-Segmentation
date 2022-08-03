import test_segmentation as ts
import pandas as pd
import os, shutil

# A quick overview of how we are collecting the data

def main():
	df = pd.DataFrame() # Create a dataframe
	S_RANGE = [0.5, 1.0, 1.5, 2.0] # Range of the different sizes for the ESPN model
	DIM_RANGE = [[512, 256], [1024, 512]] # Range of different image dimensions used
	count = 1
	for i in S_RANGE:
		for j in DIM_RANGE: # Iterating over each possible combination of the dimensions:
				print(f"Round {count} Settings: {i}, {j}")
				results = ts.alt_start(i, j) # This function calles the test_segmentation file and starts a test with the selected
											 # parameters
				dftemp = pd.DataFrame([results]) # The result is a JSON object (not important but you can look it up for more info)
												 # which is then inserted into a dataframe
				df = pd.concat([df, dftemp], ignore_index=True) # Concatenate each row
				print(df)
				print("Next Iteration...")
				count += 1

	# Saving the data

	if os.path.isdir("./seg_eval_results"):
		shutil.rmtree("./seg_eval_results")
	os.mkdir("./seg_eval_results")
	df.to_csv('./seg_eval_results/results.csv')
