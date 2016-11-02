## Week 4 and 5 Memo
From: Zhihao Xue
Date: Sept.29 - Oct.12 
To: Dr. Berry

----

This memo is for week 4 and week 5 from Sept.29 to Oct.12, because we have fall break and I did not show up on Oct.5 because of some family issue. So this memo is for two weeks. 

From last memo, I was working on Google Speech API and Stanford natural language process toolkit and run into lots of problems. 

As I mentioned in last memo, Google does support multiple programing languages, including JavaScript, Java and Python. At the very beginning, I was tried to use JavaScript as selected language, since I want to use returning JSON object directly. However, after installed the library and tested, I found that we need some other packages and libraries to support this particular library (too many dependencies and some installation errors) and JavaScript does not support streaming. 

Then, I tried Java. In order to use Google's API, you have to register your app on Google App Engine and Google Cloud Console, then Google will generate an unique credential for you to authenticate. You need to export this credential to your environment configuration path, then you have right to use all Google APIs. However, when I tried to do so in Java, if just failed. Other than this, Java's API does not support streaming as well. 

Finally is Python. There are two package for Python, one is the traditional REST APi, which is similar with JavaScript's API. The result is in a JSON object with transcript and confidence. But, still, this REST API does not support streaming. The other one is gRPC. This one does support streaming, but returning result is slightly different from JSON object. 

When I tested this API, I also found another issue about non-streaming. From [Google official documentation](https://cloud.google.com/speech/docs/best-practices), it says we should use FLAC or uncompressed audio, and sampling rate should be 16kHz or higher. We test various format of audio files, including wmv, wav, FLAC with higher sampling rate. And tried to convert format with Google recommended software. But we cannot get any result from Google. Each time, when we send out a audio file, Google can receive that, but when we tried to get something from Google, there is nothing. The retuning object is pure empty. There is no transcript or confidence. 

Fortunately, we still have gRPC protocol. With this API, we can easily send voice to Google and get result almost simultaneously. And we don't need to worry any format issue. With a microphone, this program can work well. As gRPC is different from REST API, the return object is also not in JSON format. The return object is using [Proto 3 protocol](https://developers.google.com/protocol-buffers/docs/proto3). In practice, I didn't have much trouble about this. I just followed the instruction to set up and everything works find. 

In Google's example, Google uses a key word 'exit' to indicate when to exit the program. When I tried this voice command on my MacBook Pro, the entire program is frozen and I have to force to quit. And when I switch to a Linux machine, the problem just disappeared. So I guess this is only about different operation systems and related softwares. 

Besides successfully run Google's API, I also have a trail on Stanford NLP toolkit. This toolkit is written in Java, from its [official website](http://stanfordnlp.github.io/CoreNLP/download.html) there is a Maven repository I can use to install all dependencies. I chose this way is because I used to use maven to install some other packages in Hadoop class. This should a easy and simple way to install packages for Java. But I had lots of trouble this time. 

First of all, there is a sample pom.xml file on Maven to help us install all dependencies this NLP toolkit needed. When I add this file to my project, it did automatic help me install all necessary libraries. And then I tried to run the sample program from Dr. Fisher, there are some compile errors. These errors indicated I did not install proper packages, so there are some methods in the demo code could not be found. 
I looked up references and found in this pom.xml file, it did not include the core nlp packages. In other words, this sample pom.xml file missed the most important part it should be included. Then i manually add these core packages into the pom.xml file. And the sample program could run. 
One problem solved, and the other one came. One reason to use Maven is I can generate a jar file through Maven, then I can use this jar file as a executable program run in command line. But the fact is not what I expected. There is a JNI error when I tried to build the jar file. And this error does not show up every time when I tried to build the jar. There occurs with a random probability. Furthermore, even I build the jar successfully, I sill cannot run the jar file in command line. There is always a 'Class not found' error each time I tried to run program.

I spent a lot of time on solving this Maven related problems. And I think I should switch to another way if I cannot make any progress by the end of this week. 

