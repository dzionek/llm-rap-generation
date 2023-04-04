To reproduce the results:
1. Register with the [Genius API](https://docs.genius.com) to get your API token.
2. Replace [API_TOKEN] with your token.
```shell
python main.py [API_TOKEN] rapper_list.txt -m 100
```

The command extracts top 100 lyrics for artists from the file `rapper_list.txt`.