# Image Segmentation

## What is image segmentation?

When you look at a picture, you can recognize individual objects that occur in the picture, right? As in, we look at the region of pixels that make up a pencil and we understand that, through our own intuition, that is a pencil. Now, how can we get a machine learning model to do this? Well, we can come up with a list of different objects that we want to classify, such as a book, a pencil, and an apple. Then, we can give the model a dataset of before and after pictures, where we highlight the books, apples, and pencils in each photo. We can train the model on this data to get it to recognize a book, pencil or apple and then highlight it accordingly. This is image segmentation in a nutshell.

Feel free to check out some articles regarding image segmentation:

## Activity: Try out image segmentation

In order to try this out, let's pretend we're creating the training set for an image segmenation database. What that means is taking an image and coloring over the objects with their specific color. Here's how we're going to do that:

1. Open up the test_segmentation.py file. Towards the top, you'll notice two lists: one that lists all the names of the classes, and one that lists each color used to segment that object in [R, G, B] format. You can refer back to this, or make a note of this data somewhere convenient.
2. Next, open up one of the normal example images (should be a first person view of a road and other objects) in a paint editor. You can either do this online or on your desktop.
3. Now go through and color this image according to the lists. Imagine this is like a coloring the numbers activity :D
4. When you're done, compare your result to the sample solution given. What are some of the differences between what you did and what was given?
