from agent.prescription_agent import prescription_agent
import json

try:
    print("Testing Prescription Agent...")

    result = prescription_agent("test_images/prescription1.jpg")

    print("\nAnalysis Result:")
    print(json.dumps(result, indent=2))

except Exception as e:
    print(f"An error occurred during testing: {e}")