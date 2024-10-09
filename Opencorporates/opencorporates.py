import requests
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

# Directly assign your API key
api_key = 'kuxzDynT48fwx1i1oOoH'

# Base URL for searching companies
search_url = "https://api.opencorporates.com/v0.4/companies/search"



# List of U.S. state jurisdiction codes
us_states = [
    "us_al", "us_ak", "us_az", "us_ar", "us_ca", "us_co", "us_ct", "us_de", "us_fl", "us_ga",
    "us_hi", "us_id", "us_il", "us_in", "us_ia", "us_ks", "us_ky", "us_la", "us_me", "us_md",
    "us_ma", "us_mi", "us_mn", "us_ms", "us_mo", "us_mt", "us_ne", "us_nv", "us_nh", "us_nj",
    "us_nm", "us_ny", "us_nc", "us_nd", "us_oh", "us_ok", "us_or", "us_pa", "us_ri", "us_sc",
    "us_sd", "us_tn", "us_tx", "us_ut", "us_vt", "us_va", "us_wa", "us_wv", "us_wi", "us_wy"
]

# Function to fetch companies for a specific state with pagination
def fetch_companies_for_state(state_code, target_count=200):
    companies = []
    page = 1
    while len(companies) < target_count:
        params = {
            "q": "*",  # Search for all companies
            "jurisdiction_code": state_code,  # Search within the given state
            #"current_status": "Active",  # Filter for active companies
            "api_token": api_key,  # Use API key directly
            "per_page": 100,  # Fetch 100 companies per page
            "page": page
        }
        
        # Request to get the companies
        response = requests.get(search_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        search_data = response.json()
        new_companies = search_data["results"]["companies"]
        
        if not new_companies:
            break  # Break the loop if no more companies are found
        
        companies.extend(new_companies)
        page += 1
        
        # If fewer than the requested amount is found, no need to keep going
        if len(new_companies) < 100:
            break

    return companies[:target_count]  # Return only up to the target number of companies

# Create an empty list to hold all companies data
all_companies = []

# Loop through each state and fetch 200 companies
for state_code in us_states:
    print(f"Fetching companies for {state_code}...")
    companies = fetch_companies_for_state(state_code)
    print(f"Fetched {len(companies)} companies for {state_code}.")
    all_companies.extend(companies)
    
    # Delay to prevent hitting API rate limits
    time.sleep(1)

# Debug: Print total number of companies fetched
print(f"Total companies fetched: {len(all_companies)}")

# Create an empty list to hold formatted company data
formatted_data = []

# Loop through each company and extract all available fields dynamically
for company_entry in all_companies:
    company = company_entry['company']
    
    # Initialize a dictionary to hold all fields for this company
    company_data = {}
    
    # Add all fields dynamically by iterating over the company keys
    for key, value in company.items():
        # Convert any lists or complex data types to strings
        if isinstance(value, (list, dict)):
            company_data[key] = str(value)
        else:
            company_data[key] = value
    
    # Append the dynamic dictionary to the list
    formatted_data.append(company_data)

# Convert the list of dictionaries into a Pandas DataFrame
df = pd.DataFrame(formatted_data)

# Replace NaN values with empty strings
df.fillna('', inplace=True)

# Define the scope
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Add credentials to the service account (You need to create a credentials JSON from Google Cloud)
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/taeeunkwon/Desktop/MSA/EquifaxPracticum/Opencorporates/credentials.json', scope)
client = gspread.authorize(creds)

# Create a Google Sheet
sheet = client.create('Equifax Project Data')

# Share the Google Sheet with your personal Google account
sheet.share('tekwon2012@gmail.com', perm_type='user', role='writer')

# Select first sheet (default worksheet) and add the full table
worksheet1 = sheet.get_worksheet(0)

# Convert your DataFrame to a list of lists
data = df.values.tolist()

# Update the first sheet with the full data
worksheet1.update([df.columns.values.tolist()] + data)

# Now, create a new worksheet (tab) without the 'name' column
df_without_name = df.drop(columns=['name'])

# Add a new worksheet/tab (Google Sheets allows a maximum of 1000 rows by default)
worksheet2 = sheet.add_worksheet(title='Data without Name', rows=len(df_without_name)+1, cols=len(df_without_name.columns))

# Convert the DataFrame without 'name' column to a list of lists
data_without_name = df_without_name.values.tolist()

# Update the new worksheet with the data excluding the 'name' column
worksheet2.update([df_without_name.columns.values.tolist()] + data_without_name)

# Print the link to the newly created Google Sheet
spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{sheet.id}/edit"
print(f"Spreadsheet successfully created! You can view it here: {spreadsheet_url}")
