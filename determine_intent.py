import vertexai
from vertexai.language_models import TextGenerationModel
from vertexai.generative_models import GenerativeModel, Part

print("Loading Vertex AI")
vertexai.init(project="quantum-engine-377722", location="us-central1")
parameters = {
    "max_output_tokens": 256,
    "temperature": 0.2,
    "top_p": 0.8,
    "top_k": 40
}
# print("Calling from_pretrained")
# model = TextGenerationModel.from_pretrained("gemini-1.0-pro")

print("Calling GenerativeModel")
model = GenerativeModel("gemini-pro")

def determine_intent(email_body):
    print("Calling predict intent on {}".format(email_body))
    chat = model.start_chat()
    # response = model.predict(
    response = chat.send_message(
        """Multi-choice problem: Define the category of the ticket?
    Categories:
    - Purchase Order (PO) Inquiry
    - Terms and Conditions (T&C) Inquiry
    - distribution center inquiry

    Ticket: I would like details about my PO 12345
    Category: PO

    Ticket: For my company (66degrees.com), what are my terms for ordering cream cheese core?
    Category: TC

    Ticket: What is the closest distribution center to PA?
    Category: DC

    Ticket: {}
    Category:
    """.format(email_body),
        # **parameters
    )
    print(f"Response from Model: {response.text}")
    return response.text


if __name__ == '__main__':
#  app.run(debug=True)
  determine_intent("Hello, I would like to know the receive date for PO 1002105")
  determine_intent("What are the terms for ordering cream cheese core?")
  determine_intent("What is the closest distribution center to PA?")
