from pyproj import CRS, Transformer
from typing import Tuple

wgs_84_crs = CRS("WGS84")
sirgas_2000_crs = CRS('epsg:31983')

transf_wgs_to_sirgas=  Transformer.from_crs(wgs_84_crs, sirgas_2000_crs)
transf_sirgas_to_wgs=  Transformer.from_crs(wgs_84_crs, sirgas_2000_crs)


def point_from_wgs_to_sirgas(x:float, y:float)->Tuple[float, float]:

    x, y = transf_wgs_to_sirgas.transform(x, y)

    return x, y


def point_from_sirgas_to_wgs(x:float, y:float)->Tuple[float, float]:

    x, y = transf_sirgas_to_wgs.transform(x, y)

    return x, y