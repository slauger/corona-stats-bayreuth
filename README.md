# corona-stats-bayreuth

## background

[landkreis-bayreuth.de](https://www.landkreis-bayreuth.de/der-landkreis/pressemitteilungen/) does not provide an api for the corona stats, so i decided to write a small crawler to extract the data.

## example usage

### print the latest available data

```
-bash$ ./corona-bt.py | jq 
[
  {
    "date": "2020-11-02 00:00:00",
    "inzidenz": {
      "land": 99.35,
      "stadt": 128.37
    },
    "infected": {
      "current": {
        "land": 140,
        "stadt": 160
      },
      "total": {
        "land": 659,
        "stadt": 492
      }
    },
    "patients": {
      "total": 0,
      "local": 0
    },
    "deaths": {
      "land": 27,
      "stadt": 10
    },
    "recovered": {
      "land": 492,
      "stadt": 331
    }
  }
]
```

### print all entries on the first page

```
-bash$ ./corona-bt.py -a | jq
```

## jq examples

```
./corona-bt.py | jq .[0].inzidenz.land
./corona-bt.py | jq .[0].inzidenz.stadt

./corona-bt.py | jq .[0].infected.current.land
./corona-bt.py | jq .[0].infected.current.stadt

./corona-bt.py | jq .[0].infected.total.land
./corona-bt.py | jq .[0].infected.total.stadt
```
