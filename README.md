# Fringe_Tracer
Python code to convert raw interferograms into traced PNG files which can be used with the MAGIC2 interferometry code. Some manual postprocessing is still required, but it is much faster than manually tracing the interferograms

Please note this code is not guaranteed to work for all interferograms, and may in some case give erroneous results. Always confirm the traced fringes match the fringes in your raw data.

User guide:

1. Externally ensure the raw interferogram has high contrast. I like to use ImageJ's Enhance Contrast tool, setting saturated pixels to 0.35% and checking the Normalize option.

2. Run Fringe_Tracer.py, and select the raw interferogram when prompted by the first dialog box. I have tested the program with 8-bit TIFF input files, but it should be able to handle several other formats as well.

3. Watch the progress bar slowly advance. It takes about 3 minutes to run on my computer; obviously the speed will heavily depend on your local machine's specifications.

4. Once the processing is completed, the traced interferogram will be displayed. Once you have inspected the resulting image, close it so the code will continue running.

5. If you are satisfied with the results, select 'yes' to save the file when prompted.

6. The image can be saved in basically any format; it will be saved as an 8-bit image regardless of file type. If you intend to use the image with MAGIC2, it must be a PNG

7. To use with MAGIC2, you will need to do a bit of manual postprocessing. This will include masking, as well as ensuring fringes do not connect. When fringes in the raw interferogram get closer than about 10 px apart, the fringe tracing algorithm can in some cases connect those two fringes. Simply drawing a white line through the connection between the fringes should separate them enough for MAGIC2. In addition, some fringes may be incomplete; these should be connected prior to use with MAGIC2.

8. Enjoy!
