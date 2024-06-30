# %%
import pandas as pd
import json

# %%
final_df = pd.read_csv('data/final_dataframe.csv')
final_df

# %%
final_df['upc'] = final_df['upc'].astype('Int64').apply(
  lambda upc: None if pd.isna(upc) else str(upc)
)
final_df['tcin'] = final_df['tcin'].astype('Int64').apply(
  lambda tcin: None if pd.isna(tcin) else str(tcin)
)
final_df

# %%
tcin_values_of_non_missing_upc = final_df[
  ~final_df['upc'].isna()
]["tcin"].values

# %%
tcin_values_of_non_missing_upc

# %%
len(tcin_values_of_non_missing_upc)

# %%
with open('tasks/task_3/task_3_3/unique_products_urls.json', 'r', encoding = 'utf-8') as f:
  unique_products_dict_list = json.loads(f.read())

unique_products_dict_list

# %%
unique_products_df = pd.DataFrame(unique_products_dict_list)
unique_products_df

# %%
unique_products_df['tcin'] = unique_products_df['tcin'].astype('Int64').apply(
  lambda tcin: None if pd.isna(tcin) else str(tcin)
)
unique_products_df

# %%
tcin_df_non_missing_upc = pd.DataFrame(
  { 'tcin' : tcin_values_of_non_missing_upc }
)
tcin_df_non_missing_upc

# %%
result = unique_products_df.merge(
  tcin_df_non_missing_upc, 
  on = 'tcin', 
  how = 'left', 
  indicator = True
)
result

# %%
ids_unicos_df1 = result[result['_merge'] == 'left_only']
ids_unicos_df1

# %%
file_path = 'tasks/task_3/task_3_3/missing_products_urls.json'

with open(file_path, 'w', encoding = 'utf-8') as f:
  json.dump(
    ids_unicos_df1
      .drop('_merge', axis = 1)
      .to_dict(orient = 'records'), 
    f,
    ensure_ascii = False, 
    indent = 2
  )
