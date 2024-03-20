import os
import email
import uuid

# from google.cloud import dialogflowcx_v3beta1 as dialogflow
from google.cloud.dialogflowcx_v3.services.sessions import SessionsClient
from google.cloud.dialogflowcx_v3.types import session


# client = dialogflow.SessionsClient()


def process_email(body,end_user_email):
    print("Entering process_email: {}".format(body))
    project_id="quantum-engine-377722"
    location_id="global"
    agent_id="ccd182f4-1c8d-4578-966b-1765ba1cfafb"
    event="email_input"
    language_code="en-us"

    resp_text = detect_intent_with_event_input(project_id, location_id, agent_id, event, language_code, body, end_user_email)
    print("Response: {}".format(resp_text))
    return resp_text

    # Initialize request argument(s)
    # query_input = dialogflow.QueryInput()
    # query_input.text.text = body
    # query_input.language_code = "EN"

    # request = dialogflow.DetectIntentRequest(
    #     # session="projects/*/locations/*/agents/*/environments/*/sessions/*",
    #     session="projects/quantum-engine-377722/locations/global/agents/ccd182f4-1c8d-4578-966b-1765ba1cfafb/environments/Draft/sessions/4656b4-b62-236-1c2-67d618fc6",
    #     query_input=query_input,
    # )

    # Make the request
    # response = client.detect_intent(request=request)
    # print("Response: {}".format(response))


def detect_intent_with_event_input(
    project_id,
    location,
    agent_id,
    event,
    language_code,
    query_text,
    end_user_email,
):
    """Detects intent using EventInput"""
    client_options = None
    if location != "global":
        api_endpoint = f"{location}-dialogflow.googleapis.com:443"
        print(f"API Endpoint: {api_endpoint}\n")
        client_options = {"api_endpoint": api_endpoint}
    session_client = SessionsClient(client_options=client_options)
    session_id = str(uuid.uuid4())
    session_path = session_client.session_path(
        project=project_id,
        location=location,
        agent=agent_id,
        session=session_id,
    )

    # Construct detect intent request:
    event = session.EventInput(event=event)
    query_text_input = session.TextInput(text=query_text)
    query_input = session.QueryInput(event=event, language_code=language_code)
    text_input = session.QueryInput(text=query_text_input, language_code=language_code)

    request = session.DetectIntentRequest(
        session=session_path,
        query_input=query_input,
    )

    response = session_client.detect_intent(request=request)
    response_text = response.query_result.response_messages[0].text.text[0]
    print(f"Event Response: {response_text}")

    query_params = session.QueryParameters(
#        event_query_params=session.EventQueryParameters(event=event)
    )
    query_params.channel="email"
    query_params.parameters=({'end_user_email':end_user_email})
    print("Query params: {}".format(query_params))
    # Construct detect intent request:

    request = session.DetectIntentRequest(
        session=session_path,
        query_input=text_input,
        query_params=query_params,
    )

    response = session_client.detect_intent(request=request)
    query_response = response.query_result
    print("Raw response: {}",format(query_response))
    response_text = query_response.response_messages[0].text.text[0]
    print(f"Query Response: {response_text}")

    return response_text


if __name__ == '__main__':
#  app.run(debug=True)
  process_email("where is the nearest distribution center to PA, and what are their hours for dry goods?","david.mcdaniel@66degrees.com")
