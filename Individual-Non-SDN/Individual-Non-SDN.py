import pandas as pd
import json
import numpy as np

main_df = pd.read_excel('./Individual-Non-SDN-Main.xlsx')
identifications_df = pd.read_excel('./Individual-Non-SDN-Identifications.xlsx')
aliases_df = pd.read_excel('./Individual-Non-SDN-Aliases.xlsx')
addresses_df = pd.read_excel('./Individual-Non-SDN-Address.xlsx')
main_df = main_df.where(pd.notnull(main_df), None)
identifications_df = identifications_df.where(pd.notnull(identifications_df), None)
aliases_df = aliases_df.where(pd.notnull(aliases_df), None)
addresses_df = addresses_df.where(pd.notnull(addresses_df), None)
main_data = main_df.to_dict(orient='records')
identifications_data = identifications_df.to_dict(orient='records')
aliases_data = aliases_df.to_dict(orient='records')
addresses_data = addresses_df.to_dict(orient='records')
merged_data = {}

for entry in main_data:
    entry_id = entry['ID']
    merged_data[entry_id] = entry
    merged_data[entry_id]['Identifications'] = []
    merged_data[entry_id]['Aliases'] = []
    merged_data[entry_id]['Addresses'] = []
    for identifications_entry in identifications_data:
        if identifications_entry['ID'] == entry_id:
            merged_data[entry_id]['Identifications'].append(identifications_entry)
    for alias_entry in aliases_data:
        if alias_entry['ID'] == entry_id:
            merged_data[entry_id]['Aliases'].append(alias_entry)
    for address_entry in addresses_data:
        if address_entry['ID'] == entry_id:
            merged_data[entry_id]['Addresses'].append(address_entry)

merged_data_list = list(merged_data.values())
with open('Individual-Non-SDN.json', 'w') as f:
    json.dump(merged_data_list, f, indent=2, default=str)

print("Merged data saved to Individual-Non-SDN.json")