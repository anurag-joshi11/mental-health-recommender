# Mental Health Recommender System

A conversational AI system for mental health assessment and personalized recommendations using GAD-7, PHQ-9, and sentiment analysis.

---

## Features

- **Survey-based assessment** (GAD-7 & PHQ-9) for anxiety and depression severity.
- **Conversational AI** for users who opt out of the survey, with sentiment analysis and clustering.
- **Personalized recommendations**: self-help, professional, or emergency resources.

---

## System Overview

![System Architecture](images/architecture.png)
*System architecture and workflow*

---

## How It Works

1. **User interacts** with the chatbot (Dialogflow).
2. **Survey path**: If user agrees, GAD-7 and PHQ-9 are administered, responses classified using ML models (SVM, etc.), and recommendations are generated.
3. **Conversational path**: If user declines, chatbot uses sentiment analysis and clustering to provide relevant support.

![Workflow](images/workflow.png)
*Survey and conversational flow*

---

## Dialogflow Intents

![Dialogflow Intents](images/dialogflow_intents.png)

---

## Model & Recommendation Flow

![Model Flow](images/model_flow.png)

---

## Results

- **Classification accuracy**: SVM performed best for both GAD-7 and PHQ-9.
- **Distribution of results**:

![Results Distribution](images/results_distribution.png)

---

## Example Scenario

![Chatbot Example](images/scenario_minimal.png)
*User with minimal anxiety & depression*

---

## Quick Start

```bash
git clone https://github.com/yourusername/mental-health-recommender.git
cd mental-health-recommender
pip install -r requirements.txt
python app.py
