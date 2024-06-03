This is currently stub documentation for pull counter.

To use any of this, you would need to get a public key from FFLogs so that you can use their API. 

# Getting Current Pull Count

```commandline
python .\get_current_pull_count.py --help
usage: get_current_pull_count.py [-h] -u INPUT_URL -f FIGHT_CODE

Periodically poll a given fflogs log (presumed live logging) and update pull counts for stream.

options:
  -h, --help            show this help message and exit
  -u INPUT_URL, --url INPUT_URL
                        FFLogs URL that's currently being live logged to
  -f FIGHT_CODE, --fight_code FIGHT_CODE
                        Fight abbreviation that we want to track counts for
```

Fight codes currently supported can be found in pull_count_config.yml.

# Reprocessing Previous Logs

# TODO

- Make processed entries available to Google Sheets for summarization