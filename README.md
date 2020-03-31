# HumanMouse

This is the official code repository for 'HumanMouse'. This gesture based screen navigation platform was developed for the CSE 314: Digital Image Processing course at SRM University, AP.

### Team

* [Tuhin Sarkar](https://7uhinn.github.io/)
* [Aayusi Biswas](https://github.com/Aayusi)
* [Khushboo Maheshwari](https://github.com/Khushboomah8)

#### Overview

In these times of COVID-19 pandemic, everybody has been locked down inside their homes. In such a situation, where droplets containing the virus are transmitted through touch, it is better to avoid touching anything at all, even computer mice. Often in a software development environment, many developers work together utilizing the mouse whenever they feel so, often for longer durations. We neither know if this set of people is hygienic nor whoever/whatever they have touched through their bare hands.

Therefore, we decided to build a platform that takes in real-time videos of the finger gestures and performs mouse operations corresponding to them. In order to build that, we focused on four main things:

* Image Acquisition\
Through the *wxpython* library we make use of the webcam to produce frames of images in real-time. All operations henceforth are applied to each input image.

* Color Detection\
We started with writing a python script that uses *OpenCV* among other libraries to facilitate color recognition. This was done to recognize the color of the sellotape wrapped to the finger. This will later help in segmentation.

* Image Enhancement and Morphological Operations\
Firstly, every image is converted from RGB format to HSV (Hue, Saturation, Value) format in order to better detect the color. This is done because colors in the RGB colorspace are coded using the three channels, hence, it is more difficult to segment an object in the image based on its color.  For this application, we are using shades of blue color as the target color range as the tape used is of blue color. However, you can use your own range as per the color of your sellotape.

  We create a primitive 'mask', i.e. an 8-bit binary image that renders 255 value to pixels falling under the given color range and 0 otherwise. However, this mask is extremely noisy and contains a lot more regions not required for segmentation. Here is where we apply Morphological Operations.

  We use mainly two compound Morphological Operations: Opening (Erosion and then Dilation) and Closing (Dilation and then Erosion). Opening removes small objects from the foreground (usually taken as the bright pixels) of an image, placing them in the background i.e. remove unwanted noise. While closing removes small holes in the foreground, changing small islands of background into the foreground i.e. forming solid masks without noise in the foreground.

  This gives us a noise-free mask for segmentation.

* Contour Segmentation and Numbering\
The mask generated is element-wise multiplied to the original HSV image and the segmented region is obtained in the image. This segmented region or AOI (Area of Interest) is referred to as contour here. There might be multiple contours in the same image. Hence the coordinates of each contour are saved in a 2D array.

* Corresponding Mouse Operation\
As aforementioned, real-time images are taken and processed in a fraction of second to give an *illusion* of real-time video capture. However, the relationship between the contour coordinates in each image defines what mouse operation is to be performed. 

  If 2 different contours (i.e. 2 fingers) are segmented, then traversal mode is activated, ie the position of the mouse can be manipulated (without holding). The Euclidean displacement of the center of the line joining the centers of the 2 contours between adjacent frames is calculated. This displacement (distance along with direction) is then translated into the size of the screen resolution. This is how the new position of the cursor is calculated. The actual movement of the cursor, however, happens with the help of *pynput* library.

  Similarly, If 1 large contour (i.e. 2 fingers pinching) is segmented, then left-click mode is activated, ie the file the cursor was pointing at is selected, if the contour is moved, the file is held and hence also moves.

  If 3 different contours (i.e. 3 fingers) are segmented, then right-click mode is activated, ie the file the cursor was pointing at is selected and right-click options are revealed.

  Finally, if 4 different contours (i.e. 4 fingers) are segmented, then double click mode is activated, ie the file the cursor was pointing at is selected and opened.

  P.S: To better understand this, please go through the video hyperlinked below.

#### Technology used

Dependencies:
* Python
* OpenCV
* Numpy
* pynput
* wxpython

Domains:
* Digital Image Processing
* Computer Vision
* Human Computer Interaction

#### Screenshots/Demo Video

To perform 'Traversal' i.e. changing position of cursor:

![Traversal](/images/t.png)

To perform 'Left Click':

![Left Click](/images/lc.png)

To perform 'Right Click':

![Right Click](/images/rc.png)

To perform 'Double Click':

![Double Click](/images/dc.png)

[Have a look at this demonstrative video.](https://drive.google.com/file/d/1SmrQV--efjpGY_e_8KmGJCTrvZoW0g2r/view?usp=sharing)

#### Usage

1. Clone this repository. 

```git clone https://github.com/7uhinn/HumanMouse```   

2. Move into the cloned repository.

```cd HumanMouse```

3. If you don't already have the required libraries: run this command 

```pip3 install -r requirements.txt```

* The required dependencies will be installed.

4. Now, apply sellotape to the both the index fingers, middle finger of one hand and the thumb of the other. After that run this command

```python3 mouse.py```

* Perform aforementioned gestures to perform corresponding mouse operations.
