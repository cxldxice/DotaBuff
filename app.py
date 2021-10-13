import dotabuff
import json


def main():
    dota = dotabuff.DotaBuff()
    match = dota.get_match(6220194119)

    with open("match.json", "w") as file:
        json.dump(match, file, indent=4, sort_keys=True)


if __name__ == "__main__":
    main()