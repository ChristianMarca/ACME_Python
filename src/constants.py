CONSTRAINS = {
    "WEEKDAY": ["MO", "TU", "WE", "TH", "FR"],
    "WEEKEND": ["SA", "SU"],
    "TIME_WEEKDAY": [
        {
            "start": ["00", "01"],
            "end": ["09", "00"],
            "USD": 25
        },
        {
            "start": ["09", "01"],
            "end": ["18", "00"],
            "USD": 15
        },
        {
            "start": ["18", "01"],
            "end": ["00", "00"],
            "USD": 20
        }
    ],
    "TIME_WEEKEND": [
        {
            "start": ["00", "01"],
            "end": ["09", "00"],
            "USD": 30
        },
        {
            "start": ["09", "01"],
            "end": ["18", "00"],
            "USD": 20
        },
        {
            "start": ["18", "01"],
            "end": ["00", "00"],
            "USD": 25
        }
    ]
}