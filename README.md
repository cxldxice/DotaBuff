# DotaBuff
> lib for dotabuff.com 

## Install 
From GitHub: `git clone https://github.com/cxldxice/DotaBuff.git` (all versions)

From pip: `pip3 install dotabuff` (only stable)

## Example
```python
import dotabuff
import json


def main():
    dota = dotabuff.DotaBuff()
    match = dota.get_match(6220194119)

    with open("match.json", "w") as file:
        json.dump(match, file, indent=4, sort_keys=True)


if __name__ == "__main__":
    main()
```

## Methods
- `DotaBuff.get_match(id)`


## Updates

### 1.0 (beta)
- Add get_match method

---
`by @cxldxice with ♥`