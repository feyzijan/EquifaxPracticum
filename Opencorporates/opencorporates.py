import requests
import pandas as pd
import time

# Directly assign your API key
api_key = 'kuxzDynT48fwx1i1oOoH'

# Base URL for searching companies
search_url = "https://api.opencorporates.com/v0.4/companies/search"

# Function to fetch companies that satisfy the conditions
def fetch_companies_with_industry_and_date(target_count=1000):
    companies = []
    page = 1
    total_fetched = 0  # Counter for tracking the total fetched companies

    while len(companies) < target_count:
        params = {
            "q": "*",  # Search for all companies
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
        
        # Filter companies based on conditions
        for company in new_companies:
            company_data = company['company']
            incorporation_date = company_data.get('incorporation_date')
            industry_codes = company_data.get('industry_codes')
            
            # Check both conditions
            if incorporation_date and incorporation_date.startswith("2024") and industry_codes:
                companies.append(company_data)
                total_fetched += 1  # Increment the counter

                # Notify when every 50 companies are added
                if total_fetched % 50 == 0:
                    print(f"Added {total_fetched} companies to the list so far.")

                if len(companies) >= target_count:
                    break
        
        page += 1
        time.sleep(1)  # Delay to prevent hitting API rate limits
    
    return companies[:target_count]

# Fetch the companies
print("Fetching companies...")
filtered_companies = fetch_companies_with_industry_and_date(target_count=1000)
print(f"Fetched {len(filtered_companies)} companies with industry codes and 2024 incorporation date.")

# Convert the filtered companies into a Pandas DataFrame
df_filtered = pd.DataFrame(filtered_companies)

# Replace NaN values with empty strings
df_filtered.fillna('', inplace=True)

# Save the filtered DataFrame locally as a CSV file
df_filtered.to_csv("../EquifaxPracticum/Opencorporates/equifax_filtered_companies.csv", index=False)
print("Filtered data saved to equifax_filtered_companies.csv")