import requests
import json
import time
from pycoingecko import CoinGeckoAPI

with open("keys.json") as f:
    ALCHEMY_KEY = json.load(f)["alchemy_key"]

if ALCHEMY_KEY == "":
    print("error: you need to set your alchemy key inside keys.json")
    exit()

cg = CoinGeckoAPI()


class NFT:
    def __init__(self, name, addr, held=0, floor=0):
        self.name = name
        self.addr = addr
        self.held = held
        self.floor = floor

    def update_floor(self):
        url = (
            "https://eth-mainnet.g.alchemy.com/nft/v2/"
            + ALCHEMY_KEY
            + "/getFloorPrice?contractAddress="
            + self.addr
        )
        resp = requests.get(url=url)
        data = resp.json()

        if "error" in data["openSea"].keys() and "error" in data["looksRare"].keys():
            print(f"---cannot update floor price for {self.name}")
        elif (
            "error" not in data["openSea"].keys()
            and "error" not in data["looksRare"].keys()
        ):
            self.floor = min(
                data["openSea"]["floorPrice"], data["looksRare"]["floorPrice"]
            )
        elif "error" in data["openSea"].keys():
            self.floor = data["looksRare"]["floorPrice"]
        elif "error" in data["looksRare"].keys():
            self.floor = data["openSea"]["floorPrice"]

    def get_value(self):
        return self.floor * self.held


def load_nfts(fname):
    with open(fname) as f:
        allJson = json.load(f)

    nfts = []

    for i in allJson:
        _nft = NFT(i["name"], i["addr"], i["held"])
        nfts.append(_nft)

    return nfts


def print_totals(nfts):
    totals = [0, 0]
    print(
        "{0:20} {1:20} {2:10} {3:30}".format(
            "Collection", "Floor", "Quantity", "Value at floor"
        )
    )
    for nft in nfts:
        nft.update_floor()

        print(
            "{0:20} {1:<20} {2:<10} {3:<30}".format(
                nft.name, round(nft.floor, 3), nft.held, round(nft.get_value(), 3)
            )
        )

        totals[0] += nft.held
        totals[1] += nft.get_value()

    print(f"Total nfts held: {totals[0]}")
    price = cg.get_price(ids="ethereum", vs_currencies="usd")
    val_usd = totals[1] * price["ethereum"]["usd"]
    print(f"Total value: {round(totals[1], 3)} eth, ${round(val_usd, 2)}")


if __name__ == "__main__":
    nfts = load_nfts("nfts.json")
    print_totals(nfts)
