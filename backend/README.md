# Amazon Nova Pro Integration

This repository demonstrates how to integrate Amazon's Nova Pro model into your application using Amazon Bedrock.

## Prerequisites

1. An AWS account with access to Amazon Bedrock
2. Appropriate IAM permissions to invoke Bedrock models
3. Python 3.7+ installed

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure AWS credentials:
   ```
   aws configure
   ```

3. Make sure you have requested and been granted access to the Nova Pro model in the Amazon Bedrock console.

## Usage

Run the example script:
```
python nova_pro_example.py
```

## Integration Steps

To integrate Nova Pro into your own application:

1. Import the necessary AWS SDK (boto3)
2. Set up the Bedrock client
3. Format your request with the appropriate parameters
4. Call the model and process the response

See `nova_pro_example.py` for a complete example.

## Important Notes

- Amazon Nova Pro is accessed through Amazon Bedrock using the Claude 3 Sonnet model ID
- You need to request model access in the AWS console before using it
- Pricing is based on input and output tokens
- Be sure to handle API errors and implement appropriate retry logic in production applications