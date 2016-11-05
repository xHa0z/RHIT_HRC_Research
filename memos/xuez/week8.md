## Week 8 Memo
From: Zhihao Xue
Date: Oct.27 - Nov.2
To: Dr. Berry

----

This week, we are going to integrate our project together. 

I made a schedule for this team, and assigned tasks and deadlines to each team member. We also had a minuted meeting on Monday at 5.15 pm. In this meeting, we confirmed this schedule and made sure what we need for each part and how to transmit data among different subsystem. 

On this meeting, we also agreed with we need a Windows machine to run our entire project. Under this scenario, I will need figure out how to run my natural language part on Windows. And this procedure is not quite difficult. Like in Linux, I just need to append python installation path to Windows default environment variables path, and create an new environment variable to export Google Cloud Authentication. After this configuration, I succeed running Python on my Windows machine. 

This week I also modified speech to text program. As we talked last week, I hard coded our game layout in my code, then, when the user says 'pick' and one of color key words 'red', 'blue' or 'green', the program will loop through the game matrix, and mark all desired coordinate where the colored box located with 1 and others are 0. 

Then we user says 'finish', the program will save this matrix into a 'out_file.txt' text file, and shares this data with main. 
If the user does not say anything useful, or the program did not capture the key words due the noise, the program will return a 4 by 4 matrix with all -1 to indicate the main there is a problem here and the user must try again.

So far, the programing part in our research project looks good. And we should finish this on time. 