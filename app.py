import streamlit as st
import pandas as pd
import plotly.express as px
from astroquery.jplhorizons import Horizons
from datetime import timedelta

st.set_page_config(page_title='Lunar Landing Site Navigator', layout='wide')
st.title('🌕 Lunar Landing Site Navigator')
st.caption('NASA Space Apps | Prototype • JPL Horizons • ideal geometric horizon only')
SITES = {'Site A — sample': (-89.0, 0.0), 'Site B — sample': (-89.5, 90.0), 'Site C — sample': (-88.5, 180.0)}

@st.cache_data(show_spinner=False, ttl=3600)
def get_data(lat, lon, start, stop):
    location = {'lon': lon, 'lat': lat, 'elevation': 0, 'body': 301}
    epochs = {'start': start, 'stop': stop, 'step': '2h'}
    output = {}
    for label, target in [('Sun', '10'), ('Earth', '399')]:
        eph = Horizons(id=target, location=location, epochs=epochs).ephemerides(quantities='4')
        df = pd.DataFrame({'time': pd.to_datetime([str(t) for t in eph['datetime_str']], format='%Y-%b-%d %H:%M', utc=True),
                           'elevation': [float(x) for x in eph['EL']],
                           'azimuth': [float(x) for x in eph['AZ']]})
        output[label] = df
    return output

st.warning('This prototype estimates visibility above a flat geometric horizon. Terrain, shadows, landing safety and radio link budgets are NOT modeled.')
date = st.date_input('Start date (UTC)')
days = st.slider('Days to analyze', 1, 5, 2)
selected = st.multiselect('Compare sample locations', list(SITES), default=list(SITES))
if st.button('Analyze using NASA JPL Horizons', type='primary'):
    if not selected:
        st.error('Select at least one site.')
    else:
        summary=[]
        for site in selected:
            lat, lon = SITES[site]
            try:
                with st.spinner(f'Retrieving ephemerides for {site}...'):
                    data=get_data(lat,lon,date.strftime('%Y-%m-%d'),(date+timedelta(days=days)).strftime('%Y-%m-%d'))
                sun_pct=100*(data['Sun']['elevation']>0).mean()
                earth_pct=100*(data['Earth']['elevation']>0).mean()
                summary.append({'Site':site,'Sun above horizon (%)':round(sun_pct,1),'Earth above horizon (%)':round(earth_pct,1),'Example weighted score':round(.6*sun_pct+.4*earth_pct,1)})
                with st.expander(f'{site}: elevation and azimuth',expanded=(len(selected)==1)):
                    combined=pd.concat([df.assign(Object=label) for label,df in data.items()])
                    fig=px.line(combined,x='time',y='elevation',color='Object',title='Geometric elevation (degrees)')
                    fig.add_hline(y=0,line_dash='dash')
                    st.plotly_chart(fig,use_container_width=True)
                    st.dataframe(combined[['time','Object','azimuth','elevation']],hide_index=True)
            except Exception as e:
                st.error(f'{site}: NASA query failed. Check connection, try another date, or inspect the Horizons response. Details: {e}')
        if summary:
            result=pd.DataFrame(summary).sort_values('Example weighted score',ascending=False)
            st.subheader('Site comparison')
            st.dataframe(result,hide_index=True,use_container_width=True)
            st.caption('Percentages count 2-hourly samples, not exact visibility durations. The 60/40 score is illustrative, not a NASA recommendation.')
st.markdown('Source: [NASA JPL Horizons](https://ssd.jpl.nasa.gov/horizons/) | [API documentation](https://ssd-api.jpl.nasa.gov/doc/horizons.html)')
