# phi3-airnav-copilot
# AirNav AI Assistant: Intelligent Line Maintenance Co-Pilot

An enterprise-grade AI tool designed for aviation maintenance environments (MRO). This project leverages **Microsoft Phi-3-mini** deployed on **Microsoft AI Foundry** to interface with **Airbus AirNav/airnavX** technical data, enabling flight-line engineers to query complex Aircraft Maintenance Manuals (AMM) using natural language.

## Key Features
- **Aviation-Specific Reasoning**: Fine-tuned prompt engineering tailored for KLM Line Maintenance standards.
- **Enterprise Security**: Zero-hardcoded keys, fully relying on secure environment configurations.
- **Cost-Optimized SLM**: Utilizes `Phi-3-mini` via Serverless APIs, providing rapid responses with minimal cloud compute costs.

## Tech Stack
- Python 3.10+
- Microsoft Azure AI Inference SDK
- Microsoft AI Foundry
- Python-dotenv

## How to Run
1. Clone the repository: `git clone https://github.com`
2. Install dependencies: `pip install azure-ai-inference python-dotenv`
3. Create a `.env` file based on the provided template and add your Azure AI Foundry credentials.
4. Run the assistant: `python airnav_assistant.py`
