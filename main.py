import requests
import json


with open("keys.json") as f:
    ALCHEMY_KEY = json.load(f)["alchemy_key"]

if ALCHEMY_KEY == "":
    print("error: you need to set your alchemy key inside keys.json")
    exit()


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
        try:
            self.floor = min(
                data["openSea"]["floorPrice"], data["looksRare"]["floorPrice"]
            )
        except:
            print(f"cannot update floor price for {self.name}")

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
    for nft in nfts:
        nft.update_floor()
        print(
            f"{nft.name} floor: {nft.floor}, holding: {nft.held}, value at floor: {nft.get_value()}"
        )
        totals[0] += nft.held
        totals[1] += nft.get_value()

    print(f"Total nfts held: {totals[0]}")
    print(f"Total value: {totals[1]}")


if __name__ == "__main__":
    nfts = load_nfts("nfts.json")
    print_totals(nfts)
