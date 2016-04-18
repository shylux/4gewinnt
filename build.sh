cat starterbot.py transposition.py minmax.py supibot.py > bot.py
sed -i '' '/from minmax.*$/d' bot.py
sed -i '' '/from starterbot.*$/d' bot.py
sed -i '' '/from transposition.*$/d' bot.py
