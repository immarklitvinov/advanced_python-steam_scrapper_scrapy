# Scrapy steam parser

## Как делал?

1. Сделал `scrapy startproject steamscrapper`
2. Создал паука (steamscrapper/steamscrapper/spiders/steam.py)
3. Разобрался с `scrapy shell`
4. Разобрался с виртуальными окружениями и разными питонами
5. Написал паука, сделал `scrapy crawl steam -O output.json`
6. Сделал `cat output.json | jq . > pretty_output.json` чтобы получить красивый выходной файлик
7. Можно наслаждаться
