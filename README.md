# PokemonAdventureBot
### on Telegram


![](https://cdn4.telesco.pe/file/Sp_hBkulWtHvOA3If1O8cwmLVvBxFH62vlnowong_EapipGBrD7tc6VO9UiJBbKqc3qHIUfhk41JfWyBzQG92vKV15aj62fynmn4XCl9j2X-fcziSjgGFQDyahbIUpjGlLmvijKuWEIsxu_uCqMabMaHbDHq6KUNUROut7qKI5xg0NlVL6zlFkO3nNgUY0dG6S5ibXK0wTbLA4rIOCUEQW2pfm-1eSuqotl7NWBLigurLKXIL_oHOz-N8FUHOVtb5XL2dwmnCxWjZ36N25m6NRbh1rru_V5VuF1Qq-YH13VhF99DXs83lwvOq7GEqM9f5IsoUwEy1IlqszzZ-Dd2HA.jpg)


____________

# About
Are you also nostalgic and dream your way back to the time when you played the first generations of Pokemon (red, blue & yellow) on the Gameboy or Gameboy Color? Then this project is surely something for you! We (Divirad) are currently developing a telegram bot for all nostalgic Pokemon fans, which we will host ourselves. The goal of this project is that in the end we will have a bot with all the old original game mechanics from the games red, blue and yellow. Read more in the roadmap.

# You are just a user?

Then go to the official [Pokemon Adventure Telegram Bot!](https://t.me/pokemonadventurebot) and have fun! :)

![](https://img.shields.io/badge/Bot-not%20running-red.svg)

# You are a developer?

### What do I need to run the bot?

![](https://img.shields.io/badge/Python-3.6-green.svg)

![](https://img.shields.io/badge/MySQL-5.7.X-orange.svg)

The following modules:

![](https://img.shields.io/badge/p.t.b-10.1-grey.svg) or higher

![](https://img.shields.io/badge/mysqlclient-2.13.12-grey.svg) or higher

![](https://img.shields.io/badge/gitpython-2.1.9-grey.svg) or higher

`pip install python-telegram-bot mysqlclient gitpython`

How do I get set up?

* type `git clone https://bitbucket.org/divirad/pokemonadventure.git` into your console
* go to the cloned directory
* Go on Telegram:
  * Create two Bots with @botfather and one channel
  * Create one Channel
* MySQL:
  * Create a Database named `pokemon`
  * Add the file pokemonadventure/PokemonAdventure/private.py and add:

 ```
  admin_token = "<YOUR-ADMIN-BOT-TOKEN>""
  admins = ["<USER 1>", "<USER 2>" ...]
  admin_channel = "<YOUR-ADMIN-CHANNEL>"
  token="<YOUR-MAIN-BOT-TOKEN>"
  database_passwd = "<YOUR-MYSQL-PASSWORD>"
  database_user = "<YOUR-MYSQL-USer>"

  log_file = "<YOUR-LOG-FILE-PATH>"
  map_file = "<YOUR-MAP-FILE-PATH>"
```
  

 Run the bot with Python3.6 or higher
 Type `/start_bot` into your admin bot
 Have fun :)

## How to contribute?

You can contribute to this project by cloning the projectfrom our Github repository and testing it. Of course you can also post ideas for features or suggestions for improvement either in the repository under Issues or via  Utopian.io. You can also contact me via [Telegram](t.me/kurodevs)! 

Of course you can also fork the project and if you think you have an improvement in, then you are welcome to do a pull request. If we like it, we will merge it with the project.
## Who do I talk to?

Divirad(c) 2017-2018

