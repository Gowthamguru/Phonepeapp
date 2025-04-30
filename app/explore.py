def exploreapp():
    #Import important libraries
    import streamlit as st
    from streamlit_option_menu import option_menu
    import sys
    import pandas as pd
    from babel.numbers import format_currency
    import os
    import json
    import plotly.express as px

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    import utils

    # Format number
    def format_indian_number(number):
            num_str = str(int(number))[::-1]
            formatted_str = ""
            for i in range(len(num_str)):
                if i != 0 and (i == 3 or (i > 3 and (i - 1) % 2 == 0)):
                    formatted_str += ','
                formatted_str += num_str[i]
            return formatted_str[::-1]

    # Format amount
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

    # read the geographical json file from folder
    with open('json/states_india.geojson') as f:
        india_states_geojson = json.load(f)

    # Define the choropleth map function
    def user_choropleth(input_df):
        fig = px.choropleth(
            input_df,
            geojson=india_states_geojson,
            featureidkey='properties.st_nm',
            locations='State',
            projection="mercator",
            hover_data=['Year', 'Registered_Users'],
            color='Registered_Users',
            color_discrete_sequence=px.colors.sequential.Viridis,
            range_color=(input_df['Registered_Users'].min(), input_df['Registered_Users'].max())
        )

        fig.update_geos(fitbounds="locations", visible=False)

        fig.update_layout(
            width=600,
            height=400,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            geo=dict(bgcolor='rgba(0,0,0,0)')

        )
        return fig
    # Define the choropleth map function
    def make_choropleth(input_df):
        fig = px.choropleth(
            input_df,
            geojson=india_states_geojson,
            featureidkey='properties.st_nm',
            locations='State',
            projection="mercator",
            hover_data=['Year', 'Transaction_Amount', 'Category_Name'],
            color='Transaction_Count',
            color_discrete_sequence=px.colors.sequential.Viridis,
            range_color=(input_df['Transaction_Count'].min(), input_df['Transaction_Count'].max())
        )

        fig.update_geos(fitbounds="locations", visible=False)

        fig.update_layout(
            width=600,
            height=400,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            geo=dict(bgcolor='rgba(0,0,0,0)')
        )

        return fig

    # Top menu Definition
    topmenu = option_menu(None, ["Transaction", "Insurance", "User"],
                        icons=['alt', "list-task", 'cast'],
                         key='topmenu', orientation="horizontal",
    styles={
        "container": {"padding": "2!important", "background-color": "#230B43"},
        "icon": {"color": "orange", "font-size": "18px"},
        "nav-link": {"color": "white","font-size": "18px", "text-align": "left", "margin":"0px", "--hover-color": "#391C59"},
        "nav-link-selected": {"background-color": "#230B43"},
    })
    st.markdown(f"<h3 style='text-align: center; font-size: 40px'> All India {topmenu} Data<h3>", unsafe_allow_html=True)

    # Top menu select event activity
    if topmenu=="Transaction":
        # Convert sql query and load the data in dataframe
        df_agg_trans = utils.fetchfrommysql(
            'select name,count,amount,agg_year,state,quarter from aggregated_transaction')
        df_map_trans = utils.fetchfrommysql(
            "select agg_year,quarter,state,district,count,amount from map_map where district!=''")
        df_top_trans = utils.fetchfrommysql(
            'select agg_year,quarter,state,district,pincode,count,amount from top_map where pincode is not null')

        #Split the page into 4 columns
        col1, col2, col3, col4 = st.columns((2, 2, 2, 3), gap="large")
        with col1:
            years = st.selectbox("#### Select Year", options=df_agg_trans["agg_year"].unique())
        with col2:
            quarters = st.selectbox("#### Select Quarter", options=df_agg_trans["quarter"].unique())
        with col3:
            trans_type = st.selectbox("#### Select Transaction",options=df_agg_trans["name"].unique())

        # Filter functionality
        trans_selected_year = df_agg_trans[(df_agg_trans['agg_year'] == years) & (df_agg_trans['quarter'] == quarters) ]
        map_selected_year = df_map_trans[(df_map_trans['agg_year'] == years) & (df_map_trans['quarter'] == quarters) ]
        top_selected_year = df_top_trans[(df_top_trans['agg_year'] == years) & (df_top_trans['quarter'] == quarters) ]

        if trans_selected_year.empty:
            st.error("#### No data available for the selected year and quarter.")

        else:
            # Group the values
            trans_selected_year_grouped = trans_selected_year.groupby('state').sum().reset_index().sort_values(
                by="amount", ascending=False)
            total_transactions = trans_selected_year['count'].sum()
            total_payment_value = trans_selected_year['amount'].sum()

            avg_transaction_value = total_payment_value / total_transactions
            total_transactions = format_indian_number(total_transactions)
            col_map, col_data = st.columns((0.6, 0.4), gap='small')

            # Map function
            with col_map:
                df_agg_trans['state'] = df_agg_trans['state'].str.title()
                df_agg_trans['state'] = df_agg_trans['state'].str.replace('-', ' ', regex=False)
                df_agg_trans = df_agg_trans[df_agg_trans['state'].notna() & (df_agg_trans['state'] != '')]

                trans_selected_year_geo = df_agg_trans[(df_agg_trans['agg_year'] == years) &
                                                    (df_agg_trans['quarter'] == quarters) & (df_agg_trans['name'] ==trans_type) ]

                trans_selected_year_geo['amount'] = trans_selected_year_geo[
                    'amount'].apply(format_amount)
                trans_selected_year_geo = trans_selected_year_geo.rename(columns={
                    'name': 'Category_Name',
                    'amount': 'Transaction_Amount',
                    'count': 'Transaction_Count',
                    'state' : 'State',
                    'agg_year':'Year'
                })
                choropleth_map = make_choropleth(trans_selected_year_geo)
                st.plotly_chart(choropleth_map, use_container_width=True)

                states_button_clicked = False
                districts_button_clicked = False
                postal_codes_button_clicked = False
                c11, c12, c13 = st.columns((1, 1, 1), gap="small")
                with c11:
                    if st.button("# States"):
                        states_button_clicked = True
                with c12:
                    if st.button("# Districts"):
                        districts_button_clicked = True
                with c13:
                    if st.button("# Postal Codes"):
                        postal_codes_button_clicked = True

                if states_button_clicked:
                    st.markdown("<h1 style='font-size: 30px'> Top 10 States", unsafe_allow_html=True)
                    trans_selected_year_grouped = trans_selected_year_grouped[
                        trans_selected_year_grouped['state'].notna()
                        & (trans_selected_year_grouped['state'] != '')]
                    trans_selected_year_grouped['amount'] = trans_selected_year_grouped[
                        'amount'].apply(format_amount)
                    trans_selected_year_grouped['Serial'] = range(1, len(trans_selected_year_grouped) + 1)
                    trans_selected_year_grouped = trans_selected_year_grouped.head(10)
                    df = pd.DataFrame(trans_selected_year_grouped[['Serial', 'state', 'amount']])
                    df['state'] = df['state'].str.title()
                    df['state'] = df['state'].str.replace('-', ' ', regex=False)

                    df = df.rename(columns={
                        'amount': 'Transaction_Amount',
                        'state': 'State',
                    })
                    df.set_index('Serial', inplace=True)
                    df.columns = ['State', 'Transaction_Amount']
                    st.table(df)
                if districts_button_clicked:
                    st.markdown("<h1 style='font-size: 30px'> Top 10 Districts", unsafe_allow_html=True)
                    trans_selected_year_grouped_dist =  map_selected_year.groupby(
                        'district').sum().reset_index().sort_values(by="amount", ascending=False)
                    trans_selected_year_grouped_dist['Serial'] = range(1, len(trans_selected_year_grouped_dist) + 1)
                    trans_selected_year_grouped_dist = trans_selected_year_grouped_dist.head(10)
                    trans_selected_year_grouped_dist['amount'] = trans_selected_year_grouped_dist[
                        'amount'].apply(format_amount)
                    df = pd.DataFrame(
                        trans_selected_year_grouped_dist[['Serial','state', 'district', 'amount']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['State','Districts', 'Transaction Amount']
                    st.table(df)
                if postal_codes_button_clicked:
                        st.markdown("<h1 style='font-size: 30px'>Top 10 Postal Codes", unsafe_allow_html=True)
                        trans_selected_year_grouped_pin = top_selected_year.groupby(
                            'pincode').sum().reset_index().sort_values(by="amount",
                                                                                      ascending=False)
                        trans_selected_year_grouped_pin['Serial'] = range(1, len(trans_selected_year_grouped_pin) + 1)
                        trans_selected_year_grouped_pin = trans_selected_year_grouped_pin.head(10)
                        trans_selected_year_grouped_pin['pincode'] = trans_selected_year_grouped_pin[
                            'pincode'].apply(lambda x: '{:.0f}'.format(x))
                        trans_selected_year_grouped_pin['amount'] = trans_selected_year_grouped_pin[
                            'amount'].apply(format_amount)
                        df = pd.DataFrame(
                            trans_selected_year_grouped_pin[['Serial','state', 'pincode', 'amount']])
                        df.set_index('Serial', inplace=True)
                        df.columns = ['State','Postal Codes', 'Transaction Amount']
                        st.table(df)

        # Line break
        st.markdown("***")

        with col_data:
                st.write(f'#### All PhonePe transactions(Q{quarters}) {years}')
                st.write(f'##### {total_transactions}')
                st.write(f'#### Total Payment Value (Q{quarters}) {years}')
                st.write(f'##### {format_amount(total_payment_value)}')
                st.write(f'#### Average Payment Value (Q{quarters}) {years}')
                st.write(f"##### ₹{avg_transaction_value:,.0f}")
                trans_selected_year_grp = trans_selected_year.groupby(
                    'name').sum().reset_index().sort_values(by="amount", ascending=False)
                trans_selected_year_grp['Serial'] = range(1, len(trans_selected_year_grp) + 1)
                df = pd.DataFrame(trans_selected_year_grp[['Serial', 'name', 'amount']])
                df['amountnew'] = df['amount']
                df['amount'] = df['amount'].apply(format_amount)
                st.markdown("***")
                st.markdown("<h1 style=' font-size: 30px'>Categories</h1>", unsafe_allow_html=True)

                col1, col2 = st.columns(2)

                for index, row in df.iterrows():
                    with col1:
                        st.markdown(f"<p style='font-size:14px;text-align: left;font-weight:bold'>{row['name']}</p>",
                                    unsafe_allow_html=True)
                    with col2:
                        st.markdown(
                            f"<p style='font-size:14px;text-align: right; color:#05C2DD;font-weight:bold'>{row['amount']}</p>",
                            unsafe_allow_html=True)

                st.markdown("***")

                fig = px.pie(trans_selected_year_grp, values='count', names='name',
                             title='Transaction Count Details',
                             color_discrete_sequence=px.colors.sequential.RdBu)

                # Make it a donut chart
                fig.update_traces(hole=0.4, textinfo='percent')

                fig.update_layout(title_font_size=20, height=600, width=600)
                st.plotly_chart(fig, use_container_width=True)

    if topmenu=="Insurance":
        df_agg_ins = utils.fetchfrommysql('select name,count,amount,agg_year as year,state,quarter from aggregated_insurance')
        df_map_ins = utils.fetchfrommysql("select agg_year as year,quarter,state,district,count,amount from map_insurance where district!='' ")
        df_top_ins = utils.fetchfrommysql('select agg_year as year,quarter,state,district,pincode,count,amount from top_insurance where pincode is not null')
        col1, col2,col3,col4,col5,col6 = st.columns((1.5, 1.5,0.5,0.5,1,1), gap="large")
        with col1:
            years = st.selectbox("#### Select Year", options=df_agg_ins["year"].unique())
        with col2:
            quarters = st.selectbox("#### Select Quarter", options=df_agg_ins["quarter"].unique())
        ins_selected_year = df_agg_ins[(df_agg_ins['year'] == years) &
                                        (df_agg_ins['quarter'] == quarters)]
        ins_selected_year_dist = df_map_ins[(df_map_ins['year'] == years) &
                                        (df_map_ins['quarter'] == quarters)]
        ins_selected_year_pin = df_top_ins[(df_top_ins['year'] == years) &
                                        (df_top_ins['quarter'] == quarters)]

        if ins_selected_year.empty:
            st.error("#### No data available for the selected year and quarter.")

        else:
            ins_selected_year_grouped = ins_selected_year.groupby('state').sum().reset_index().sort_values(
                by="amount", ascending=False)
            ins_selected_year_grouped = ins_selected_year_grouped[
                ins_selected_year_grouped['state'].notna()
                & (ins_selected_year_grouped['state'] != '')]
            ins_selected_year_grouped['Serial'] = range(1, len(ins_selected_year_grouped) + 1)
            ins_selected_year_grouped = ins_selected_year_grouped.head(10)

            total_transactions = ins_selected_year['count'].sum()
            total_payment_value = ins_selected_year['amount'].sum()
            avg_transaction_value = total_payment_value / total_transactions
            total_transactions = format_indian_number(total_transactions)
            col_map, col_data = st.columns((0.7, 0.3), gap='small')
            with col_map:
                ins_selected_year = ins_selected_year.rename(columns={
                    'name': 'Category_Name',
                    'amount': 'Transaction_Amount',
                    'count': 'Transaction_Count',
                    'state' : 'State',
                    'year':'Year'
                })
                ins_selected_year['Transaction_Amount'] = ins_selected_year[
                    'Transaction_Amount'].apply(format_amount)
                ins_selected_year['State'] = ins_selected_year['State'].str.title()
                ins_selected_year['State'] = ins_selected_year['State'].str.replace('-', ' ', regex=False)
                ins_selected_year = ins_selected_year[ins_selected_year['State'].notna() & (ins_selected_year['State'] != '')]

                choropleth_map = make_choropleth(ins_selected_year)
                st.plotly_chart(choropleth_map, use_container_width=True)
                st.markdown('***')
                states_button_clicked = False
                districts_button_clicked = False
                postal_codes_button_clicked = False
                c11, c12, c13 = st.columns((1, 1, 1.5), gap="small")
                with c11:
                    if st.button("# States"):
                        states_button_clicked = True

                with c12:
                    if st.button("# Districts"):
                        districts_button_clicked = True

                with c13:
                    if st.button("# Postal Codes"):
                        postal_codes_button_clicked = True

                if states_button_clicked:
                    st.markdown("<h1 style='font-size: 30px'> Top 10 States", unsafe_allow_html=True)
                    ins_selected_year_grouped['amount'] = ins_selected_year_grouped[
                        'amount'].apply(format_amount)
                    df = pd.DataFrame(ins_selected_year_grouped[['Serial', 'state', 'amount']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['State', 'Premium Amount']
                    st.table(df)

                if districts_button_clicked:
                    st.markdown("<h1 style='font-size: 30px'> Top 10 Districts", unsafe_allow_html=True)
                    ins_selected_year_grouped_dist = ins_selected_year_dist.groupby(
                        'district').sum().reset_index().sort_values(by="amount", ascending=False)
                    ins_selected_year_grouped_dist['Serial'] = range(1, len(ins_selected_year_grouped_dist) + 1)
                    ins_selected_year_grouped_dist = ins_selected_year_grouped_dist.head(10)
                    ins_selected_year_grouped_dist['amount'] = ins_selected_year_grouped_dist[
                        'amount'].apply(format_amount)
                    df = pd.DataFrame(ins_selected_year_grouped_dist[['Serial', 'state','district', 'amount']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['State','Districts', 'Premium Amount']
                    st.table(df)

                if postal_codes_button_clicked:
                    st.markdown("<h1 style='font-size: 30px'>Top 10 Postal Codes", unsafe_allow_html=True)
                    ins_selected_year_grouped_pin = ins_selected_year_pin.groupby(
                        'pincode').sum().reset_index().sort_values(by="amount",
                                                                                  ascending=False)
                    ins_selected_year_grouped_pin['Serial'] = range(1, len(ins_selected_year_grouped_pin) + 1)
                    ins_selected_year_grouped_pin = ins_selected_year_grouped_pin.head(10)
                    ins_selected_year_grouped_pin['pincode'] = ins_selected_year_grouped_pin[
                        'pincode'].apply(lambda x: '{:.0f}'.format(x))
                    ins_selected_year_grouped_pin['amount'] = ins_selected_year_grouped_pin[
                        'amount'].apply(format_amount)
                    df = pd.DataFrame(
                        ins_selected_year_grouped_pin[['Serial', 'state','pincode', 'amount']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['State','Postal Codes', 'Premium Amount']
                    st.table(df)

            with col_data:
                st.write(f'#### All India Insurance Policies Purchased (Nos.) ****(Q{quarters}) {years}****')
                st.write(f'##### {total_transactions}')
                st.write(f'#### Total Premium Value (Q{quarters}) {years}')
                st.write(f'##### {format_amount(total_payment_value)}')
                st.write(f'#### Average Premium Value (Q{quarters}) {years}')
                st.write(f"₹{avg_transaction_value:,.0f}")
                st.markdown('***')

    if topmenu == "User":
        df_agg_user = utils.fetchfrommysql('select reg_users,app_opens,brand,count,percentage,agg_year as year,state,quarter from aggregated_user')
        df_map_user = utils.fetchfrommysql("select reg_users,app_opens,agg_year as year,state,district,quarter  from map_user where district!=''")
        df_top_user = utils.fetchfrommysql('select reg_users,agg_year as year,state,district,pincode,quarter  from top_user where pincode is not null')
        col1, col2, co3, col4, col5, col6 = st.columns((1.5, 1.5, 0.5, 0.5, 1, 1), gap="large")
        with col1:
            years = st.selectbox("#### Select Year", options=df_map_user["year"].unique())
        with col2:
            quarters = st.selectbox("#### Select Quarter", options=df_map_user["quarter"].unique())

        user_selected_year = df_agg_user[(df_agg_user['year'] == years) &
                                      (df_agg_user['quarter'] == quarters)]
        user_selected_year_dist = df_map_user[(df_map_user['year'] == years) &
                                           (df_map_user['quarter'] == quarters)]
        user_selected_year_pin = df_top_user[(df_top_user['year'] == years) &
                                          (df_top_user['quarter'] == quarters)]

        if user_selected_year_dist.empty:
            st.error("#### No data available for the selected year and quarter.")

        else:
            user_selected_year_grouped = user_selected_year_dist.groupby('state').sum().reset_index().sort_values(
                by="reg_users", ascending=False)
            user_selected_year_group = user_selected_year.groupby('state').sum().reset_index().sort_values(by="count",
                                                                                                           ascending=False)
            user_selected_year_grouped['Serial'] = range(1, len(user_selected_year_grouped) + 1)
            user_selected_year_grouped1 = user_selected_year_grouped.head(10)

            total_user = user_selected_year_group['count'].sum()
            total_app_opens = user_selected_year_grouped['app_opens'].sum()
            total_user = format_indian_number(total_user)
            total_app_opens = format_indian_number(total_app_opens)

            col_map, col_data = st.columns((0.7, 0.3), gap='small')

            with col_map:
                user_selected_year_grouped = user_selected_year_grouped.rename(columns={
                    'reg_users': 'Registered_Users',
                    'app_opens': 'App_opens',
                    'count': 'Transaction_Count',
                    'percentage':'Percentage',
                    'state': 'State',
                    'year': 'Year'
                })
                user_selected_year_grouped['State'] = user_selected_year_grouped['State'].str.title()
                user_selected_year_grouped['State'] = user_selected_year_grouped['State'].str.replace('-', ' ', regex=False)
                user_selected_year_grouped = user_selected_year_grouped[
                    user_selected_year_grouped['State'].notna() & (user_selected_year_grouped['State'] != '')]

                choropleth_map = user_choropleth(user_selected_year_grouped)
                st.plotly_chart(choropleth_map, use_container_width=True)
                st.markdown('***')

                states_button_clicked = False
                districts_button_clicked = False
                postal_codes_button_clicked = False
                c11, c12, c13 = st.columns((1, 1, 1.5), gap="small")
                with c11:
                    if st.button("# States"):
                        states_button_clicked = True

                with c12:
                    if st.button("# Districts"):
                        districts_button_clicked = True

                with c13:
                    if st.button("# Postal Codes"):
                        postal_codes_button_clicked = True

                if states_button_clicked:
                    st.markdown("<h1 style='font-size: 30px'> Top 10 States", unsafe_allow_html=True)
                    user_selected_year_grouped1['reg_users'] = user_selected_year_grouped1[
                        'reg_users'].apply(format_indian_number)
                    df = pd.DataFrame(user_selected_year_grouped1[['Serial', 'state', 'reg_users']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['State', 'Registered User']
                    st.table(df)

                if districts_button_clicked:
                    st.markdown("<h1 style='font-size: 30px'> Top 10 Districts", unsafe_allow_html=True)
                    user_selected_year_grouped_dist = user_selected_year_dist.groupby(
                        'district').sum().reset_index().sort_values(by="reg_users", ascending=False)
                    user_selected_year_grouped_dist['Serial'] = range(1, len(user_selected_year_grouped_dist) + 1)
                    user_selected_year_grouped_dist = user_selected_year_grouped_dist.head(10)
                    user_selected_year_grouped_dist['reg_users'] = user_selected_year_grouped_dist[
                        'reg_users'].apply(format_indian_number)
                    df = pd.DataFrame(user_selected_year_grouped_dist[['Serial', 'state','district', 'reg_users']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['State','Districts', 'Registered User']
                    st.table(df)

                if postal_codes_button_clicked:
                    st.markdown("<h1 style='font-size: 30px'>Top 10 Postal Codes", unsafe_allow_html=True)
                    user_selected_year_grouped_pin = user_selected_year_pin.groupby(
                        'pincode').sum().reset_index().sort_values(by="reg_users",
                                                                                  ascending=False)
                    user_selected_year_grouped_pin['Serial'] = range(1, len(user_selected_year_grouped_pin) + 1)
                    user_selected_year_grouped_pin = user_selected_year_grouped_pin.head(10)
                    user_selected_year_grouped_pin['reg_users'] = user_selected_year_grouped_pin[
                        'reg_users'].apply(format_indian_number)
                    user_selected_year_grouped_pin['pincode'] = user_selected_year_grouped_pin[
                        'pincode'].apply(lambda x: '{:.0f}'.format(x))
                    df = pd.DataFrame(
                        user_selected_year_grouped_pin[['Serial','state', 'pincode', 'reg_users']])
                    df.set_index('Serial', inplace=True)
                    df.columns = ['State','Postal Codes', 'Registered User']
                    st.table(df)

            with col_data:
                st.write(f'#### Registered PhonePe users (Q{quarters}) {years}')
                st.write(f'##### {total_user}')
                st.write(f'#### PhonePe app opens in (Q{quarters}) {years}')
                st.write(f'##### {total_app_opens}')
                st.markdown('***')
                st.markdown("<h1 style='font-size: 30px'>Top 10 Brand Wise ", unsafe_allow_html=True)

                user_selected_year = user_selected_year.groupby('brand').sum().reset_index().sort_values(by="count",
                                                                                                         ascending=False)
                user_selected_year['Serial'] = range(1, len(user_selected_year) + 1)
                user_selected_year = user_selected_year.head(10)
                user_selected_year['count'] = user_selected_year['count'].apply(format_indian_number)
                df = pd.DataFrame(user_selected_year[['Serial', 'brand', 'count']])
                df.set_index('Serial', inplace=True)
                df.columns = ['Mobile Brands', 'User Count']
                st.table(df)
