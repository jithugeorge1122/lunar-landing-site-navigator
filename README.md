# Lunar Landing Site Navigator

NASA Space Apps Challenge rapid prototype. Uses NASA JPL Horizons ephemerides to compare apparent Sun and Earth elevation and azimuth for three **sample** lunar south-pole coordinates.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Select a UTC start date, duration and sample locations; click **Analyze using NASA JPL Horizons**. Internet access is required for NASA queries.

## Scientific limitations

- Site coordinates are demonstration points, **not vetted landing sites**.
- The horizon is idealized at 0° elevation; crater rims and local terrain are ignored.
- Visibility percentages are fractions of 2-hour samples, not exact continuous windows.
- Earth above the horizon is a necessary but not sufficient condition for a reliable radio link.
- Weighted score is an illustrative 60% sunlight / 40% Earth visibility metric, not a NASA metric or landing safety assessment.
- No solar panel, terrain, radiation, slope or landing hazard model is included.

## Data and credits

- NASA JPL Horizons: https://ssd.jpl.nasa.gov/horizons/
- Horizons API: https://ssd-api.jpl.nasa.gov/doc/horizons.html
- Python: https://www.python.org/
- Astroquery: https://astroquery.readthedocs.io/
- Streamlit: https://streamlit.io/
- Plotly: https://plotly.com/python/

## AI disclosure

ChatGPT assisted with prototype code, project architecture and documentation. Team members should review and test the code and verify any NASA outputs before presenting them as validated results.
