from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
from google.protobuf import json_format
import os
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VertexAIClient:
    def __init__(self, project_id: str, location: str = "us-central1"):
        """
        Initialize Vertex AI client
        Args:
            project_id: Google Cloud project ID
            location: Google Cloud region
        """
        try:
            aiplatform.init(project=project_id, location=location)
            self.project_id = project_id
            self.location = location
            logger.info(f"Initialized Vertex AI client for project {project_id} in {location}")
        except Exception as e:
            logger.error(f"Failed to initialize Vertex AI client: {e}")
            raise

    def get_text_prediction(
        self,
        prompt: str,
        model_name: str = "text-bison@001",
        temperature: float = 0.2,
        max_output_tokens: int = 1024,
        top_p: float = 0.8,
        top_k: int = 40,
    ) -> Dict[str, Any]:
        """
        Get prediction from a text model
        Args:
            prompt: Input text prompt
            model_name: Name of the model to use
            temperature: Temperature for sampling
            max_output_tokens: Maximum number of tokens to generate
            top_p: Top p sampling parameter
            top_k: Top k sampling parameter
        Returns:
            Dictionary containing the response
        """
        try:
            # Initialize the model
            model = aiplatform.Model.list(
                filter=f'display_name="{model_name}"',
                order_by="create_time desc",
                project=self.project_id,
                location=self.location,
            )[0]

            # Create the instance
            instance = predict.instance.TextPredictionInstance(
                content=prompt,
            ).to_dict()

            # Create the parameters
            parameters = predict.params.TextGenerationParams(
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                top_p=top_p,
                top_k=top_k,
            ).to_dict()

            # Get the prediction
            response = model.predict([instance], parameters=parameters)
            
            # Process the response
            predictions = response.predictions[0]
            
            return {
                "generated_text": predictions["content"],
                "safety_attributes": predictions.get("safety_attributes", {}),
                "citation_metadata": predictions.get("citation_metadata", {})
            }

        except Exception as e:
            logger.error(f"Error getting prediction from Vertex AI: {e}")
            raise

    def get_chat_response(
        self,
        messages: List[Dict[str, str]],
        model_name: str = "chat-bison@001",
        temperature: float = 0.2,
        max_output_tokens: int = 1024,
        top_p: float = 0.8,
        top_k: int = 40,
    ) -> Dict[str, Any]:
        """
        Get response from a chat model
        Args:
            messages: List of message dictionaries with 'author' and 'content'
            model_name: Name of the model to use
            temperature: Temperature for sampling
            max_output_tokens: Maximum number of tokens to generate
            top_p: Top p sampling parameter
            top_k: Top k sampling parameter
        Returns:
            Dictionary containing the response
        """
        try:
            # Initialize the model
            model = aiplatform.Model.list(
                filter=f'display_name="{model_name}"',
                order_by="create_time desc",
                project=self.project_id,
                location=self.location,
            )[0]

            # Create the instance
            instance = predict.instance.ChatPredictionInstance(
                context="You are a helpful AI assistant.",
                messages=messages,
            ).to_dict()

            # Create the parameters
            parameters = predict.params.ChatGenerationParams(
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                top_p=top_p,
                top_k=top_k,
            ).to_dict()

            # Get the prediction
            response = model.predict([instance], parameters=parameters)
            
            # Process the response
            predictions = response.predictions[0]
            
            return {
                "response": predictions["candidates"][0],
                "safety_attributes": predictions.get("safety_attributes", {}),
                "citation_metadata": predictions.get("citation_metadata", {})
            }

        except Exception as e:
            logger.error(f"Error getting chat response from Vertex AI: {e}")
            raise 