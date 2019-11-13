from behave import given, when, then
from django.test import Client
import json

client = Client()

USER_ENDPOINT = "/users/"

def retrieve_json_response_content_and_id(response):
    """
    JSON loads response.content.
    
    :param response: response to retrieve content from
    
    :returns (dict): response content
    """
    try:
        response_content = json.loads(response.content)

    except json.decoder.JSONDecodeError:
        assert False, \
            "Response is not JSON serializable (most likely not a valid request}"

    user_url = response_content["url"]
    user_id = user_url[user_url.rfind("users/") + 6: user_url.rfind("/")]

    return user_id, response_content


@given(u'the following user data')
def step_impl(context):
    user_data_payload = {}
    for row in context.table:
        for heading in row.headings:
            if heading == "groups":
                groups_value = row.get(heading).strip()
                if groups_value:
                    user_data_payload[heading] = [groups_value]
                else:
                    user_data_payload[heading] = []
            else:
                user_data_payload[heading] = row.get(heading)

    context.user_payload = user_data_payload


@when(u'a {request_method} request is made to the user endpoint')
def step_impl(context, request_method):
    if request_method == "POST":
        context.response = client.post(USER_ENDPOINT, 
                               context.user_payload, 
                               content_type="application/json")
    if request_method == "GET":
        context.response = client.get(f"{USER_ENDPOINT}{context.user_id}/")

    


@then(u'the user is created')
def step_impl(context):
    assert context.response.status_code == 201, "Failed to create user, " \
                                        f"status code: {context.response.status_code}"


@given(u'a user exists with the following user data')
def step_impl(context):
    user_data_payload = {}
    for row in context.table:
        for heading in row.headings:
            if heading == "username":
                context.username = row.get(heading)
            if heading == "groups":
                groups_value = row.get(heading).strip()
                if groups_value:
                    user_data_payload[heading] = [groups_value]
                else:
                    user_data_payload[heading] = []
            else:
                user_data_payload[heading] = row.get(heading)

    context.user_payload = user_data_payload

    context.response = client.post(USER_ENDPOINT, 
                           context.user_payload, 
                           content_type="application/json")

    context.user_id, response_content = retrieve_json_response_content_and_id(context.response)


@then(u'the user is retrieved')
def step_impl(context):
    assert context.response.status_code == 203, "Failed to retrieve user, " \
                                        f"status code: {context.response.status_code}"