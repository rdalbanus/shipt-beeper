# Shipt beeper

This python script will automate checking for open slots on shipt so that you don't need to keep refreshing their website all day in the hopes that there is a delivery window available.

The script uses a Slack webhook to send you a direct message, but that is not necessary to set up - you can just keep it running on the background and checking the output periodically.

Usage: 
```
python check_open_slots.py
```

Thanks [@Vivek Rai](https://github.com/raivivek) for [the idea](https://github.com/raivivek/til/blob/master/misc/covid-19-and-groceries.md) and help troubleshooting.