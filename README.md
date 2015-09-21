# SamFileConverter
This is a project for a friend who works in video editing.
The problem was:
We are given a file (in .edl format) with some number of lines, each of which has an identifier at the start, then irrelevant info followed by 4 times, followed by more irrelevant info. We need to find the lines which start with a given identifier, and output a filecontaining the midpoint time of the last 2 times from each of those lines.

The time format is HH:MM:SS:FF where FF indicates frames, from 00 to 23.
For example, the input line 

002  HAW_BLAC V     C        00:00:00:00 00:00:01:00 00:07:00:03 00:07:01:03 * FROM CLIP NAME:  HAW_BLACK_HD.nxclip 

would result in a computed time of 00:07:00:15

Functionality:
The converter can be given a single file, and an output file name, or it can operate in batch mode where it finds all .edl files in a given folder and creates a folder inside that folder with all the converted files. These files will have the same names as the .edl files, but with a .txt extension.

In the current version, the old command line interface has been upgraded to a GUI.
