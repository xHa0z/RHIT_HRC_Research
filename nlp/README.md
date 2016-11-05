# Speech To Text Conversion and Natural Language Processing 

This part is inspired by Google Cloud Speech gRPC APIs
For details about this API, please REFER to [Google Cloud Speech API](http://cloud.google.com/speech). 

What this part does is to use Google Cloud Speech API to analyze user's voice command, and base on this command to generate related output matrix. 

## Prerequisites

### Enable and configure Google Cloud Speech API

Please follow [this instruction](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/speech/grpc/README.rst) to enable and setup Google API.

#### Windows user
The above instruction is mainly for Mac and Linux users. 
For Windows users, the configuration is similar. Go to 'My Computer' -> right click 'properties' -> click 'Advanced system setting' on left sidebar -> click 'Environment Variables...' at the bottom -> create a new environment variable named 'GOOGLE_APPLICATION_CREDENTIALS' and set proper credential path.
Then you are ready to use Google API. 

### Numpy Package

In this program, we use numpy package to deal with some matrix operations and file IO handling. To install numpy package:
* Mac and Linux user:

  ```sh
  pip install numpy
  ```

* Windows user:

  ```sh
  python -m pip install numpy
  ```

## Usage and Procedure

This program needs one text file as input and generate a text as output and use this output file to communicate with Main program.

The input text file, named 'game.txt', record a 4 by 4 matrix. This file should be generated from the GUI, and tell this program where are these color blocks located and delimited with single space. A sample file is look like:
```sh
0 0 2 3
1 0 2 1
3 3 1 2
2 0 1 3
```

Where 0 means no block here, 1 means red block, 2 means green block and 3 means blue block.

When the program runs, it will first load this game board. If it detects a proper movement command from sample command list, such as 'pick up a green block', it will generate a 4 by 4 0 and 1 matrix, where 0 indicates there is no green block at this coordinate and 1 indicates there is a green block. Then, save this matrix to the output file 'out_file.txt'.

The program will exit and jump back to Main when user says 'finish'.

#### Error Handling

If something wrong with user's command, such as user gives multiple instructions in one session or gives no instruction, a 4 by 4 matrix with all -1 will be generated and save into 'out_file.txt' to tell Main there is something wrong in this part. User need to repeat this procedure again.



