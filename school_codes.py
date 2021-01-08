import numpy as np
import pandas as pd

school_data = pd.read_csv('csv_colegio_madrid.csv', sep=';', header=1, index_col=False, encoding='CP850')

school_data = school_data.convert_dtypes()

school_codes_np = school_data['CODIGO CENTRO'].array

school_codes_lst = list(school_codes_np)

base_url = 'http://www.madrid.org/wpad_pub/run/j/BusquedaSencilla.icm?accion_paginacion=2&dscCentrosComp=&cdCentro=&tipoCurso=ADM&recargaDatos=&formularioConsulta=busquedaSencilla&siPrivadoComp=&basica.strCodNomMuni=&codCentrosComp=&navegador=Netscape&esPaginacion=S#'