from copy import deepcopy
import json
import os
import hashlib

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets.json'), 'r') as infile:
	assets = json.load(infile)

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json'), 'r') as infile:
	config = json.load(infile)

def parse_address_to_bytes(address):
    if address.startswith('0x'):
        address = address[2:]  # Remove the '0x' prefix
    return bytes.fromhex(address)

def pad_address(address, byte_len):
	hex_address = address.hex()
	padded_hex_address = hex_address.zfill(byte_len)
	return bytes.fromhex(padded_hex_address)

def sha256(*data):
	bytes_to_hash = bytearray()
	for piece in data:
		bytes_to_hash.extend(piece)
	return hashlib.sha256(bytes_to_hash)

def get_l1_network_config_from_fuel(networks, type, chain):
	for network in networks:
		if network.get('type') == type and network.get('chain') == chain:
			return network

def generate_fuel_network_config(asset, chain, network):
	base_config = config['fuelAddressConfig'][chain]
	l1_network = get_l1_network_config_from_fuel(asset['networks'], base_config['l1_type'], base_config['l1_chain'])
	if l1_network is None:
		del network
		return

	l1_chain_id = config['chainIds'][base_config['l1_type']][base_config['l1_chain']]
	l1_contract_address = l1_network['address']

	# set the contract ID
	network['contractId'] = base_config['l2_contract']
	sub_id = calculate_fuel_sub_id(l1_chain_id, l1_contract_address)
	asset_id = calculate_fuel_asset_id(network['contractId'], sub_id)
	network['subId'] = f'0x{sub_id.hexdigest()}'
	network['assetId'] = f'0x{asset_id.hexdigest()}'

	return

def calculate_fuel_sub_id(chain_id, address):
	# chain ID is always 1
	# https://github.com/FuelLabs/fuel-bridge/blob/0b6e3b198707d9fd7000d255b0ad3164d7e64507/packages/fungible-token/bridge-fungible-token/implementation/src/main.sw#L496
	chain_id = '1'.encode('utf-8') # chain ID in ASCII
	token_id = bytes(32) # zeros, not used

	# parse eth address and ensure padding
	parsed_address = parse_address_to_bytes(address)
	padded_address = pad_address(parsed_address, 64)

	return sha256(chain_id, padded_address, token_id)

def calculate_fuel_asset_id(contract_id, sub_id):
	parsed_contract_id = parse_address_to_bytes(contract_id)
	return sha256(parsed_contract_id, sub_id.digest())

def generate_final_assets():
	local_data = []
	cdn_data = []

	# Generate final asset config
	for asset in assets:
		converted_asset = deepcopy(asset)

		for network in converted_asset["networks"]:

			# Convert type and chain to chainId
			network_type = network['type']
			chain = network['chain']
			network["chainId"] = config['chainIds'][network_type][chain]

			if network_type == "fuel" and network.get('assetId') is None:
				generate_fuel_network_config(converted_asset, chain, network)

		# write out the local version
		local_data.append(deepcopy(converted_asset))

		# Update the icon to use the proper full cdn path
		converted_asset['icon'] = config['cdn']['icon'] + converted_asset['icon']
		cdn_data.append(converted_asset)

	# Compressed CDN output with full CDN URLs
	with open('assets.local.gen.json', 'w') as f:
		json.dump(local_data, f, separators=(',', ':'))

	# Compressed output for ZIP file
	with open('assets.cdn.gen.json', 'w') as f:
		json.dump(cdn_data, f, separators=(',', ':'))

	# Uncompressed output for repo
	with open('assets.gen.json', 'w') as f:
		json.dump(local_data, f, indent=2)

	print('Asset file regenerated')

if __name__ == "__main__":
    generate_final_assets()
