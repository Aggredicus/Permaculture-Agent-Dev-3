from pathlib import Path
import sys
import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from run_hager_park import osm_way_to_geojson, geographic_acres


def test_parse_valid_polygon():
    xml='''<osm version="0.6">
    <node id="1" lat="42.916" lon="-85.852"/>
    <node id="2" lat="42.916" lon="-85.848"/>
    <node id="3" lat="42.921" lon="-85.848"/>
    <node id="4" lat="42.921" lon="-85.852"/>
    <way id="158802227"><nd ref="1"/><nd ref="2"/><nd ref="3"/><nd ref="4"/><nd ref="1"/>
     <tag k="leisure" v="park"/><tag k="name" v="Hager Park"/></way>
    </osm>'''
    feature=osm_way_to_geojson(xml,158802227)
    assert feature['geometry']['type']=='Polygon'
    assert 40 < geographic_acres(feature['geometry']) < 50


def test_wrong_way_does_not_substitute():
    xml='''<osm version="0.6"><way id="158802227"><tag k="leisure" v="forest"/>
    <tag k="name" v="Unrelated"/></way></osm>'''
    with pytest.raises(ValueError): osm_way_to_geojson(xml,158802227)


def test_wrong_way_id_raises():
    with pytest.raises(ValueError): osm_way_to_geojson('<osm version="0.6"/>',158802227)