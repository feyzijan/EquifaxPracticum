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

def fetch_companies_for_state(state_code, target_count=60):
    companies = []
    page = 1
    while len(companies) < target_count:
        params = {
            "q": "*",  # Search for all companies
            "jurisdiction_code": state_code,  # Search within the given state
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
        
        # Filter companies based on incorporation_date
        for company in new_companies:
            incorporation_date = company['company'].get('incorporation_date')
            if incorporation_date and incorporation_date.startswith("2024"):
                companies.append(company)
                if len(companies) >= target_count:
                    break
        
        page += 1
        
    return companies[:target_count]  # Return only up to the target number of companies

# Create an empty list to hold all companies data
all_companies = []

# Loop through each state and fetch 60 companies established in 2024
for state_code in us_states:
    print(f"Fetching companies for {state_code}...")
    companies = fetch_companies_for_state(state_code, target_count=60)
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

# Sort the DataFrame by 'industry_codes' while keeping all rows
df_sorted = df.sort_values(by='industry_codes', ascending=True, na_position='last')

# Save the sorted DataFrame locally as a CSV file
df_sorted.to_csv("../EquifaxPracticum/Opencorporates/equifax_project_data_sorted.csv", index=False)
print("Full data saved to equifax_project_data.csv")

# Create a DataFrame without the 'name' column
df_without_name = df.drop(columns=['name'])

# Save the DataFrame without 'name' locally as another CSV file
df_without_name.to_csv("../EquifaxPracticum/Opencorporates/Eequifax_project_data_without_name_.csv", index=False)
print("Data without 'name' column saved to equifax_project_data_without_name.csv")