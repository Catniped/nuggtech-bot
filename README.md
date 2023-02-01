**Quickstart guide**

Clone the repo onto your host.

Install the dependencies:
`pip install -r requirements.txt`

Go to the discord developer portal and create a new application, then create a bot (dont close this page, ull need it in a minute).

Open `config.toml` and fill out the values

Quick refference table:
| Value | Description |
| ----------- | ----------- |
| broadcastserver | Boolean, `True` will display a tag infront of messages originating from your server, displaying your servers name. |
| servername | The name that will be broadcasted. |
| hostname | IP of the mqtt broker. |
| username | Username used for access to the mqtt broker. |
| password | Password used for access to the mqtt broker. |
| port | Port of the mqtt broker. |
| botid | Application ID of the bot, get this in the developer portal. |
| bottoken | Token of the bot, get this in the developer portal. |
| chanid | ID of the channel in which the chatbridge will initialize. |
| outtopic | The topic on which the messages from the server will be broadcasted. Reccomended format: servername/number |
| intopics | Topics on which the bot will listen for messages. Use # if you want to subscribe to all topics (will mirror your messages). |
| status | The status the bot will display on discord. |

Now, start the bot.py script. If the config was filled out properly, the bot should connect to the mqtt broker and start functioning!