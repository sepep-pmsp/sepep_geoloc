from pyproj import CRS, Transformer
from typing import Tuple
import geopandas as gpd
from shapely.geometry import shape

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


def geojson_dict_to_geodf(geojson:dict, crs_data=True)->gpd.GeoDataFrame:

    geometries = [shape(feature['geometry']) for feature in geojson['features']]
    gdf = gpd.GeoDataFrame(geometry=geometries)
    #pressupoe que as properties sao as mesmas
    for key in geojson['features'][0]['properties']:
        gdf[key] = [feature['properties'][key] for feature in geojson['features']]

    if crs_data:
        gdf.crs = geojson['crs']['properties']['name']

    return gdf


def extract_points_from_feature(geojson_feature:dict)->Tuple[float, float]:
        
        geom = geojson_feature['geometry']
        geom_type = geom['type']
        if geom_type!='Point':
            raise ValueError(f'Geometria deve ser ponto. Geometria: {geom_type}')
        
        x, y = geom['coordinates']

        #nunca entendi o por que, mas precisa inverter
        return y, x
    
def convert_points_to_sirgas(geojson_feature:dict)->Tuple[float, float]:

    x, y = extract_points_from_feature(geojson_feature)
    x, y = point_from_wgs_to_sirgas(x, y)


    return x, y
