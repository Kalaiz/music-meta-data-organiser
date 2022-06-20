# Music meta-data organiser
![Status](https://img.shields.io/badge/status-viewable-green)

A command line tool which cleans and organises the metadata of music files. 


## Table of Content:
  - [Table of Content:](#table-of-content)
    - [📜 Description:](#-description)
    - [🛠️ Tools Used:](#️-tools-used)
    - [🔖 References:](#-references)
    - [⚙️ Installation:](#️-installation)

### 📜 Description:
A simple command line tool which can standardise formats of music files, add meta data such as title, cover art and artist names to the music files, without any input.


<p align="center">
<img src="resources/cmd-help.gif" width="95%" height="95%" /> 
</br>
<sub>Command line tool help documentation.</sub>
</p>

<p align="center">
<video src="https://user-images.githubusercontent.com/44941115/174575397-4e625674-dbb6-4bfc-a8df-86526ef0e999.mp4" controls="controls" />
</p>
<p align="center">
<sub>Command line tool in action.</sub>
</p>

[**User Story Map**](/resources/usm.svg)

### 🛠️ Tools Used:
- [mutagen](https://mutagen.readthedocs.io/en/latest/)
- [progress](https://pypi.org/project/progress/)
- [pydub](https://pydub.com/)
- [shazamio](https://github.com/dotX12/ShazamIO#readme)
- [pytest](https://docs.pytest.org/en/7.1.x/)
- [docopt](http://docopt.org/)
- Python


### 🔖 References:
- [Characters to avoid when naming file names, across all platforms.](https://www.mtu.edu/umc/services/websites/writing/characters-avoid/)
- [Maximum file name size](https://mossgreen.github.io/filenames-that-cross-platforms/)

### ⚙️ Installation:
1) Having this repository's content as the root folder, install relevant python packages by running:
   
   ```pip3 install -r requirements.txt```

2) To find out on how to use this command line tool, run: 
   
    ```python3  music_meta_data_organiser.py -h```


