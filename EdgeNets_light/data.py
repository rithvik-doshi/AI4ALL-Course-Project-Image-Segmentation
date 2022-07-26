import test_segmentation as ts
import pandas as pd
import os, shutil

def main():
	df = pd.DataFrame()
	S_RANGE = [0.5, 1.0, 1.5, 2.0]
	DIM_RANGE = [[512, 256], [1024, 512]]
	count = 1
	for i in S_RANGE:
		for j in DIM_RANGE:
				print(f"Round {count} Settings: {i}, {j}")
				results = ts.alt_start(i, j)
				dftemp = pd.DataFrame([results])
				df = pd.concat([df, dftemp], ignore_index=True)
				print(df)
				print("Next Iteration...")
				count += 1

	if os.path.isdir("./seg_eval_results"):
		shutil.rmtree("./seg_eval_results")
	os.mkdir("./seg_eval_results")
	df.to_csv('./seg_eval_results/results.csv')
