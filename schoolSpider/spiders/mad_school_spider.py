import scrapy
from scrapy.exceptions import CloseSpider
import re
import sys
sys.path.append('../../')
from school_codes import school_codes_lst


class MadSchoolSpider(scrapy.Spider):
  '''Collects general information on nurseries, schools, high schools and 
  vocational colleges in Madrid'''
  global school_codes_lst
  name = 'mad_schools'
  start_urls = [f'http://www.madrid.org/wpad_pub/run/j/MostrarFichaCentro.icm?cdCentro={code}' for code in school_codes_lst[110:160]]

  def parse(self, response):
    info_list = response.css('.pSizeSB strong::text').getall()
    school = {
      'code': info_list[3],
      'name': response.css('.pSizeMB strong::text').get(),
      'denomination': info_list[0],
      'type': info_list[1],
      'titular': info_list[2],
      'territorial_zone': info_list[4],
      'address': info_list[5]
    }
    # compile patterns to check in results
    five_digits = re.compile(r'\d{5}')
    nine_digits = re.compile(r'\d{9}')
    parenthesis = re.compile(r'\(.*\)')
    www = re.compile(r'w{3}')
    e_mail = re.compile(r'\S+@\S+')
    # general information
    if re.search(five_digits, info_list[6]):
      info_list.insert(6, 's/n')
    school['street_number'] = info_list[6]
    school['postcode'] = info_list[7]
    school['city'] = info_list[8]

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
    if not 'telephone' in school.keys():
      school['telephone'] = None
    for i in range(10, len(info_list)):
      if re.search(www, info_list[i]) and not re.search(e_mail, info_list[i]):
        school['webpage'] = info_list[i].strip()
      else:
        school['webpage'] = None
    try:
      school['email'] = [mail for mail in [email.strip() for email in response.css('.pB strong::text').getall()] if re.search(e_mail, mail)] or None
    except TypeError:
      pass
    if not re.search(e_mail, response.css('.pB strong::text').get()) and len(response.css('.pB strong::text').get().strip()) > 1:
      school['segregation'] = response.css('.pB strong::text').get()
    # languages
    try:
      school['language_options'] = response.css('#capaOpcLingContent .pNegro::text').getall() or None
    except TypeError:
      pass
    # Services and additional information
    try:
      school['additional_info'] = response.css('#capaOtrosCritContent .pNegro::text').getall() or None
    except TypeError:
      pass
    # Institucional extracurricular activities
    try:
      school['extracurricular_official'] = [strg for strg in [string.strip() for string in response.css('#capaInstitContent td::text').getall()] if strg != ''] or None
    except TypeError:
      pass

    yield school