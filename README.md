# Images Mixer and Viewer

## Team Members:
- Sondos Mahmoud
- Fatma Ehab
- Mai Mohamed
- Noura Osama

## Project Overview:

### Images Viewer:
The project aims to create an Images Viewer with advanced functionalities for manipulating and viewing grayscale images. The key features include:

1. **Open and View Images:**
    - The ability to open and view four grayscale images, each in a separate "viewport."
    - If a colored image is opened, the program should automatically convert it to grayscale.

2. **FT Components Display:**
    - For each image, there are two displays:
        - A fixed display for the image.
        - A secondary display that can show various components (FT Magnitude, FT Phase, FT Real, FT Imaginary) based on a combo-box selection.
    - Users can easily browse and change any image by double-clicking on its viewer.

### Mixer and Output:

3. **Output Viewports:**
    - Two output viewports for displaying the mixer result.
    - Users can control in which viewport the new mixer result will be shown.

4. **Brightness/Contrast Adjustment:**
    - Users can change the brightness/contrast  of any image viewport via mouse dragging.
    - Brightness/contrast adjustments can be applied to any of the four components individually.

### Components Mixer:

5. **Weighted Average:**
    - The output image is the inverse Fourier transform (ifft) of a weighted average of the Fourier transforms of the input four images.
    - Customizable weights for each image's Fourier transform via sliders.

### Regions Mixer:

6. **Region Selection:**
    - For each FT component, users can select the region (inner or outer) that will be considered for the output.
    - Selection is done by drawing a rectangle on each FT, with options to include the inner or outer region.
    - The size or percentage of the region rectangle is customizable via a slider.
    - The selected region is unified for all four images.

## Usage Guidelines:

- Double-click on an image viewer to browse and change the image.
- Use combo-box to select FT components for display.
- Adjust brightness/contrast by dragging the mouse.
- Customize weights for the Fourier transforms via sliders.
- Draw rectangles on FTs for region selection.
- Utilize progress bar for real-time feedback during mixing operations.
