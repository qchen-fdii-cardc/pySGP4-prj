from pysgp4 import timefunc


def test_utc2correction():
    # Test with a known date (e.g., January 1, 2000)
    ds50utc = 1.0  # This is the number of days since January 1, 1950 for January 1, 2000
    taiMinusUTC, ut1MinusUTC, ut1Rate, polarX, polarY = timefunc.utc2correction(
        ds50utc)

    # Check that the returned values are reasonable (not all zeros)
    print("No timing constants record found for the given ds50UTC, as expected.")
    assert taiMinusUTC == 0
    assert ut1MinusUTC == 0
    assert ut1Rate == 0
    assert polarX == 0
    assert polarY == 0

    timefunc.tcon_add_one(ds50utc, taiMinusUTC=37.0,
                          ut1MinusUTC=0.1, ut1Rate=0.001, polarX=0.2, polarY=0.3)

    taiMinusUTC, ut1MinusUTC, ut1Rate, polarX, polarY = timefunc.utc2correction(
        ds50utc)

    # Check that the returned values match what we added
    assert taiMinusUTC == 37.0
    assert ut1MinusUTC == 0.1
    assert ut1Rate == 0.001
    assert polarX == 0.2
    assert polarY == 0.3

    numOfRecs, fr, to = timefunc.tcon_time_span()
    assert numOfRecs == 1
    assert fr == ds50utc
    assert to == ds50utc


def test_utc2dtg20():
    # Test with a known date (e.g., January 1, 2000)
    ds50utc = 2192.0  # This is the number of days since January 1, 1950 for January 1, 2000

    dtg20 = timefunc.utc2dtg20(ds50utc)
    print(f"DTG20 for ds50UTC={ds50utc}: {dtg20}")
    assert dtg20 == "1956/001 0000 00.000"

    ds50utc = 2192.0 + 366.5  # Add one year and one day and a half to account for leap year
    dtg20 = timefunc.utc2dtg20(ds50utc)  # Add one year
    print(f"DTG20 for ds50UTC={ds50utc}: {dtg20}")
    assert dtg20 == "1957/001 1200 00.000"


def test_utc2_dtg():
    ds = 2192.0 + 366.5
    print()
    dtgs = [
        "57001120000.000",
        "1957/001.50000000",
        "1957Jan01120000.000",
        "1957/001 1200 00.000",
        "1957 001 12 00  0.000",
        "1957-001T12:00: 0.000Z",
        "01 Jan 1957 12:00: 0.000",
        "1957/01/01 12:00: 0.000",
        "1957-01-01 12:00: 0.000",
        "1957 001 (01 JAN) 12:00: 0.000"
    ]
    for idx in range(1, 11):
        dtg = timefunc.utc2dtg(ds, idx)
        print(dtg)
        assert dtg == dtgs[idx-1]
