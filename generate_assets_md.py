import json

def generate_markdown():
    # Read the assets.json file
    with open('assets.json', 'r', encoding='utf-8') as f:
        assets = json.load(f)

    markdown = ''

    sections = {}

    for asset in assets:
        for network in asset.get('networks', []):
            if not network.get('type') or not network.get('chainPath'):
                continue

            type_lower = network['type'].lower()
            chain_path_lower = network['chainPath'].lower()

            key = f"{type_lower}|{chain_path_lower}"
            if key not in sections:
                sections[key] = {
                    'type': network['type'],
                    'chainPath': network['chainPath'],
                    'assets': []
                }

            sections[key]['assets'].append({
                'name': asset.get('name', ''),
                'symbol': asset.get('symbol', ''),
                'address': network.get('address') or network.get('contractId') or '',
                'decimals': network.get('decimals', ''),
                'type': network.get('type'),
                'chainPath': network.get('chainPath'),
                'assetId': network.get('assetId', '')
            })

    for key in sections:
        section = sections[key]
        type_lower = section['type'].lower()
        chain_path_lower = section['chainPath'].lower()

        if type_lower == 'ethereum':
            if chain_path_lower == 'eth.mainnet':
                heading = '## Ethereum L1'
            elif chain_path_lower == 'eth.sepolia':
                heading = '## Ethereum Sepolia Testnet'
            elif chain_path_lower == 'eth.foundry':
                heading = '## Ethereum Foundry'
            else:
                heading = f"## Ethereum {section['chainPath']}"
        elif type_lower == 'fuel':
            if chain_path_lower == 'fuel.mainnet':
                heading = '## Fuel Mainnet'
            elif chain_path_lower == 'fuel.testnet':
                heading = '## Fuel Testnet'
            elif chain_path_lower == 'fuel.devnet':
                heading = '## Fuel Devnet'
            else:
                heading = f"## Fuel {section['chainPath']}"
        else:
            heading = f"## {section['type']} {section['chainPath']}"

        markdown += f"{heading}\n\n"

        if type_lower == 'fuel':
            markdown += "| Name | Asset ID | Contract Address | Decimals |\n"
            markdown += "|------|----------|------------------|----------|\n"
        else:
            markdown += "| Name | Address | Decimals |\n"
            markdown += "|------|---------|----------|\n"

        for asset in section['assets']:
            name = asset['name']
            decimals = asset['decimals']
            address = asset['address']
            asset_id = asset.get('assetId', '')
            name_md = f"`{name}`" if name else ''
            decimals_md = f"`{decimals}`" if decimals != '' else ''
            asset_id_md = f"`{asset_id}`" if asset_id else ''

            if type_lower == 'ethereum' and address:
                if chain_path_lower == 'eth.mainnet':
                    etherscan_base = 'https://etherscan.io'
                elif chain_path_lower == 'eth.sepolia':
                    etherscan_base = 'https://sepolia.etherscan.io'
                else:
                    etherscan_base = 'https://etherscan.io'
                address_md = f"[`{address}`]({etherscan_base}/address/{address})"
            else:
                address_md = f"`{address}`" if address else ''

            if type_lower == 'fuel':
                markdown += f"| {name_md} | {asset_id_md} | {address_md} | {decimals_md} |\n"
            else:
                markdown += f"| {name_md} | {address_md} | {decimals_md} |\n"

        markdown += "\n"

    with open('assets.md', 'w', encoding='utf-8') as f:
        f.write(markdown)

    print('assets.md has been generated successfully.')

if __name__ == "__main__":
    generate_markdown()
