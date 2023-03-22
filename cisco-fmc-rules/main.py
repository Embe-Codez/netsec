import requests
import config
import base64
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Retrieve the FMC URL, username, and password from the config module
print("Authenticating with Cisco FMC API...")
fmc_url             = config.url
fmc_username        = config.username
fmc_password        = config.password
domain_id           = config.domain_id

# Encode the username and password using Base64 encoding
auth_string         = f"{fmc_username}:{fmc_password}"
encoded_auth_string = base64.b64encode(auth_string.encode()).decode()

# Authenticate with the FMC API and retrieve an access token
auth_url            = f"{fmc_url}/api/fmc_platform/v1/auth/generatetoken"
auth_headers        = {"Authorization": f"Basic {encoded_auth_string}"}
auth_response       = requests.post(auth_url, headers=auth_headers, verify=False)
access_token        = auth_response.headers.get("X-auth-access-token", default=None)
if not access_token:
    raise ValueError("Failed to authenticate with FMC API: {}".format(auth_response.text))

# Retrieve the policy ID and other configuration options from environment variables
print("Please enter the following object UUIDs: ")
policy_id           = input("Enter the access control policy ID: ")
intrusion_policy_id = input("Enter the intrusion policy ID: ")
file_policy_id      = input("Enter the file policy ID: ")
variable_set_id     = input("Enter the variable set ID: ")

# Define the base URL for the access control policy (without the /accessrules endpoint)
access_control_policy_base_url = f'{fmc_url}/api/fmc_config/v1/domain/{domain_id}/policy/accesspolicies/{policy_id}'

# Define the API endpoint for the access control policy rules
access_control_policy_url = f'{access_control_policy_base_url}/accessrules'

# Make a GET request to retrieve the current rules for the access control policy
print("Gathering all rules within access control policy...")
get_response = requests.get(access_control_policy_url, headers={'X-auth-access-token': access_token}, verify=False)
get_response.raise_for_status()

# Parse the JSON response and retrieve the access control policy name
access_control_policy = get_response.json()

# Print statement to notify user of updating rules within access control policy.
print("Updating rules within access control policy...")

# Define the maximum number of attempts to update a rule
max_attempts = 3

#######################3################################### UPDATING RULES IN LOOP ###############################################################################
for rule in access_control_policy['items']:
    # Define the API endpoint for the specific rule
    object_UUID = rule['id']
    access_control_policy_rule_url = f'{access_control_policy_url}/{object_UUID}'

    # Define a dictionary to store the updated rule attributes
    updated_rule = {
        'name': rule['name'],
        'action': 'ALLOW',
        'enabled': 'true',
        'ipsPolicy': {
            'type': 'IntrusionPolicy',
            'id': intrusion_policy_id,
            'name': ""
        },
        'filePolicy': {
            'type': 'FilePolicy',
            'id': file_policy_id,
            'name': ""
        },
        'variableSet': {
            'type': 'variableSet',
            'id': variable_set_id,
            'name': ""
        },
        'logBegin': True,
        'logEnd': True,
        'sendEventsToFMC': True,
        'enableSyslog': True,
        # Include the id of the rule in the request body
        'id': object_UUID
}
#######################3################################### UPDATING RULES IN LOOP ###############################################################################

    # Remove null objects from the updated rule
    updated_rule = {k: v for k, v in updated_rule.items() if v is not None}

    # Defines PUT request URL
    rule_url     = access_control_policy_rule_url

    # Update the rule attributes
    put_response = requests.put(rule_url, headers={'X-auth-access-token': access_token, 'Content-Type': 'application/json'}, json=updated_rule, verify=False)

    # Attempt to update the rule, with retries if the request fails
    attempts = 0
    while attempts < max_attempts:
        try:
            put_response = requests.put(rule_url, headers={'X-auth-access-token': access_token, 'Content-Type': 'application/json'}, json=updated_rule, verify=False)
            put_response.raise_for_status()
            print(f"Updated rule {rule_url} successfully.")
            break
        except requests.exceptions.RequestException as e:
            print(f"Failed to update rule {rule_url}.")
            print(f"Exception: {e}")
            attempts += 1
            if attempts >= max_attempts:
                print(f"Maximum number of attempts reached for rule {rule_url}.")
                break

   # Check if the PUT request was successful
    if put_response.status_code == 200:
        print(f"Updated rule {rule_url} successfully.")
    else:
        print(f"Failed to update rule {rule_url}.")
        print(f"Response code: {put_response.status_code}")
        print(f"Response content: {put_response.content}")

   # Reset the updated_rule dictionary for the next iteration
    updated_rule = {}

    # Code to be executed only when the script is run as the main file
    if __name__ == '__main__':
        print("Running Cisco FMC API updater script...")