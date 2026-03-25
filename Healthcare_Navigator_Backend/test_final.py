import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from agent.prescription_agent import prescription_agent
import json

# Mocking some parts for a quick check if needed, 
# but let's try to run it on an existing test image if possible.
test_image = "test_images/prescription1.jpg"

if os.path.exists(test_image):
    print(f"Testing prescription_agent with {test_image}...")
    try:
        result = prescription_agent(test_image)
        print("\nFinal API Response:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
else:
    print(f"Test image {test_image} not found. Skipping full test.")
