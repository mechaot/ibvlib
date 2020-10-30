# IBV Library
Common functions used in the Lecture "Image Processing I: Industrial Imaging" at Leibniz Universität Hannover, Germany

- [IBV Library](#ibv-library)
  - [Library Structure](#library-structure)
  - [Windows/Linux/Mac](#windowslinuxmac)
    - [Installing and learning Git is **highly** encouraged](#installing-and-learning-git-is-highly-encouraged)
    - [Linux/Mac users will most probably need to replace below *all*:](#linuxmac-users-will-most-probably-need-to-replace-below-all)
  - [Download and install using git](#download-and-install-using-git)
    - [Update to new release](#update-to-new-release)
  - [Installing wihout git](#installing-wihout-git)
    - [Update to new release](#update-to-new-release-1)
  - [Student's Note](#students-note)

## Library Structure

* Camera
  - USB Camera access
  - Emulating Camera using image files
  - Cameras over network

* Visionmaker
  - Our demo system: Wifi connected, Ultimaker based Axis and Illumination system

* Algorithms
  - Otsu's Thresholding algorithm
  - ...

## Windows/Linux/Mac


### Installing and learning Git is **highly** encouraged

* Windows: Install git 4 windows (www.gitforwindows.org)
  - Tipp: Select *install to PATH* and use *OpenSSH* and *Windows Credential Storage* (or similar; no Putty!)
* Linux (Ubuntu): ```sudo apt install git```
* Linux (Fedora): ```sudo yum install git```
* Mac: I have no idea/test device: www.google.com/search?q=install+git+on+mac


### Linux/Mac users will most probably need to replace below *all*:

* `python` &rarr;  `python3`
* `pip` &rarr; `pip3`

## Download and install using git

To install editably with everything taken care of, in current dir's subfolder `src/ibvlib`:

```bash
  pip install -e git+https://github.com/mechaot/ibvlib.git#egg=ibvlib
```

Note: use `--src=<dirname>` in the above command to manually specify the install folder, e.g.

### Update to new release
```bash
  cd `ibvlib`  # you know what I mean by that
  git pull
```

Note: If you have edits preventing said `pull` then try this *dirty solution*:

```bash
  git stash      # store away your changes
  git pull       # fetch from github
  git stash pop  # (optional) re-apply your changes
```
...or learn more about using `git` properly:

## Installing wihout git

1. Download from https://github.com/mechaot/ibvlib/archive/master.zip as zip-Archive
2. save && extract to your development `<workspace>/ibvlib`

3. Open Terminal in `ibvlib` (`cd` to the project directory).
    * Windows: use "cmd.exe"
    * Linux: use "bash" / "Terminal"
  

4. Install dependencies

  ```bash
    pip install -r requirements.txt
  ```

4. Install as *editable* library
  
  ```bash
    pip install -e .
  ``` 


Note: See: https://packaging.python.org/tutorials/installing-packages/

### Update to new release

1. Uninstall package

In cmd/bash type

```bash
  pip uninstall ibvlib
```

2. Confirm.

3. Start over by downloading and extracting

## Student's Note

This repository is under development an will update during lessons. You can download the zip-file every few weeks, but learning about git and cloning the repository is strongly recommended.

