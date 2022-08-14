# nft-portfolio-tracker

Uses Alchemy's new NFT API to calculate portfolio value. This doesn't take into account traits but gives you an overall estimate based on the floors of the input collections.
Alchemy currently only checks OpenSea and LooksRare.

## How to use

### Add your Alchemy key
Modify keys.json to include your Alchemy API key as follows:
``` json
{
    "alchemy_key": "your_key_here"
}
```
If you don't already have an API key, make an [Alchemy](https://alchemy.com) account and create a project.

### Add your portfolio

Portfolio tracking happens manually based on the information entered into nfts.json. I might update it in the future to calculate based on wallet address.

nfts.json looks like this by default:
```json
[
    {"name": "BAYC", "addr": "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D", "held": 1},
    {"name": "MAYC", "addr": "0x60E4d786628Fea6478F785A6d7e704777c86a7c6", "held": 1},
    {"name": "Pudgy Penguins", "addr": "0xBd3531dA5CF5857e7CfAA92426877b022e612cf8", "held": 2}
]
```
Modify it to contain your own portfolio values:
```json
[
    {"name": "Azuki", "addr": "0xED5AF388653567Af2F388E6224dC7C4b3241C544", "held": 1},
    {"name": "Doodles", "addr": "0x8a90CAb2b38dba80c64b7734e58Ee1dB38B8992e", "held": 1},
    {"name": "Pudgy Penguins", "addr": "0xBd3531dA5CF5857e7CfAA92426877b022e612cf8", "held": 8},
    {"name": "Milady", "addr": "0x5Af0D9827E0c53E4799BB226655A1de152A425a5", "held": 2}
]
```
### Run it
```
python main.py
```
Example output:
```
Collection           Floor                Quantity   Value at floor
Azuki                7.1                  1          7.1
Doodles              7.985                1          7.985
Pudgy Penguins       2.79                 8          22.32
Milady               0.483                2          0.966
Total nfts held: 12
Total value: 38.371 eth, $76181.76
```


