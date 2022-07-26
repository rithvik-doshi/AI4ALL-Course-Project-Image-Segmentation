import matplotlib.pyplot as plt
import pandas as pd
import data

if __name__ == "__main__":
	data.main()
	df = pd.read_csv("./seg_eval_results/results.csv")
	pc = pd.read_csv("./seg_eval_results/power_consumption.csv")
	# print(df)
	pc = pc.iloc[:, 5]

	pc1 = pc[pc.index.map(lambda x: x%2==0)]
	pc2 = pd.concat([pc, pc1, pc1]).drop_duplicates(keep=False)

	# print(pc1)
	# print(pc2)

	color1 = pc1.map(lambda x: ((x/pc1.max())**6))
	color2 = pc2.map(lambda x: ((x/pc2.max())**6))

	size1 = color1*10**3.5
	size2 = color2*10**3.5

	df_512 = df[df['im_size'] == "512x256"]
	df_1024 = pd.concat([df, df_512, df_512]).drop_duplicates(keep=False)
	
	df_512 = df_512.reset_index()
	df_1024 = df_1024.reset_index()

	df_512 = df_512.iloc[:, 2:]
	df_1024 = df_1024.iloc[:, 2:]

	df_512.drop('im_size', axis = 1, inplace=True)
	df_1024.drop('im_size', axis = 1, inplace=True)

	# print(df_512)
	# print(df_1024)

	X_1 = df_512['miou']
	Y_1 = df_512['speed']
	X_2 = df_1024['miou']
	Y_2 = df_1024['speed']

	plt.scatter(X_1, Y_1, s=size1, c=[[i, 0.5, 0.5] for i in color1])
	plt.xlabel("Mean Intersection-Over-Union")
	plt.ylabel("Speed (ms/f)")
	plt.margins(0.2)
	plt.title("MIOU vs Speed, 512x256 pixels")
	annotations = df_512['s']
	numpc1 = pc1.to_numpy()
	numpc2 = pc2.to_numpy()
	for i, label in enumerate(annotations):
		plt.annotate(f"{label}, {numpc1[i]:.2e} Wh/it", (X_1[i], Y_1[i]))
	plt.savefig('seg_eval_results/MIOU_vs_speed512.png')
	plt.show()

	plt.scatter(X_2, Y_2, s=size2, c=[[i, 0.5, 0.5] for i in color2])
	plt.xlabel("Mean Intersection-Over-Union")
	plt.ylabel("Speed (ms/f)")
	plt.margins(0.2)
	plt.title("MIOU vs Speed, 1024x512 pixels")
	annotations2 = df_1024['s']
	for i, label in enumerate(annotations2):
		plt.annotate(f"{label}, {numpc2[i]:.2e} Wh/it", (X_2[i], Y_2[i]))
	plt.savefig('seg_eval_results/MIOU_vs_speed1024.png')
	plt.show()






