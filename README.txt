Mental Health Recommender System

Architecture:

Chatbot: Used DialogFlow messanger to run chatbot
Flask Back-end - Connected Dialogflow via webhook to flask
Server: ngrok used to expose local flask server and connect to dialogflow via https reques

Pre-requisites and installation:
1. Access to dialogflow has been provided to the email ids: aissaoui2022@gmail.com, aissaoui@uottawa.ca, arahgoza@uottawa.ca
2. DialogFlow console link: https://dialogflow.cloud.google.com/#/agent/mentalhealthassistantchat-kegh/intents
3. Run the Flask-API.py file for back-end
4. Download ngrok and configure the API key from the ngrok website.
5. Open the folder containing ngrok.exe file and open this path in cmd
6. Run command: ngrok.exe http 5000
7. Above command will generate an https url (eg. https://61cf-2607-fea8-bda2-800-9508-147d-8e44-e39.ngrok-free.app)
8. Go to the Dialogflow console -> Fulfillment -> Paste this url along with /webhook as it is the API exposed via Flask back-end (eg. https://61cf-2607-fea8-bda2-800-9508-147d-8e44-e39.ngrok-free.app/webhook)
9. Now, to use the chatbot use DialogFlow Messenger since we have survey data that display multiple options and process user input. To view the intents, logs have been printed in the Flask Back-end.


DialogFlow Response: {'responseId': '98c1c317-230c-488a-91cb-3943f24b3939-7c6de2ad', 'queryResult': {'queryText': 'Nearly every day', 'action': 'PHQ_Question-1.PHQ_Question-1-custom.PHQ_Question-2-custom.PHQ_Question-3-custom', 'parameters': {'duration': ''}, 'allRequiredParamsPresent': True, 'fulfillmentMessages': [{'text': {'text': ['']}}, {'payload': {'richContent': [[{'type': 'description', 'text': ['Select one of the following options:'], 'title': 'How often are you Feeling tired or having little energy?'}, {'options': [{'text': 'Not at all'}, {'text': 'Several days'}, {'text': 'More than half the days'}, {'text': 'Nearly every day'}], 'type': 'chips'}]]}}], 'outputContexts': [{'name': 'projects/mentalhealthassistantchat-kegh/agent/sessions/dfMessenger-5063695/contexts/phq_question-4-followup', 'lifespanCount': 2, 'parameters': {'duration': '', 'duration.original': ''}}, {'name': 'projects/mentalhealthassistantchat-kegh/agent/sessions/dfMessenger-5063695/contexts/phq_question-3-followup', 'lifespanCount': 1, 'parameters': {'duration': '', 'duration.original': ''}}, {'name': 'projects/mentalhealthassistantchat-kegh/agent/sessions/dfMessenger-5063695/contexts/phq_question-2-followup', 'parameters': {'duration': '', 'duration.original': ''}}, {'name': 'projects/mentalhealthassistantchat-kegh/agent/sessions/dfMessenger-5063695/contexts/__system_counters__', 'parameters': {'no-input': 0.0, 'no-match': 0.0, 'duration': '', 'duration.original': ''}}], 'intent': {'name': 'projects/mentalhealthassistantchat-kegh/agent/intents/84bf7ff9-3ef8-4206-8bbe-6fa055cb0ccd', 'displayName': 'PHQ_Question-4'}, 'intentDetectionConfidence': 1.0, 'languageCode': 'en'}, 'originalDetectIntentRequest': {'payload': {}}, 'session': 'projects/mentalhealthassistantchat-kegh/agent/sessions/dfMessenger-5063695', 'alternativeQueryResults': [{'queryText': 'Nearly every day', 'allRequiredParamsPresent': True, 'fulfillmentText': "Hi, thank you for sharing your feelings with me. I can understand how challenging it must be to carry that weight of emptiness. Depression often brings with it a deep sense of pain and stress. Can you tell me more about what you're experiencing?", 'fulfillmentMessages': [{'text': {'text': ["Hi, thank you for sharing your feelings with me. I can understand how challenging it must be to carry that weight of emptiness. Depression often brings with it a deep sense of pain and stress. Can you tell me more about what you're experiencing?"]}}], 'outputContexts': [{'name': 'projects/mentalhealthassistantchat-kegh/agent/sessions/dfMessenger-5063695/contexts/phq_question-3-followup', 'lifespanCount': 1, 'parameters': {'duration': '', 'duration.original': ''}}, {'name': 'projects/mentalhealthassistantchat-kegh/agent/sessions/dfMessenger-5063695/context'HIGH', 'matchConfidence': 0.79519325}, {'source': 'projects/mentalhealthassistantchat-kegh/knowledgeBases/MzU3ODA3OTk0MjI1NDAwMjE3Nw/documents/MjAwOTgzMDYzMzM1Nzk2NzM2MQ', 'faqQuestion': "I've been feeling so stressed out lately, Buddy. It's like every aspect of my life is weighing down on me. I can't seem to catch a break.", 'answer': "I'm sorry to hear that,. It sounds like you're really overwhelmed. Can you tell me more about what's been going on?", 'matchConfidenceLevel': 'LOW', 'matchConfidence': 0.3965751}, {'source': 'projects/mentalhealthassistantchat-kegh/knowledgeBases/MzU3ODA3OTk0MjI1NDAwMjE3Nw/documents/MjAwOTgzMDYzMzM1Nzk2NzM2MQ', 'faqQuestion': "I feel so lost. I don't know what to do anymore. Her words haunt me every day, and it's unbearable.", 'answer': "It sounds like you're carrying a heavy burden. Can you tell me more about what's been going on at work?", 'matchConfidenceLevel': 'LOW', 'matchConfidence': 0.3301698}]}}]}    

Intent: PHQ_Question-4
User Response: Nearly every day
Stored in PHQ: 3
Next question stored for session projects/mentalhealthassistantchat-kegh/agent/sessions/dfMessenger-5063695: PHQ_Question-4
127.0.0.1 - - [03/Apr/2025 14:10:25] "POST /webhook HTTP/1.1" 200 -

