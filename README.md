# Face-Eye-Detection_HaarCascade
Using OpenCV and HaarCascade for face and eye detection in a video input

We used a client-server architecture for the development of this project

Both the server and client were run on a single laptop which had the below configuration. 

HARDWARE -
OS : Windows 10,
Processor : Intel i7,
RAM : 16.0 GB,
Bit : 64-bit operating system


SOFTWARE -
PyCharm Community Edition 2019.3.3


LIBRARIES - 
Python OpenCV - cv2,
socket,
struct, 
pickle,
zlib

To run the project, follow the below steps:
1. First run the file named server.py from pyCharm IDE.
2. Once server starts runnnig, then run the file named client.py from the terminal. Confirm that 
   the location points to the project folder. 
	command : python client.py
3. To stop the process, stop the server from pyCharm.
