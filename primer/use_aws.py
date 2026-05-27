# Import necessary libraries
import os                                     
from strands import Agent                    
from strands.models.anthropic import AnthropicModel  
from strands_tools import use_aws           
from dotenv import load_dotenv              

load_dotenv()
model = AnthropicModel(
    client_args={"api_key": os.getenv("api_key"),},
    max_tokens=1028,                    
    model_id="claude-sonnet-4-20250514",  
    params={ "temperature": 0.3,              
    }
)
agent = Agent(model=model, tools=[use_aws])
query= "List the S3 buckets in my account"  
query="Query the DynamoDB table called 'UserProfiles' in the us-west-2 region. Get all items for userId 'user123' and show me the results in a readable format."  
query="Find all users in the 'UserProfiles' table in the us-west-2 region who have an attribute 'status' of 'Active', show me their names and email addresses."
response = agent(query)
