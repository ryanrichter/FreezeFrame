FreezeFrame is a proof-of-concept platform that detects objects within video frames and maps them to relevant product links in real time.

Built during an AWS hackathon, this project explores the intersection of computer vision, real-time media processing, and e-commerce integration—enabling a “pause and shop” experience for video content.

🚀 Overview

FreezeFrame allows users to:

Capture a frame from video content
Detect objects within that frame
Map detected objects to purchasable products
Surface relevant links instantly

The goal is to bridge the gap between content consumption and commerce, turning passive viewing into an interactive experience.

🧠 How It Works
Frame Capture
A frame is extracted from a video stream or static input
Object Detection
Computer vision models identify objects within the frame
Data Mapping
Detected objects are mapped to product data sources (e.g., Amazon listings)
Result Delivery
Users receive contextual product recommendations tied to the visual content
🏗️ Architecture
Frontend: Interface for capturing frames and displaying results
Backend Services: API layer for processing and orchestration
Cloud Infrastructure:
AWS Lambda for serverless compute
Event-driven processing for scalability
Data Integration:
Product lookup and mapping logic
External APIs for product data
🛠️ Tech Stack
Languages: C#, Python (for CV/processing)
Frameworks: .NET
Cloud: AWS (Lambda)
Concepts:
Event-driven architecture
Serverless computing
Computer vision integration
API design
🧪 Hackathon Context
🏆 AWS Hackathon Co-Winner
Built within a constrained timeframe as a rapid prototype
Focused on demonstrating:
Technical feasibility
Real-time performance
Product-market potential

The core concept was later explored in a production context on Amazon Prime Video.

📦 Getting Started

Note: This is a hackathon prototype and may require additional setup or configuration.

Prerequisites
.NET SDK
AWS account (for Lambda deployment)
API keys for any external services (if applicable)
Setup
# Clone the repository
git clone https://github.com/ryanrichter/FreezeFrame.git

# Navigate into the project
cd FreezeFrame

# Restore dependencies
dotnet restore

# Run the application
dotnet run
📈 Future Improvements
Improve object detection accuracy with more advanced models
Enhance product matching relevance
Add real-time video stream processing (vs static frames)
Expand integrations beyond a single product source
Optimize latency for production-scale usage

📄 License

This project is for demonstration purposes and was developed as part of a hackathon.

💡 Inspiration

FreezeFrame was inspired by the idea that every moment in video content could be interactive and shoppable, unlocking new possibilities for media, advertising, and user engagement.
