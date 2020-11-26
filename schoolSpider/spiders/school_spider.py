import scrapy
from scrapy.exceptions import CloseSpider

class SchoolSpider(scrapy.Spider):
  name = 'schools'
  # Due to a bug on the site a gentler crawling needed 
  #start_urls = [f'http://colesyguardes.es/colegios/{num}' for num in range(1,15)]
  start_urls =  ['http://colesyguardes.es/colegios/1']
  
  def parse(self, response):
    for div in response.css('.searchResult-item'):
      school = {
        'name': div.css('.lnk-profile-header::text').get(),
        'address': div.css('.item-info p::text').getall()[0],
      }
      try:
        school['telephone'] = div.css('.item-info p::text').getall()[2]
      except:
        pass
      yield school
    # Creates basically a synchronous crawler which doesn´t 
    # affect the functioning of the target page 
    next_page = f'/colegios/{int(str(response)[38:-1])+1}'
    if next_page is not None and next_page != '/colegios/116':
      yield response.follow(next_page, callback=self.parse)



# with open('schools_test.txt', 'a') as f:
    #   for line in schools:
    #     f.write(f'{line}\n')
      
    