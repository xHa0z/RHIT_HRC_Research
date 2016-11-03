## Week 6 Memo
From: Zhihao Xue
Date: Oct.13 - Oct.19 
To: Dr. Berry

----

First, I want to talk about Stanford NLP toolkit. After trails and errors, I realize that there might be a solution to my current issues, but try another way may save a lot of time than keeping finding a solution. 

The current solution is to download the entire Stanford NLP toolkit to local machine and then install it on local. Then, in the project settings, include the library path, and I can use this library. The disadvantage of this method is when you want to share your program, you have to tell them how to download, install and include this library. And this library is about 700MB, which means it is hard to upload or package and send to others directly. (The main program is only few hundred KBs, it is not very efficient)

Since we are in MVP, the priority goal is to make the project run successfully, I will arbitrary choose this way (include library path) to use Stanford's toolkit. 

To exam the toolkit installed correctly, I ran the demo code from Dr. Fisher, and no errors popped up. 

After test Stanford toolkit, I tried to combine Google's speech to text part and NLP part together. As these two parts are written in two different languages, the current solution I came up with is to create a shared file, and make these two parts both have the right to read and write this file. 

So, now the procedure is like a pipeline. First, the speech to text program fired up, and dictation user's voice input. Then send this voice to Google and waiting for the return value. When it has the result, the program will extract the transcript from the result and save it into a text file in a specific folder base on created time. At this time, Google's job is done, NLP parts starts. Java program would locate this particular directory and store all text files into a list. Java would sort these file first and loop this list, read content in each file and process it. 

So far, the most of this procedure worked fine. There are two issues needed to be fixed. The first one is this pipeline is not fully automatic, I still need to switch to Eclipse to click 'Run' button to run Java NLP program. The other one is when the Java ran the last text file, there is a IndexOutOfBoundary exception error occurred. 
I am still working on how to fix this bug. 

Few weeks ago, I mentioned to upload our data to Gauss server. Recently, Darryl replied me what I can do. Basically, it is hard to upload files to Gauss without user name and password authentication. So, a more general way to do this is after certain amount of time, for example one day, we can manually upload our raw data to Gauss. 

I also tried to port our current project to a Raspberry Pi device. However, Pi is based on ARM architecture, some of software may not have a good compatibility. Some errors show up during the installation. So a spare laptop should be a better option.

