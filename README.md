# Asynchronous-Cowin-Telegram-Bot
A telegram bot that searches for your vaccination centeres/slots available in the specified pincode for next 5 dates every 5 minutes and filters out the one you look for based on the keyword specified.

For example, Let's say this is the configuration:
```
PINCODE = 248001
SEARCH_WORD = "ganpati"
```

There are 3 vaccination centers for the Pin 248140:
* CHC Doiwala  
* Ganpati Wedding P.Bhaniyawala  
* Dudhli  

Since the specified keyword "ganpati" matches with the second vaccination center, it will keep track of availability of vaccination slots in that location. And whenever there is any free slot available, it will send a message to the user on telegram.

It also has a functionality when you want to check for slots in other vaccination centers in the same pincode on the go. You can trigger the "check" function and pass it any other keyword that matches with the vaccination slots in the specified pincode.
