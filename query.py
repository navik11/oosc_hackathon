import google.generativeai as genai

genai.configure(api_key="AIzaSyA9hLGJD5RjmB8OrAmwdL5zpSEzUiG3w1Y")

model = genai.GenerativeModel('gemini-1.5-flash')

query = "generate 10 questions from the following content: 'Welcome to the OpenAI Developer community! Looking for ChatGPT support? Head tohttps://help.openai.com! This community resource is for all users of the various OpenAI developer platforms. We welcome discussion of the API, our models, ChatGPT Plugins, and other closely related topics. We also welcome your site feedback. The OpenAI API Community Forum is a place where you can learn, share, and collaborate. It\u2019s a great way to see what others are working on, trade tips, hear about the latest product updates, and share feedback. Categories As of writing, the following forum categories exist: When creating a new topic (by clicking \u201cNew Topic\u201d on theforum homepage), please select the most relevant category. This will keep the forum organized, and make it easier for other users to find your topic. 882\u00d7442 43.5 KB You can also search topics by category on the homepage. Policies Please see our broader guidelines on theOpenAI website. Other resources Learn more about the OpenAI API, or get start'"
q2 = "generate 10 question from 'https://openai.com' and some relevant links in json formate"

response = model.generate_content(q2)
print(response.text)