import boto3
import json
import base64
import os
from datetime import datetime

# Create a Bedrock Runtime client in the AWS Region of your choice.
client = boto3.client("bedrock-runtime", region_name="us-east-1")

LITE_MODEL_ID = "amazon.nova-pro-v1:0"

def encode_image(image_path):
    """
    Read an image file and encode it as a base64 string.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
        
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def create_message_with_image(image_path):
    """
    Create a message with only an image.
    """
    content = []
    
    if image_path:
        try:
            image_data = encode_image(image_path)
            # Determine image format from file extension
            image_format = "jpeg" if image_path.lower().endswith(('.jpg', '.jpeg')) else "png"
            content.append({
                "image": {
                    "format": image_format,
                    "source": {
                        "bytes": image_data
                    }
                }
            })
        except Exception as e:
            print(f"Error processing image: {e}")
    
    return content

# Define your system prompt(s).
system_list = [
            {
                "text": """You are an AI assistant specializing in image analysis for e-commerce. Your task is to analyze the provided image and identify all items that are commercially available products (i.e., items that can be purchased online). For each identified product, provide the following details:
                1. **Product Name**: A clear, concise name or description of the item. Include a brand name (e.g., "Nike Air Max Sneakers" or "YETI Steel Coffee Mug").
                2. **Confidence Score**: A percentage (0-100%) indicating your confidence that the item is a purchasable product.
                3. **Brief Description**: A short description of the item's key features (e.g., color, material, or brand, if identifiable).
                4. **Potential Online Retailers**: Suggest 1-3 major online platforms where this product might be available (e.g., Amazon, eBay, Walmart, brand-specific websites).
                **Instructions:**
                - You must include a brand name in product_name. If no brand is visible or unknown, use a likely brand name based on the product type (e.g. "Apple AirPods" for unidentifiable earbuds, "Old Navy" for unidentifiable clothing). You MUST include a brand name, even if it may be incorrect.
                - Only include items that are clearly identifiable as products available for purchase. Exclude non-commercial items (e.g., a random rock, a person, or a generic background object).
                - If there are multiple similarly categorized items (e.g. several shoes or sweaters), provide mutliple entries for each item.
                - If the image contains multiple products, list each one separately.
                - If no products are identifiable, respond with: "No purchasable products detected in the image."
                - If certain details (e.g., brand or exact model) are unclear, make an educated guess based on visual cues and note any assumptions.
                - Format the response in a structured JSON-like format for easy integration into an app.
                **Example Response:**
                
                [
                {
                    "product_name": "Apple iPhone 14",
                    "confidence_score": 95,
                    "description": "A black smartphone with a dual-camera system, likely an iPhone 14 based on design.",
                    "potential_retailers": ["Amazon", "Apple Store", "Best Buy"]
                },
                {
                    "product_name": "YETI Ceramic Coffee Mug",
                    "confidence_score": 80,
                    "description": "A solid blue ceramic mug with a handle, standard size.",
                    "potential_retailers": ["Amazon", "Walmart", "Target"]
                }
                ]
                ```
                Analyze the image and provide the response in the specified format."""
            }
]

# Set your image path
image_path = "C:\\Users\\ryanric\\source\\repos\\foxcorp-hackathon-2025\\team-12\\Ryan\\tvshow.png"

# Define message with only the image
message_list = [{"role": "user", "content": create_message_with_image(image_path)}]

# Configure the inference parameters.
inf_params = {"maxTokens": 500, "topP": 0.9, "topK": 20, "temperature": 0.7}

request_body = {
    "schemaVersion": "messages-v1",
    "messages": message_list,
    "system": system_list,
    "inferenceConfig": inf_params,
}

start_time = datetime.now()

# Invoke the model with the response stream
response = client.invoke_model_with_response_stream(
    modelId=LITE_MODEL_ID, body=json.dumps(request_body)
)

request_id = response.get("ResponseMetadata").get("RequestId")
print(f"Request ID: {request_id}")
print("Awaiting first token...")

chunk_count = 0
time_to_first_token = None

# Process the response stream
stream = response.get("body")
if stream:
    for event in stream:
        chunk = event.get("chunk")
        if chunk:
            # Print the response chunk
            chunk_json = json.loads(chunk.get("bytes").decode())
            content_block_delta = chunk_json.get("contentBlockDelta")
            if content_block_delta:
                if time_to_first_token is None:
                    time_to_first_token = datetime.now() - start_time
                    print(f"Time to first token: {time_to_first_token}")

                chunk_count += 1
                print(content_block_delta.get("delta").get("text"), end="")
    print(f"\nTotal chunks: {chunk_count}")
else:
    print("No response stream received.")