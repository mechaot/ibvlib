# IBV Library

Common functions used in the Lecture "Image Processing I: Industrial Imaging" at Leibniz Universität Hannover, Germany

* Camera
  - USB Camera access
  - Emulating Camera using image files
  - Cameras over network

* Visionmaker
  - Our demo system: Wifi connected, Ultimaker based Axis and Illumination system

* Algorithms
  - Otsu's Thresholding algorithm
  - ...



## Fast download and install

To install editably in current dir's subfolder `src/ibvlib`:

```bash
  pip install -e git+https://github.com/mechaot/ibvlib.git#egg=ibvlib
```



## Installing to Python environment (recommended way)

Note: Linux/Mac users might need to replace *all* 

* `python` &rarr;  `python3`
* `pip` &rarr; `pip3`

1. Download + extract / clone *ibvlib*

2. Open Terminal in *ibvlib*. `cd` to the project directory.
    * Windows: use "cmd.exe"
    * Linux: use "bash" / "Terminal"
  

3. Install dependencies

  ```bash
    pip install -r requirements.txt
  ```

4. Install as *editable* library
  
  ```bash
    pip install -e .
  ``` 


Note: See: https://packaging.python.org/tutorials/installing-packages/



## Student's Note

This repository is under development an will update during lessons. You can download the zip-file every few weeks, but learning about git and cloning the repository is strongly recommended.

