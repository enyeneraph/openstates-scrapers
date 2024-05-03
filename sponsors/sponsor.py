import json
import os
import click
import csv


def read_bills_from_state(state):
    bill_names = os.listdir(state)
    bills = [os.path.join(state, bill_name) for bill_name in bill_names if bill_name.startswith('bill')]
    return bills

def get_sponsor_data(bill_path, state, sponsors_data):
    with open(bill_path, 'r') as f:
        content = json.load(f)

    print(f'Retrieving data  for {bill_path} in {state}')

    if not content['sponsorships']:
        return sponsors_data

    for sponsor in content['sponsorships']:
        sponsor['person_id'] = json.loads(sponsor['person_id'].replace('~', ''))['name'] if sponsor['person_id'] is not None else ''
        sponsor['organization_id'] = json.loads(sponsor['organization_id'].replace('~', ''))['name'] if sponsor['organization_id'] is not None else ''
        sponsor['bill_id'] = content['_id']
        sponsor['state'] = state

        print(sponsor)
        sponsors_data.append(sponsor)
    return sponsors_data

def write_to_csv(sponsors_data):
    # Define the field names for the CSV
    fieldnames = ["name", "classification", "entity_type", "primary", "person_id", "organization_id", "bill_id", "state"]

    # Specify the filename for the CSV
    filename = "sponsorships.csv"

    # Write data to CSV
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
    
        # Write header
        writer.writeheader()  

        # Write rows
        for row in sponsors_data:
            # print(row)
            writer.writerow(row)

        print(f"CSV file '{filename}' has been created successfully.")

# @click.command()
# @click.option('--state', prompt='Your name',
#               help='The person to greet.')
def main():

    for state in os.listdir('_data'):
        sponsors_data=[]
        print('Retrieving data  for %s' %state)
        state_path = os.path.join(os.getcwd(),'_data', state)
        bills = read_bills_from_state(state_path)
        for bill in bills:
            sponsors_data = get_sponsor_data(bill, state, sponsors_data)  ###if I don't set it to a variabl, will it be changesd in polace?
        write_to_csv(sponsors_data)
    




if __name__== "__main__":
    main()