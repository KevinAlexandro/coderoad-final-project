# CodeRoad Final Project

Install:
* Java JDK 12
* Python 3.11
* Spark 3.5.5
Run the following command to install the required packages:
```bash
pip install -r requirements.txt
```
There are 3 files that can be executed:
1. `datagenerator/datagenerator.py`: This script generates synthetic data for the project. Use `constants.py` to change the parameters of the data.
2. `etl/etl.py`: This script will process the data using spark
3. `llms/chat_bot.py`: This script will run the chat bot.