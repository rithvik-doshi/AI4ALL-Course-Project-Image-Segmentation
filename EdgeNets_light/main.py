import matplotlib.pyplot as plt
import pandas as pd
# import data

# HEY EVERYONE!

# Just remember, if you ever feel lost, ask your peers, ask me or ask the internet!

if __name__ == "__main__":

	# OUR GOAL: To create a graph that models our MIOU (Mean Intersection over Union - accuracty) vs Speed of execution
	# for several different parameters, and also see how much power each test consumes.
	
	# First, we would usually run the test on the ML model. We don't have to do this since we already have the results,
	# but this is the command we would normally use:

	# data.main()

	# Now, write some code to load two files into dataframes: results.csv and power_consumption.csv, both found in the
	# seg_eval_results folder

	# df = ________
	# pc = ________

	# print(df.head(), pc.head())

	# --------------------------------------------------------------------------------------------------------------- #

	# Let's take some of the power consumption data and add it to the results dataframe. We want the sixth column
	# titled Wh/it, and we don't need the rest, so we can just redefine pc. Remember, we will be using the pc to
	# determine the size and color of the data points. To do this, take a look at the iloc function in pandas
	# and how it works

	# pc = _______

	# Next, we will organize our data points into two graphs by the image size that we evaluate the model at. The data
	# was collected in a specific order, where we want to group all rows with even indices together in one column, and
	# all rows with odd indices into another.

	# pc1 = _______
	# pc2 = _______

	# Optional, but you can print the data at each step to make sure it's evaluating correctly

	# print(pc1)
	# print(pc2)

	# If you take a look at this data, it seems to be very spread out and small in value. So, if we try to visualize
	# these values at scale, we will not necessarily be able to spot any differences. So, what can we do to exaggerate
	# the differences between the points is by normalizing and transforming the data points. Write some code where,
	# for each point in pc1 or pc2, we divide it by the max value in pc1 or pc2 (hence normalizing the data between 0
	# and 1) and then exponentiating it to the 6th power (remember, when we exponentiate two different numbers, their
	# difference becomes greater? So by exponentiating with a really high power, we are increasing their differences)

	# color1 = ________
	# color2 = ________

	# Next, we also want to create two vectors that dictate the size of the data points. Write some code to multiply
	# the color data by 10 and exponentiate by 3.5 (trust me, this looks weird now but it looks very nice on a graph)

	# size1 = ________
	# size2 = ________

	# --------------------------------------------------------------------------------------------------------------- #

	# Now, we will pivot to extracting the test results. Write code that separates the dataframe by the different
	# image sizes: either "512x256" or "1024x512".

	# df_512 = ________
	# df_1024 = ________
	
	# If you call the head or tail function on either of the new dataframes, you may notice that the indices look a
	# little messed up. Find and apply a function that resets the indices of each dataframe.

	# df_512 =
	# df_1024 = 

	# A couple of these functions create some vestigial columns due to some of these functions. Don't change the
	# code below:

	# df_512 = df_512.iloc[:, 2:]
	# df_1024 = df_1024.iloc[:, 2:]

	# Next, we don't need to keep the image size column now that the data is pretty evenly split up. Write code to
	# drop the im_size column in each dataframe. Look up the drop function, what it does and how to use it.

	# df_512.drop(stuff_goes_here)
	# df_1024.drop(stuff_goes_here)

	# print(df_512)
	# print(df_1024)

	# Finally, before we start plotting the results data, we need to figure out what our X and Y variables are. Write
	# some code to assign the miou data to X and the speed data to Y, for each df that we're working with.

	# X_1 = ________
	# Y_1 = ________
	# X_2 = ________
	# Y_2 = ________

	# --------------------------------------------------------------------------------------------------------------- #

	# Great! Now here comes the fun part: let's take the data and plot it! We will be using matplotlib functions
	# to create two scatterplots, label each axis and title the plots, annotate each point, save the figure and show
	# it. So, let's do that!

	# First, use plt.scatter() to create a scatter plot. Look up the documentation and see how you can pass the
	# different parameters in to change the characteristics of the graph. We want to include the X, Y, size and color
	# as parameters. The X_1, Y_1 and size1 parameters should be easy to plug in, but for color, we want to enter a
	# list of [R, G, B], where R, G and B each are numbers between 0 and 1. We want to create a list of these [R, G, B]
	# lists where the R value is dependent on the value in the color1 list.

	# plt.scatter(_____, _____, s = ______, c = ______)

	# Next, create an xlabel, ylabel and title for the plot. To give you some context, the MIOU is a ratio (so what
	# does that mean for the range of values?) and the Speed is measured in ms/f (miliseconds per figure, figure is
	# each image that the ML model processed). Finally, come up with a title that compares the X and Y axes, and
	# identifies the plot with the specific image size we are working with.

	# plt.xlabel()
	# plt.ylabel()
	# plt.title()

	# Then, set the margins of the plot to 0.2, for better spacing.

	# plt.margins()

	# Now we're going to annotate each image with some details, namely the model scales that we used for each test
	# and the power consumption for each test. First, create a variable that stores all the values in the 's' column:

	# annotations = 

	# Next, convert pc1 and pc2 to numpy arrays so that they become numerical data, which we can format cleanly.

	# numpc1 = 
	# numpc2 = 

	# Now, for each data point, we want to create an annotation using plt.annotation. Look up plt.annotate, try to
	# figure out how it works, and see if you can come up with a way to annotate each point as so:

	# {s_value}, {power_value in scientific notation and to 2 decimal places} Wh/it

	# for i, label in enumerate(annotations):
	# 	plt.annotate(f"{label}, {numpc1[i]:.2e} Wh/it", (X_1[i], Y_1[i]))

	# We are pretty much done! Now, save the figure to the folder, seg_eval_results with the name: MIOU_vs_speed512.png
	# Look up a function that will help you do this!

	# _____________

	# Now, all you have left to do is run plt.show() to show the plot to you!

	# plt.show()

	# --------------------------------------------------------------------------------------------------------------- #

	# Yay, you've done one plot! Now, do the same thing for the second plot:

	# 
	# 
	# 
	# 
	# 
	# 
	# 

	# Good stuff! Now you're a pro at visualizing data!

