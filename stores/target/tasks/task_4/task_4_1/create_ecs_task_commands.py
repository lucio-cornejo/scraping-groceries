# %%
import os; os.chdir('./../../../')

# %%
from src.instances import config

import json
import re
import boto3

# %%
with open('data/unique_products_urls.json', 'r', encoding = 'utf-8') as f:
  unique_products_urls = json.loads(f.read())

unique_products_urls

# %%
len(unique_products_urls)

# %%
indices = []
max_index_shift = 150
iteration = 0

while (iteration*150 < len(unique_products_urls)):
  indices.append([
    iteration * max_index_shift,
    max_index_shift + iteration * max_index_shift
  ])
  
  iteration += 1

indices[-1][-1] = len(unique_products_urls)

indices

# %%
# Initialize a session using Amazon ECS
client = boto3.client(
  'ecs',
  aws_access_key_id = config['aws']['access_key_id'],
  aws_secret_access_key = config['aws']['access_key_secret'],
  region_name = config['aws']['region']
)


# Define the parameters for the run_task call
cluster_name = 'scraping'
task_definition = 'node-async-test'
container_name = 'node-async-test'

# %%
for index_pair in indices:
  first_index = str(index_pair[0])
  last_index = str(index_pair[1])

  overrides = {
    'containerOverrides': [
      {
        'name': container_name,
        'environment': [
          {'name': 'PRODUCTS_JSON_LIST_FIRST_INDEX', 'value' : first_index },
          {'name': 'PRODUCTS_JSON_LIST_LAST_INDEX', 'value': last_index }
        ]
      }
    ]
  }

  # Run the ECS task
  response = client.run_task(
    cluster = cluster_name,
    taskDefinition = task_definition,
    overrides = overrides,
    count = 1,
    launchType = 'FARGATE',
    networkConfiguration = {
      'awsvpcConfiguration': {
        'subnets': ['subnet-0e963910ab4b5e151'],
        'assignPublicIp': 'ENABLED'
      }
    }
  )

  # Print the response
  print(response)

  break
