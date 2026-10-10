"""Numerical regression tests; no network required."""
import importlib.util
from pathlib import Path
import numpy as np

path=Path(__file__).resolve().parents[1]/'scripts'/'terrain_site_analysis.py'
spec=importlib.util.spec_from_file_location('terrain_site_analysis',path)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def test_planar_east_slope_facing_west():
    cols=np.arange(31)
    z=np.tile(100+0.1*cols,(31,1))
    r=m.compute_terrain(z,1.0,np.ones_like(z,dtype=bool),None)
    assert np.allclose(r['slope'],np.degrees(np.arctan(0.1)))
    assert np.allclose(r['aspect'],270)
    assert abs(r['net_m3']) < 1e-9


def test_north_rising_south_facing():
    row=np.arange(20)
    z=np.tile(200-0.5*row[:,None],(1,20))
    r=m.compute_terrain(z,1.0,np.ones_like(z,dtype=bool),None)
    assert np.allclose(r['aspect'],180)
    assert abs(r['south_facing_pct']-100.0) < 1e-9


def test_custom_target_cut_fill():
    z=np.full((9,9),10.,dtype=float)
    z[:,5:]=20.
    r=m.compute_terrain(z,2.0,np.ones_like(z,dtype=bool),15)
    assert abs(r['cut_m3']-(9*4*5*4))<1e-8
    assert abs(r['fill_m3']-(9*5*5*4))<1e-8


def test_flat_aspect_undefined():
    z=np.full((10,10),10.,dtype=float)
    r=m.compute_terrain(z,1,np.ones_like(z,dtype=bool),None)
    assert np.isnan(r['aspect']).all()
    assert r['south_facing_pct'] is None