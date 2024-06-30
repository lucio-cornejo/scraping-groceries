# %%
from src.instances import config

import json
import boto3

# %%
with open('data/products_urls_for_task_3.3.json', 'r', encoding = 'utf-8') as f:
  products_basic_info_dicts_list = json.loads(f.read())

products_basic_info_dicts_list

# %%
len(products_basic_info_dicts_list)

# %%
max_index_shift = 100
iteration = 0
indices = []

while (iteration*max_index_shift < len(products_basic_info_dicts_list)):
  indices.append([
    iteration * max_index_shift,
    max_index_shift + iteration * max_index_shift
  ])
  
  iteration += 1

indices[-1][-1] = len(products_basic_info_dicts_list)

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
subnet = 'subnet-0e963910ab4b5e151'

# %%
for index_pair in indices:
  first_index = str(index_pair[0])
  last_index = str(index_pair[1])
  print(f'Last list index is {last_index}')

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
        'subnets': [subnet],
        'assignPublicIp': 'ENABLED'
      }
    }
  )

  # Print the response
  print(response)

  # break