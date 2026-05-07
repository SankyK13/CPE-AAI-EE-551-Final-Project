"""
test_project.py
Pytest test cases for the transit delay analysis project.
Tests include average delay calculations and delay prediction logic.
Run with:  pytest test_project.py -v
By: Pal Sanjaybhai Anghan
"""

import pytest
import pandas as pd
from transit_data import TransitRoute, TransitNetwork
from data_loader import load_data, clean_data
from analytics import compute_statistics, compute_rms_delay, get_high_delays

#TransitRoute tests
def test_route_average_delay():
    #Average delay should match manual calculation
    route = TransitRoute("R1")
    route.add_record(4.0)
    route.add_record(6.0)
    route.add_record(10.0)
    assert route.average_delay == pytest.approx(20.0 / 3)

def test_route_empty():
    #Empty route should return 0 for avg and max
    route = TransitRoute("R_empty")
    assert route.average_delay == 0.0
    assert route.max_delay == 0.0
    assert len(route) == 0

def test_route_str():
    #__str__ should contain the route ID
    route = TransitRoute("Route_42")
    route.add_record(5.0)
    text = str(route)
    assert "Route_42" in text

def test_route_equality():
    #Two routes with the same ID should be equal
    a = TransitRoute("R1")
    b = TransitRoute("R1")
    c = TransitRoute("R2")
    assert a == b
    assert a != c

#TransitNetwork tests

def test_network_add_and_contains():
    net = TransitNetwork()
    net.add_record("R1", 5.0)
    assert "R1" in net
    assert "R99" not in net
    assert len(net) == 1

def test_network_generator():
    #Generator should yield all delay records
    net = TransitNetwork()
    net.add_record("R1", 3.0)
    net.add_record("R1", 7.0)
    net.add_record("R2", 5.0)

    all_delays = list(net.delay_generator())
    assert len(all_delays) == 3
    assert all_delays[0] == ("R1", 3.0)

def test_network_set_operations():
    #Common categories should be the intersection
    net = TransitNetwork()
    net.add_record("R1", 1.0)   # On Time
    net.add_record("R1", 7.0)   # Moderate
    net.add_record("R2", 7.0)   # Moderate
    net.add_record("R2", 15.0)  # Severe

    common = net.common_categories("R1", "R2")
    assert common == {"Moderate"}

#Analytics tests

def test_compute_statistics():
    delays = [2.0, 4.0, 6.0, 8.0, 10.0]
    mean, std, median = compute_statistics(delays)
    assert mean == pytest.approx(6.0)
    assert median == pytest.approx(6.0)
    assert std > 0

def test_rms_delay():
    delays = [3.0, 4.0]
    rms = compute_rms_delay(delays)
    # sqrt((9 + 16) / 2) = sqrt(12.5) ≈ 3.5355
    assert rms == pytest.approx(3.5355, abs=0.001)

def test_get_high_delays():
    delays = [1, 5, 10, 15, 20]
    result = get_high_delays(delays, 10)
    assert result == [15, 20]

#Data loader exception tests

def test_load_missing_file():
    #Should raise FileNotFoundError for a nonexistent file
    with pytest.raises(FileNotFoundError):
        load_data("this_file_does_not_exist.csv")

def test_load_missing_columns(tmp_path):
    #Should raise ValueError if required columns are missing
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("col_a,col_b\n1,2\n")
    with pytest.raises(ValueError):
        load_data(str(bad_csv))

#Data cleaning test

def test_clean_removes_negatives():
    #Negative delays should be dropped during cleaning
    df = pd.DataFrame({
        "trip_id": ["T1", "T2", "T3"],
        "route_id": ["R1", "R1", "R1"],
        "transport_type": ["Bus", "Bus", "Bus"],
        "actual_departure_delay_min": [5, -3, 10],
        "weather_condition": ["Clear", "Clear", "Rain"],
    })
    cleaned = clean_data(df)
    assert len(cleaned) == 2
    assert (cleaned["actual_departure_delay_min"] >= 0).all()
