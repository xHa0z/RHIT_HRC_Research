## Week 7 Memo
From: Zhihao Xue
Date: Oct.20 - Oct.26
To: Dr. Berry

----

In this week, I made a big decision. In our project, we will not use Stanford natural language processing toolkit for this MVP. This decision is made by following considerations. 
First, from Jackson's game instruction, all input commands are fixed and have specific format. We don't need NLP toolkit to help us analyze what people say, what they want to express. With simple and limited inputs, Google Speech API and Python regular expression library can help us quickly detect the key words we interested in, such as pick, move and different color of blocks. 

Second, the NLP toolkit is written in Java, while most of our research project using Python. It is a little difficult to coordinate two different programming languages, as both of these two program try to implement similar functions. 

Third, run Java NLP program consumes lots of time. Since our game only lasts about 1.5 minutes, we should not waste much time on analysis, while Google is quick enough. 

I also began to integrate sub-system together. In the student meeting, we talk about how to communicate between each part. The main idea is still use a shared file to transmit data. 

A 1 and 0 matrix will be generated from NLP side, where 1 indicate this coordinate/location has the block with desired color and 0 shows no desired block there. Then this matrix will send back to the Main program, combine the result from Leap Motion side to generate our final decision matrix and send to Cyton robot. 

Our system diagram also be updated, GUI is separated from Leap Motion, and stands along as our main program. 
In our GUI, we need a button to turn on our speech to text program. Also, I will make sure the STT program will only receive and convert one command each time. 