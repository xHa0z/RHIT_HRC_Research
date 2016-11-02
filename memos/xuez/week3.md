## Week 3 Memo
From: Zhihao Xue
Date: Sept.22 - Sept.29
To: Dr. Berry

----

This week the main work is about how to covert voice to text. 

There are several commercial software and non-commercial software libraries on the market. Based on Dr. Shibberu's recommendation, our priority option is Google Cloud Speech API. Besides this, I also have trail on IBM Watson. 

Both Google and IBM has an online demo of their API. You can try [Google's](https://cloud.google.com/speech/) here and [Watson](https://speech-to-text-demo.mybluemix.net) here. 

After comparison, Google is more reliable and more accurate than Watson. Both of them return a JSON object with some alternatives and confidence level. Google is free for the first 60 minutes every month, after that, the price is $0.006 per 15 seconds, while Watson is free for the first 1000 minutes and $0.02 per minute after that. 

Another important factor that I choose Google is that from Google's documentation, Google is the only one supports live streaming. Both Google and Watson you can have real-time result on web page. But using their library may not give us a streaming result. 

I used Google Cloud Console register a new app with Speech API and tried different programming languages tried to find the best one to fit our project. The ideal solution is to use JavaScript, since the return value is JSON. But from Google's doc, JavaScript may not support streaming. 

Other than Google Speech API, I also started looking at Stanford NLP toolkit. And Stanford has an online course, [CS224d](http://cs224d.stanford.edu/) about neural network and natural language processing. I watched some videos about this topic. 


