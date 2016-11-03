## Week 2 Memo
From: Zhihao Xue
Date: Sept.14 - Sept.21
To: Dr. Berry

----

On last Wednesday, we had a team meeting to shared our idea about this research and assigned tasks to each members. We also talked about our game design. An updated [system diagram](https://www.draw.io/?state=%7B%22ids%22:%5B%220B6HVlD4v4sFQSl9JMy1wckdfOHM%22%5D,%22action%22:%22open%22,%22userId%22:%22103520717676869315452%22%7D#G0B6HVlD4v4sFQSl9JMy1wckdfOHM) has been uploaded to our Google Drive. This new diagram is made by draw.io, powered by Google. Using draw.io, each student in this group has authentication to modified the system diagram. 

In that meeting, I switched my task with Bryan. So, from now on, I will work with natural language processing part, while Bryan will be involved with Leap Motion. 

After switch role, I talked with Dr. Shibberu about how to build neural network, what we should consider to design the game and which API we should use to convert voice to text. Dr. Shibberu gave me some advice on game design. 

First, since we need to train our neural network eventually, our input data should be well-labeled, then we can use these data to train our neural network with supervised learning. In addition, this game may need to by played remotely, everyone over the campus could involve this game. But this is not our priority purpose for our MVP this quarter. With interactive with robot arm, this game must be implemented with physical control in real world, otherwise, there is no need to use robot arm. Also, to achieve MVP goal, the game should be start as simple as possible. As this game will be played by Rose students during the class breaks, this game should be designed as easy to follow and could be done within a considerable time duration. 

Dr. Shibberu also suggested that game data, including user input and game result can be stored on Rose server, such as Gauss, which is a high performance server for scientific computing. In our case, this server will improve speed of training neural network. After talking with Darryl, Gauss equipped with two Nividia Tesla K80, and there are about 3 TB free space. We can directly send our data on the Gauss without any compression. Darryl also helped us create a group and a working directory on Gauss. 

For natural language processing, Dr. Shibberu recommended me to use [Googel Speech API](https://cloud.google.com/speech/docs/) This API supports multiple programming language, including Python and Java. But is not free, we have 60 minutes each month to send data to and get result from Google. After that, we need to pay. Stanford has a NLP toolkit, we may also use this toolkit in our research to extract different kinds of words in each commands. 

And we still didn't get access to Meyer's room yet. A Skype chat room has been create to help our team communicate with each other. 

Some updates are pushed to GitHub, and there are still some students did not send me their GitHub user name and email address. 

Another students meeting will be held this afternoon in Library, since we didn't have our room yet. 


