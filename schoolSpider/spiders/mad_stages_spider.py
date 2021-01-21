import scrapy
import pandas as pd
import sys
sys.path.append('../../')
from school_codes import school_codes_lst

class MadSchoolStageSpider(scrapy.Spider):
  '''Collects educational offer information on nurseries, schools, high schools and 
  vocational colleges in Madrid'''
  global school_codes_lst
  name = 'mad_stages'
  start_urls = [f'http://www.madrid.org/wpad_pub/run/j/MostrarFichaCentro.icm?cdCentro={code}' for code in school_codes_lst[110:160]]

  def parse(self,response):
    school = {
      'code': response.css('.pSizeSB strong::text').getall()[3]
    }
    #funding_type = response.css('.pSizeSB strong::text').getall()[1]
    try:
      table = pd.read_html(response.css('#capaEtapasContent').get())
      clean_table = table[0].dropna(how='all').drop([3,5], axis=1).drop(1).fillna(value='')
      stage_list = clean_table.values.tolist()
      for stage in stage_list:
        school[stage[0]] = {'titularidad':stage[1] or None, 'tipo':stage[2] or None, 'plazas_libres':stage[3] or None}
    except TypeError:
      school['stages'] = None
    try:
      school['authorized_study_plans'] = response.css('#capaPlanesEstudioContent .pSizeS::text').getall() or None
    except TypeError:
      pass

    
    yield school