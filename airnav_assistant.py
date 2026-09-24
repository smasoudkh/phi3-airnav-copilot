import os
import logging
from typing import Dict, Any
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage

# Configure logging for production-ready code
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AirNavAIAssistant:
    """
    An Intelligent Maintenance Assistant that interfaces with AirNav/airnavX 
    technical data to provide instant troubleshooting steps using Microsoft Phi-3.
    """
    def __init__(self):
        # Load environment variables safely (Best practice for GitHub)
        load_dotenv()
        self.endpoint = os.getenv("AZURE_FOUNDRY_ENDPOINT")
        self.api_key = os.getenv("AZURE_FOUNDRY_API_KEY")
        self.model_name = os.getenv("AZURE_DEPLOYMENT_NAME", "phi-3-mini")
        
        if not self.endpoint or not self.api_key:
            raise ValueError("Missing Azure AI Foundry credentials in environment variables.")
        
        # Initialize the official Microsoft Azure AI Inference Client
        self.client = ChatCompletionsClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.api_key)
        )
        logging.info("AirNav AI Assistant successfully initialized.")

    def get_troubleshooting_steps(self, airnav_fault_code: str, aircraft_type: str) -> str:
        """
        Queries Phi-3 to analyze the AirNav fault code and return AMM procedures.
        """
        # Simulated RAG Context from AirNav database export
        simulated_airnav_db = {
            "ECAM 29-11-00": "AMM Ref 29-11-00-A: Main Hydraulic Pump low pressure. Action: Check primary pump valves, bleed lines, inspect fluid level.",
            "ATA 21-31-00": "AMM Ref 21-31-00-B: Cabin Pressure Control System fault. Action: Verify Outflow Valve actuator, check static ports."
        }
        
        # Retrieve the technical data chunk matching the fault code
        manual_context = simulated_airnav_db.get(
            airnav_fault_code, 
            "General AMM fault isolation procedure applies. Inspect related ATA chapter systems."
        )

        # System prompt tailoring Phi-3 into a precise KLM Engineering Assistant
        system_prompt = (
            "You are an expert Aircraft Maintenance Systems Engineer at KLM Line Maintenance.\n"
            "Your task is to analyze AirNav/airnavX technical fault data and output clean, "
            "step-by-step troubleshooting instructions based ONLY on the provided Aircraft Maintenance Manual (AMM) reference.\n"
            "Keep the response technical, precise, and concise for flight-line technicians."
        )

        user_content = f"Aircraft: {aircraft_type}\nAirNav Fault Code: {airnav_fault_code}\nAMM Reference Context: {manual_context}"

        try:
            logging.info(f"Sending request to Phi-3 for fault code: {airnav_fault_code}")
            response = self.client.complete(
                messages=[
                    SystemMessage(content=system_prompt),
                    UserMessage(content=user_content)
                ],
                model=self.model_name,
                temperature=0.1, # Low temperature ensures strict technical accuracy
                max_tokens=500
            )
            return response.choices.message.content
            
        except Exception as e:
            logging.error(f"Failed to communicate with Azure AI Foundry: {e}")
            return "Error: Unable to process maintenance request at this time."

# Example execution block
if __name__ == "__main__":
    try:
        assistant = AirNavAIAssistant()
        
        # Simulating a real-world flight line scenario (Airbus A320 Hydraulic Fault)
        fault_code = "ECAM 29-11-00"
        ac_type = "Airbus A320"
        
        result = assistant.get_troubleshooting_steps(airnav_fault_code=fault_code, aircraft_type=ac_type)
        
        print("\n=== AIRNAV COGNITIVE ASSISTANT OUTPUT ===")
        print(result)
        print("=========================================\n")
        
    except Exception as error:
        print(f"Initialization Error: {error}")
