# Fuel Verified Assets

To keep our users safe and secure, Fuel has compiled this official list of verified assets that are available across our network.

Developers wishing to maintain a full list of on-chain assets should develop their own indexed solutions and be aware of the security risks that might exist by doing so.

## Using this repository

The information in this repository is published to a CDN maintained by Fuel. The current list of verified assets can be found at the following URL:

    https://verified-assets.fuel.network/assets.json

Any projects wishing to use this information are welcome to, however this is done at your own risk.

You can also download the latest asset information and icons in a single archive. This is great if you want to locally cache this list, or include it as part of a release pipeline in your own tools and libraries:

    https://verified-assets.fuel.network/latest.zip

## Submitting new assets

To submit new assets for inclusion in the verified assets list, [open a new Issue](https://github.com/FuelLabs/verified-assets/issues/new?assignees=&labels=update+info&projects=&template=submit_info.yml&title=Update+info+for+ASSET_NAME). Be sure to fill out all the fields on the issue form.

## Included Files

### `assets.json`

This is the list of assets that have been verified by the Fuel team. It contains critical information such as asset ids, chain information, and so on.

There are also lists to icons. If you chose to use those icons, please host them yourselves to be polite to Fuel's CDN.

This file is used to build the `assets.gen.json` file

### `assets.gen.json`

Finalized list of asset configurations. This file is published to the CDN, and is the format that should be used by all projects integrating with this repository.

It is built from the contents of the `assets.json` file using the `create_assets_json.py` script.

### `ASSETS.md`

User friendly list of all currently supported assets, including their network, addresses, and other metadata. It is built from the contents of the `assets.gen.json` file using the `create_assets_md.py` script.

### `config.json`

Configuration variables for bridge contracts, CDN URLs, and other information needed to generate the `assets.gen.json` and `ASSETS.md` files. It is used by the Python scripts.
