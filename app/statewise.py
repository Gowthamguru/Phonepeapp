def statewiseapp():
    import streamlit as st
    import sys
    import json
    from babel.numbers import format_currency
    import os
    import plotly.express as px
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    import utils

    def state_map(input_df,states):
        formatted_state_name = states.replace('-', '').lower()
        if formatted_state_name == "andaman&nicobarislands":
            formatted_state_name = 'andamanandnicobarislands'
        if formatted_state_name == "dadra&nagarhaveli&daman&diu":
            formatted_state_name = 'dadranagarhaveli'
        if formatted_state_name == "jammu&kashmir":
            formatted_state_name = 'jammuandkashmir'
        geojson_file_path = f'json/state-geojson-master/{formatted_state_name}.json'
        with open(geojson_file_path) as f:
            state_geojson = json.load(f)

        fig = px.choropleth(
            input_df,
            geojson=state_geojson,
            featureidkey='properties.district',
            locations='district',
            projection="mercator",
            color='Transaction_amount',
            hover_data=['Transaction_count','Transaction_amount'],
            color_discrete_sequence=px.colors.sequential.Viridis,
            range_color=(input_df['Transaction_amount'].min(), input_df['Transaction_amount'].max())
        )

        fig.update_geos(fitbounds="locations", visible=False)

        fig.update_layout(
            width=600,
            height=400,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            geo=dict(bgcolor='rgba(0,0,0,0)')
        )
        return fig
    def state_map_user(input_df,states):
        formatted_state_name = states.replace('-', '').lower()
        if formatted_state_name == "andaman&nicobarislands":
            formatted_state_name = 'andamanandnicobarislands'
        if formatted_state_name == "dadra&nagarhaveli&daman&diu":
            formatted_state_name = 'dadranagarhaveli'
        if formatted_state_name == "jammu&kashmir":
            formatted_state_name = 'jammuandkashmir'
        geojson_file_path = f'json/state-geojson-master/{formatted_state_name}.json'
        with open(geojson_file_path) as f:
            state_geojson = json.load(f)
        fig = px.choropleth(
            input_df,
            geojson=state_geojson,
            featureidkey='properties.district',
            locations='district',
            projection="mercator",
            color='reg_users',
            hover_data=['reg_users','app_opens'],
            color_discrete_sequence=px.colors.sequential.Viridis,
            range_color=(input_df['reg_users'].min(), input_df['reg_users'].max())
        )

        fig.update_geos(fitbounds="locations", visible=False)

        fig.update_layout(
            width=600,
            height=400,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            geo=dict(bgcolor='rgba(0,0,0,0)')
        )
        return fig
    def format_indian_number(number):
            num_str = str(int(number))[::-1]
            formatted_str = ""
            for i in range(len(num_str)):
                if i != 0 and (i == 3 or (i > 3 and (i - 1) % 2 == 0)):
                    formatted_str += ','
                formatted_str += num_str[i]
            return formatted_str[::-1]


    def format_amount(amount):
        if amount >= 1e7:
            amount_in_crore = amount / 1e7
            formatted_amount = format_currency(amount_in_crore, 'INR', locale='en_IN')
            return f"{formatted_amount} Cr"
        elif amount >= 1e5:
            amount_in_lakhs = amount / 1e5
            formatted_amount = format_currency(amount_in_lakhs, 'INR', locale='en_IN')
            return f"{formatted_amount} L"
        elif amount >= 1e3:
            amount_in_thousand = amount / 1e3
            formatted_amount = format_currency(amount_in_thousand, 'INR', locale='en_IN')
            return f"{formatted_amount} K"
        else:
            formatted_amount = format_currency(amount, 'INR', locale='en_IN')
            return format_indian_number(formatted_amount)


    chart_options = ['Transaction Analysis','Device and User Engagement Analysis','Insurance Analysis']
    stateinfo = utils.fetchfrommysql("select distinct state as State from map_user where district!=''")
    col1, col2 = st.columns((0.7, 0.3))
    with col1:
        select_chart = st.selectbox('ChartType', chart_options)
    with col2:
        state = st.selectbox('State', stateinfo['State'])
    st.markdown(f"### {select_chart} - {state}")
    if select_chart=='Transaction Analysis':
        col1, col2 = st.columns((0.5, 0.5), gap="medium")
        with col1:
            map_trans_growth = utils.fetchfrommysql(f"""select agg_year as Year,sum(amount) as Transaction_amount from map_map 
        where district!='' and state='{state}' group by agg_year""")
            map_trans_growth['Transaction_amount'] = map_trans_growth['Transaction_amount'].apply(format_amount)
            fig = px.line(map_trans_growth, x='Year', y='Transaction_amount',
                          labels={'Year': 'Year', 'Transaction_amount': 'Transaction Amount'},
                          title=f"Transaction Amount of {state} Over Years")

            st.plotly_chart(fig, use_container_width=True)
        with col2:
            map_trans_growth = utils.fetchfrommysql(f"""select agg_year as Year,sum(count) as Transaction_count from map_map 
                    where district!='' and state='{state}' group by agg_year""")
            map_trans_growth['Transaction_count'] = map_trans_growth['Transaction_count'].apply(format_amount)
            fig = px.line(map_trans_growth, x='Year', y='Transaction_count',
                          labels={'Year': 'Year', 'Transaction_count': 'Transaction Count'},
                          title=f"Transaction Count of {state} Over Years")

            st.plotly_chart(fig, use_container_width=True)
        st.markdown("***")
        st.markdown(f"#### {state} Transaction Details")
        map_trans_growth_map = utils.fetchfrommysql(
            f"select  replace(replace(district,'district',''),' ','') as district,sum(count) as Transaction_count,sum(amount) as Transaction_amount from map_map where district!='' and state='{state}' group by district;")
        map_trans_growth_map['district'] = map_trans_growth_map['district'].str.title()
        map_trans_growth_map['district'] = map_trans_growth_map['district'].str.replace('-', ' ', regex=False)
        map_trans_growth_map['Transaction_amount'] = map_trans_growth_map['Transaction_amount'].apply(format_amount)
        map_trans_growth_map['Transaction_count'] = map_trans_growth_map['Transaction_count'].apply(format_indian_number)
        choropleth_map = state_map(map_trans_growth_map, state)
        st.plotly_chart(choropleth_map, use_container_width=True)
        st.markdown("***")
        col1, col2 = st.columns((0.5, 0.5), gap='small')
        with col1:
            top_pincode = utils.fetchfrommysql(f"""select agg_year as Year,quarter as Quarter, pincode as Pincode,amount as Amount 
        from top_map where pincode is not null and state='{state}'
        order by amount desc limit 10;""")
            top_pincode['Amount'] = top_pincode['Amount'].apply(format_amount)
            top_pincode['Serial'] = range(1, len(top_pincode) + 1)
            top_pincode.set_index('Serial', inplace=True)
            top_pincode.columns = ['Year', 'Quarter', 'Postal Codes', 'Transaction Amount']
            st.markdown(f"#### Top 10 postal code wise transactions in {state}")
            st.write(top_pincode)
        with col2:
            top_district = utils.fetchfrommysql(f"""select agg_year as Year,quarter as Quarter, district as District,amount as Amount 
        from top_map where pincode is null and district!='' and state='{state}'
        order by amount desc limit 10;""")
            top_district['Amount'] = top_district['Amount'].apply(format_amount)
            top_district['Serial'] = range(1, len(top_district) + 1)
            top_district.set_index('Serial', inplace=True)
            top_district.columns = ['Year', 'Quarter', 'District', 'Transaction Amount']
            st.markdown(f"#### Top 10 District wise transactions in {state}")
            st.write(top_district)
    if select_chart=='Device and User Engagement Analysis':
        agg_district_user = utils.fetchfrommysql(
           f"select district as District, sum(reg_users) as Count from map_user where district!='' and state='{state}' group by district;")
        fig = px.bar(agg_district_user, x='District', y='Count', color='District',
                     title=f'Total Registered Users in {state}',
                     labels={'Count': 'Registered Users', 'District': 'District'},
                     color_discrete_sequence=px.colors.qualitative.Pastel2_r, height=500)

        fig.update_layout(barmode='stack', legend_title="District", xaxis_title="District", yaxis_title="Registered Users")

        fig.update_traces(showlegend=True, selector=dict(type='bar'))

        st.plotly_chart(fig, use_container_width=True)
        st.markdown("***")
        agg_district_user = utils.fetchfrommysql(
                f"select district as District, sum(app_opens) as Count from map_user where district!='' and state='{state}' group by district;")
        fig = px.bar(agg_district_user, x='District', y='Count', color='District',
                         title=f'District wise App Opens in {state}',
                         color_discrete_sequence=px.colors.qualitative.Pastel2_r, height=500)

        fig.update_layout(barmode='stack', legend_title="District", xaxis_title="District",
                              yaxis_title="App Opens")

        fig.update_traces(showlegend=True, selector=dict(type='bar'))

        st.plotly_chart(fig, use_container_width=True)
        st.markdown("***")
        agg_user = utils.fetchfrommysql(
                f"select sum(reg_users) as Registered_Users,sum(app_opens) as App_opens,agg_year as Year from map_user where district!='' and state='{state}' group by agg_year")
        fig = px.line(
                agg_user,
                x='Year',
                y=['Registered_Users', 'App_opens'],  # List of columns for multiple lines
                title=f"Yearly App registered & Opens in {state}"
            )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("***")
        reg_user_year = utils.fetchfrommysql(
            f"select agg_year as Year,sum(reg_users) as Registered_Users,sum(app_opens) as App_Opens from map_user where district!='' and state='{state}' group by agg_year;")
        total_reg_user = reg_user_year["Registered_Users"].sum()
        total_app_opens = reg_user_year["App_Opens"].sum()
        col1, col2 = st.columns((0.6, 0.4), gap='small')
        with col1:
            st.write(f'#### Total Registered Users in {state}')
            st.markdown(f'##### {format_indian_number(total_reg_user)}')
        with col2:
            st.write(f'#### Total App Opens in {state}')
            st.write(f'##### {format_indian_number(total_app_opens)}')

        col1,col2 = st.columns((0.7,0.3),gap='small')
        with col1:
            map_user = utils.fetchfrommysql(f"select  replace(replace(district,'district',''),' ','') as district,sum(reg_users) as reg_users,sum(app_opens) as app_opens from map_user where district!='' and state='{state}' group by district;")
            map_user['district'] = map_user['district'].str.title()
            map_user['district'] = map_user['district'].str.replace('-', ' ', regex=False)
            map_user['reg_users'] = map_user['reg_users'].apply(format_amount)
            map_user['app_opens'] = map_user['app_opens'].apply(
                format_indian_number)
            choropleth_map = state_map_user(map_user, state)
            st.plotly_chart(choropleth_map, use_container_width=True)
        with col2:
            reg_user_year['Serial'] = range(1, len(reg_user_year) + 1)
            reg_user_year.set_index('Serial', inplace=True)
            reg_user_year.columns = ['Year', 'Registered_Users', 'App_Opens']
            st.markdown(f"#### Year wise registered Users & App Opens in {state}")
            st.write(reg_user_year)
            st.markdown("***")
        col1,col2 = st.columns((0.5,0.5),gap='small')
        with col1:
            top_reg_user =utils.fetchfrommysql(f"""select agg_year as Year,district District,sum(reg_users) Registered_Users from top_user where state='{state}' and pincode is null and district!=''
group by agg_year,district order by sum(reg_users) desc;""")
            top_reg_user['Serial'] = range(1, len(top_reg_user) + 1)
            top_reg_user.set_index('Serial', inplace=True)
            top_reg_user.columns = ['Year',  'District', 'Registered Users']
            st.markdown(f"#### Top 10 District wise registered Users in {state}")
            st.write(top_reg_user)
        with col2:
            top_reg_user = utils.fetchfrommysql(
                    f"""select agg_year as Year,pincode,sum(reg_users) reg_user from top_user where state='{state}' and pincode is not null 
group by agg_year,pincode order by sum(reg_users) desc;""")
            top_reg_user['Serial'] = range(1, len(top_reg_user) + 1)
            top_reg_user.set_index('Serial', inplace=True)
            top_reg_user.columns = ['Year', 'Postal Codes', 'Registered Users']
            st.markdown(f"#### Top 10 Postal code wise registered Users in {state}")
            st.write(top_reg_user)
    if select_chart=='Insurance Analysis':
        st.markdown(f"### {select_chart}")
        col1, col2 = st.columns((0.5, 0.5), gap="medium")
        with col1:
            agg_ins_growth = utils.fetchfrommysql(
                f"select agg_year as Year,sum(amount) Transaction_amount from map_insurance where state!='' and district!='' and state='{state}' group by agg_year;")
            agg_ins_growth['Transaction_amount'] = agg_ins_growth['Transaction_amount'].apply(format_amount)
            fig = px.line(agg_ins_growth, x='Year', y='Transaction_amount',
                          labels={'Year': 'Year', 'Transaction_amount': 'Transaction Amount'},
                          title=f"Insurance Premium Over Years in {state}")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            agg_ins_growth = utils.fetchfrommysql(
                f"select agg_year as Year,sum(count) Transaction_count from map_insurance where state!='' and district!='' and state='{state}' group by agg_year;")
            agg_ins_growth['Transaction_count'] = agg_ins_growth['Transaction_count'].apply(format_indian_number)
            fig = px.line(agg_ins_growth, x='Year', y='Transaction_count',
                          labels={'Year': 'Year', 'Transaction_count': 'Transaction Count'},
                          title=f"Insurance Counts Over Years in {state}")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("***")
        agg_ins_quarter = utils.fetchfrommysql(f"""select concat(agg_year,'-',concat('Q',quarter)) as Year,sum(amount) Transaction_amount from map_insurance where state!='' and district!='' and state='{state}' 
group by concat(agg_year,'-',concat('Q',quarter))
order by concat(agg_year,'-',concat('Q',quarter));""")
        fig = px.line(agg_ins_quarter, x='Year', y='Transaction_amount',
                      labels={'Year': 'Year', 'Transaction_amount': 'Transaction Amount'},
                      title=f"Each Quarter wise changes in {state}")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("***")
        agg_ins_state = utils.fetchfrommysql(f"""
            select replace(replace(district,'district',''),' ','') as district,
            sum(count) as Transaction_count,sum(amount) as Transaction_amount,sum(count) as Transaction_count1,sum(amount) as Transaction_amount1 from map_insurance 
            where district!='' and state='{state}' group by district;""")
        col1,col2 = st.columns((0.6,0.4),gap="small")
        with col1:
            agg_ins_state['district'] = agg_ins_state['district'].str.title()
            agg_ins_state['district'] = agg_ins_state['district'].str.replace('-', ' ', regex=False)
            agg_ins_state['Transaction_amount'] = agg_ins_state['Transaction_amount'].apply(format_amount)
            agg_ins_state['Transaction_count'] = agg_ins_state['Transaction_count'].apply(
                format_indian_number)
            choropleth_map = state_map(agg_ins_state, state)
            st.plotly_chart(choropleth_map, use_container_width=True)
            st.markdown("***")
        with col2:
            agg_ins_year = utils.fetchfrommysql(f"""select agg_year as Year,
            sum(amount) as Transaction_amount,sum(count) as Transaction_count from map_insurance
            where district!='' and state='{state}' group by agg_year;""")
            st.markdown(f"#### Year wise Premium Amount & count in {state}")
            agg_ins_year['Transaction_amount'] = agg_ins_year['Transaction_amount'].apply(format_amount)
            agg_ins_year['Transaction_count'] = agg_ins_year['Transaction_count'].apply(
                format_indian_number)
            agg_ins_year['Serial'] = range(1, len(agg_ins_year) + 1)
            agg_ins_year.set_index('Serial', inplace=True)
            agg_ins_year.columns = ['Year','Transaction Amount','Transaction Count']
            st.write(agg_ins_year)
            st.markdown("***")
        total = agg_ins_state[['Transaction_count1', 'Transaction_amount1']].sum()
        agg_ins_state['Transaction_count_percent'] =agg_ins_state['Transaction_count1']/total['Transaction_count1']*100
        agg_ins_state['Transaction_amount_percent'] =agg_ins_state['Transaction_amount1']/total['Transaction_amount1']*100
        df_melt = agg_ins_state.melt(id_vars='district', value_vars=['Transaction_count_percent', 'Transaction_amount_percent'],
                          var_name='Type', value_name='Count')
        fig = px.bar(df_melt,
                     x="district",
                     y="Count",
                     color="Type",
                     barmode="group",
                     labels={'Year': 'Year', 'Transaction_count_percent': 'Transaction Count','Transaction_amount_percent':'Transaction Amount'},
                     title=f"{state} district wise Insurance Count & Amount percentage",
                     color_discrete_map={
                         'Transaction_count_percent': 'skyblue',
                         'Transaction_amount_percent': 'lightgreen'
                     }, height=500)
        fig.update_layout(barmode='group')
        fig.update_traces(showlegend=True, selector=dict(type='bar'))
        st.plotly_chart(fig, use_container_width=True)
        col1, col2 = st.columns((0.5, 0.5), gap='small')
        with col1:
            top_ins_district = utils.fetchfrommysql(
                f"""select agg_year as Year,district as District,sum(amount) Transaction_Amount from top_insurance where state='{state}' and pincode is null and district!=''
        group by agg_year,district order by sum(amount) desc;""")
            top_ins_district['Transaction_Amount'] = top_ins_district['Transaction_Amount'].apply(format_amount)
            top_ins_district['Serial'] = range(1, len(top_ins_district) + 1)
            top_ins_district.set_index('Serial', inplace=True)
            top_ins_district.columns = ['Year', 'District', 'TransactionAmount']
            st.markdown(f"#### Top 10 District Insurance premium in {state}")
            st.write(top_ins_district)
        with col2:
            top_ins_pin = utils.fetchfrommysql(
                f"""select agg_year as Year,pincode,sum(amount) Transaction_Amount from top_insurance where state='{state}' and pincode is not null 
        group by agg_year,pincode order by sum(amount) desc;""")
            top_ins_pin['Transaction_Amount'] = top_ins_pin['Transaction_Amount'].apply(format_amount)
            top_ins_pin['Serial'] = range(1, len(top_ins_pin) + 1)
            top_ins_pin.set_index('Serial', inplace=True)
            top_ins_pin.columns = ['Year', 'Postal Codes', 'Transaction Amount']
            st.markdown(f"#### Top 10 Postal code wise Insurance premium in {state}")
            st.write(top_ins_pin)