import json
import os
import click
import csv
import datetime a


def read_bills_from_state(state):
    bill_names = os.listdir(state)
    bills = [os.path.join(state, bill_name) for bill_name in bill_names if bill_name.startswith('bill')]
    return bills

def get_action_data(bill_path, state, actions_data):
    with open(bill_path, 'r') as f:
        content = json.load(f)

    print(f'Retrieving data  for {bill_path} in {state}')

    if not content['actions']:
        return actions_data

    for action in content['actions']:
        action['organization_id'] = json.loads(action['organization_id'].replace('~', ''))['classification'] if action['organization_id'] is not None else ''
        action['bill_id'] = content['_id']
        action['state'] = state

        print(action)
        actions_data.append(action)
    return actions_data

def write_to_csv(actions_data):
    # Define the field names for the CSV
    fieldnames = ["description", "date", "organization_id", "classification", "bill_id", "state"]

    # Specify the filename for the CSV
    filename = "actions.csv"

    # Write data to CSV
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
    
        # Write header
        writer.writeheader()  

        # Write rows
        for row in actions_data:
            # print(row)
            writer.writerow(row)

        print(f"CSV file '{filename}' has been created successfully.")

# @click.command()
# @click.option('--state', prompt='Your name',
#               help='The person to greet.')
def main():

    for state in os.listdir('_data'):
        actions_data=[]
        print('Retrieving data  for %s' %state)
        state_path = os.path.join(os.getcwd(),'_data', state)
        bills = read_bills_from_state(state_path)
        for bill in bills:
            actions_data = get_action_data(bill, state, actions_data)  ###if I don't set it to a variabl, will it be changesd in polace?
        write_to_csv(sponsors_data)
    




if __name__== "__main__":
    main()