

fields = ["Registered_Address", "CEO", "Establishment_Year", "Number_Of_Employees", "Revenue_Size" ,
        "Website", "NAICS_Code", "SIC_Code", "Status", 
        "Dissolvement_Year","Company_Type","Previous_Names", "Alternative_Names", "Key_Executive_Personnel"]


## Use the following when using Gemini with Groudning
context_single_answer_v1 = """
I will ask you a series of questions about a company. Please provide the required information in a single answer,
making sure that your answer to each of my queries is separated by the following delimiter '*-*'. 
Simply write the answers in order separated by '*-*', do not repeat the questions or the field names.'
My questions are as follows: """


context_single_field_v1 = """
I will ask you a question about a company. Please provide the required information in a single answer,
do not repeat the questions or the field names. My question is as follows: """

field_to_query_v1 = {
    "Registered_Address": 
        """Tell me the Registered Adress for the firm named {firm_name}.
        Your answer should consist of the street address, city, state, country, and postal code.""",
    
    "CEO": 
        """Tell me the name and surname of the CEO for the firm named {firm_name}. 
        Your answer should be in the format 'Name Surname'""",
    
    "Establishment_Year": 
        """Tell me the establishment year of {firm_name}. 
        Your answer should be 4 digits in the format YYYY""",
    
    "Number_Of_Employees": 
        """Tell me the estimated number of employees for the firm named {firm_name}. 
        Your answer should be an approximate range, like 1-10, 10-100, 100-1000, 1000-10000, 10000+ etc. 
        You can specify other ranges like 200-250 if you wish.""",
    
    "Revenue_Size": 
        """Tell me the estimated annual revenue in dollars for the firm named {firm_name}. 
        Your answer should be an approximate range, 10000-100000, 1000000-10000000, or 1000000000+ etc. 
        You can specify other ranges like 200-250 if you wish.""",
    
    "Website": 
        """Tell me the url of the official website of for the firm named {firm_name}.
        If you can't find a website for the firm, please write 'No website found'""",
    
    "NAICS_Code": 
        """Tell me the numeric NAICS code for the firm named {firm_name}.""",
    
    "SIC_Code": 
        """Tell me the numeric SIC code for the firm named {firm_name}.""",
    
    "Status": 
        """Tell me whether the firm named {firm_name} is Active or Dissolved.
        Answer with one word.""",
    
    "Dissolvement_Year": 
        """Tell me the year when the firm named {firm_name} was dissolved. 
        Your answer should be 4 digits in the format YYYY. If the firm has not been dissolved, please respond with 'N/A'.""",
    
    "Company_Type":
        """Tell me the type of company for the firm named {firm_name} (e.g., Public, Private, Partnership, LLC, etc.).""",
    
    "Previous_Names": 
        """List any previous names that the firm named {firm_name} has had. 
        If there are no previous names, please respond with 'N/A'.""",
    
    "Alternative_Names": 
        """Tell me if there are any alternative or trade names for the firm named {firm_name}. 
        If none, please respond with 'N/A'.""",
    
    "Key_Executive_Personnel": 
        """List the key executive personnel for the firm named {firm_name}, including their names and job titles.
        If there are no key executive personnel, please respond with 'N/A'."""
}


answer_format_v1 = """
If you have absolutely no idea on how to answer a query for a given field you can answer 'No information found' for that field. 
Do not leave the answer blank or give me a long explanation on why you couldn't find the answer or an explanation of your answer.
If you find multiple possible answers return your best answer.
To reiterate i just want you to give a short answer in the format described above for each field. Do not give me a long textual response."""


context_local_dataset_v1 = """
I will give you potentially relevant information I have gained from web search results and the scraped contents of certain websites that I gathered by searching online for the firm name and each field. 
You can use your own knowledge or the data i provide below to answer the question.
The relevant information i give you will will be in Json format. Some websites may have failed the webscraping procedure, so the data may be incomplete.
"""


general_context = """
You will be assisting me with filling in data fields for a firm database I am building.
I will tell you the name of the firm i am interested in, and a certain datafield whose value I want you to fill for that firm.
I will give you potentially relevant information I have gained from web search results and the scraped contents of certain websites that I gathered by searching for the firm name and field.
You can use your own knowledge, the data i provide below, or previous data from the chat session to answer the question.
The relevant information i give you will will be in Json format.
You will give your answer by simply stating the value of the field in the required format based on my below prompt.
If you have absolutely no idea about the answer, then you can answer with 'No information Found' .
"""