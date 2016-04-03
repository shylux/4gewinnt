cat starterbot.py minmax.py supibot.py > bot.py
sed -i '/from minmax.*$/d' bot.py
sed -i '/from starterbot.*$/d' bot.py
