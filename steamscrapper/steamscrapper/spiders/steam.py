import scrapy
from bs4 import BeautifulSoup


class SteamSpyder(scrapy.Spider):
    name = "steam"

    def start_requests(self):
        search_requests = ['left4dead', 'cs', 'drift']
        url_pattern = 'https://store.steampowered.com/search/?cc=us&term'
        pages_amount = 5
        
        for search_request in search_requests:
            for page_number in range(1, pages_amount + 1):
                current_url = f'{url_pattern}={search_request}&page={page_number}'                
                yield scrapy.Request(url=current_url, callback=self.parse_page)


    def parse_page(self, response):
        games_container = response.xpath('//div[@id="search_resultsRows"]')[0].css('a')
        for game_container in games_container:
            game_url = game_container.css('a::attr(href)')[0].get() 
            game_title = game_container.css('span.title::text')[0].get() # 'Nova Drift'
            game_platforms = game_container.css('span.platform_img::attr(class)').getall() # ['platform_img win', 'platform_img mac']
            game_price = game_container.css('div.search_price::text').getall()[-1].strip() # '$10'
            try:
                game_release_date = game_container.css('div.search_released::text').getall()[0] # '27 Jul, 2022'
            except:
                game_release_date = 'not stated'
            
            params = {
                'title': game_title,
                'platforms': list(map(lambda x: x.split()[1], game_platforms)),
                'price': game_price,
                'release_date': game_release_date,
                'url': game_url
            }
            
            yield scrapy.Request(game_url, self.parse_game, meta=params)
        
    def parse_game(self, response, **kwargs):
        game_category = ' > '.join(response.css('div.blockbg a::text').getall()[1:])
        game_dev_list = (''.join(response.xpath('//div[@id="developers_list"]').css('::text').getall()[1:-1])).split(', ')
        game_tags_list = list(map(lambda x: x.strip(), response.xpath('//div[@class="glance_tags popular_tags"]').css('a::text').getall()))
        try:
            game_reviews_rate, game_reviews_amount = response.xpath('//div[@class="user_reviews"]')[0].css('div.user_reviews_summary_row')[-1].css('span::text').getall()[:2]
            game_reviews_rate = game_reviews_rate.strip()
            game_reviews_amount = game_reviews_amount.strip()[1:-1]
            yield {
                'title': response.meta.get('title'),
                'category': game_category,
                'reviews_amount': game_reviews_amount,
                'general_review': game_reviews_rate,
                'release_date': response.meta.get('release_date'),
                'developers': game_dev_list,
                'tags': game_tags_list,
                'price': response.meta.get('price'),
                'platforms': response.meta.get('platforms')
            }
        except:
            # print('''ERROR: didn't work with\n\n''' + response.meta.get('url') + '\n\n')
            pass
        
        
        
        