import scrapy
from scrapy.exceptions import CloseSpider
import re
import sys
sys.path.append('../../')
from school_codes import school_codes_lst


class MadSchoolSpider(scrapy.Spider):
  global school_codes_lst
  name = 'mad_schools'
  start_urls = [f'http://www.madrid.org/wpad_pub/run/j/MostrarFichaCentro.icm?cdCentro={code}' for code in school_codes_lst[70:90]]

  def parse(self, response):
    info_list = response.css('.pSizeSB strong::text').getall()
    school = {
      'name': response.css('.pSizeMB strong::text').get(),
      'denomination': info_list[0],
      'type': info_list[1],
      'titular': info_list[2],
      'code': info_list[3],
      'territorial_zone': info_list[4],
      'address': info_list[5],
      'street_number': info_list[6],
      'postcode': info_list[7],
      'city': info_list[8]
    }
    # compile patterns to check in results
    nine_digits = re.compile(r'\d{9}')
    parenthesis = re.compile(r'\(.*\)')
    www = re.compile(r'w{3}')
    e_mail = re.compile(r'\S+@\S+')
    # general information
    if re.search(nine_digits, info_list[9]):
      school['telephone'] = re.findall(nine_digits, info_list[9])
      if re.search(nine_digits, info_list[10]):
        school['fax'] = re.findall(nine_digits, info_list[10])
    elif re.search(parenthesis, info_list[9]):
      school['zone'] = info_list[9]
      if re.search(nine_digits, info_list[10]):
        school['telephone'] = re.findall(nine_digits, info_list[10])
        if re.search(nine_digits, info_list[11]):
          school['fax'] = re.findall(nine_digits, info_list[11])
    for i in range(10, len(info_list)):
      if re.search(www, info_list[i]) and not re.search(e_mail, info_list[i]):
        school['webpage'] = info_list[i].strip()
    if len([email.strip() for email in response.css('.pB strong::text').getall()]) > 0:
      school['email'] = [email.strip() for email in response.css('.pB strong::text').getall()]
    # stages
    stages = [string for string in [strg.strip() for strg in response.css('#capaEtapasContent td::text').getall()] if string != '']
    stage_types = [string for string in [strg.strip() for strg in response.css('#capaEtapasContent .pNegro::text').getall()] if string != '']
    stages = stages[len(stages)-len(stage_types):]
    for i in range(len(stages)):
      school[stages[i]] = stage_types[i]
    # print(response.css('.pSizeSB strong::text').getall())
    yield school