def chartsapp():
    import streamlit as st
    import sys
    from babel.numbers import format_currency
    import os
    import plotly.express as px
    from statewise import  statewiseapp
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

    # Create tab to show the two different types of records
    tab1, tab2 = st.tabs(["# All India Insights", "# State-Wise Insights"])
    with tab1:
        chart_options =['Transaction Analysis','Device and User Engagement Analysis','Insurance Analysis']
        select_chart = st.selectbox('Chart Type',chart_options)
        if select_chart =="Transaction Analysis":
            st.markdown(f"### {select_chart}")
            col1,col2 = st.columns((0.5,0.5),gap="medium")
            with col1:
                agg_trans_growth = utils.fetchfrommysql("select agg_year as Year,sum(amount) as Transaction_amount from aggregated_transaction where state='' group by agg_year")
                agg_trans_growth['Transaction_amount'] = agg_trans_growth['Transaction_amount'].apply(format_amount)
                fig = px.line(agg_trans_growth,x='Year',y='Transaction_amount',labels={'Year': 'Year', 'Transaction_amount': 'Transaction Amount'},
                        title="Transaction Amounts Over Years")

                st.plotly_chart(fig,use_container_width=True)

                agg_trans_growth = utils.fetchfrommysql(
                    "select agg_year as Year,sum(count) as Transaction_count from aggregated_transaction where state='' group by agg_year")
                agg_trans_growth['Transaction_count'] = agg_trans_growth['Transaction_count'].apply(format_indian_number)
                fig = px.line(agg_trans_growth, x='Year', y='Transaction_count',
                              labels={'Year': 'Year', 'Transaction_count': 'Transaction Count'},
                              title="Transaction Counts Over Years")

                st.plotly_chart(fig, use_container_width=True)


            with col2:
                agg_trans_growth_quarter = utils.fetchfrommysql(
                    """select agg_year as Year,sum(case when quarter=1 then amount else 0 end) as Q1, 
        sum(case when quarter=2 then amount else 0 end) as Q2,
        sum(case when quarter=3 then amount else 0 end) as Q3,
        sum(case when quarter=4 then amount else 0 end) as Q4
        from aggregated_transaction where state=''
        group by agg_year;""")
                agg_trans_growth_quarter['Q1'] = agg_trans_growth_quarter['Q1'].apply(format_amount)
                agg_trans_growth_quarter['Q2'] = agg_trans_growth_quarter['Q2'].apply(format_amount)
                agg_trans_growth_quarter['Q3'] = agg_trans_growth_quarter['Q3'].apply(format_amount)
                agg_trans_growth_quarter['Q4'] = agg_trans_growth_quarter['Q4'].apply(format_amount)
                fig = px.line(
                    agg_trans_growth_quarter,
                    x='Year',
                    y=['Q1', 'Q2', 'Q3', 'Q4'],  # List of columns for multiple lines
                    labels={'value': 'Transaction Amount', 'variable': 'Quarter'},
                    title="Quarterly Transaction Amount Over Years"
                )
                st.plotly_chart(fig, use_container_width=True)

                agg_trans_growth_quarter = utils.fetchfrommysql(
                    """select agg_year as Year,sum(case when quarter=1 then count else 0 end) as Q1, 
        sum(case when quarter=2 then count else 0 end) as Q2,
        sum(case when quarter=3 then count else 0 end) as Q3,
        sum(case when quarter=4 then count else 0 end) as Q4
        from aggregated_transaction where state=''
        group by agg_year;""")
                agg_trans_growth_quarter['Q1'] = agg_trans_growth_quarter['Q1'].apply(format_indian_number)
                agg_trans_growth_quarter['Q2'] = agg_trans_growth_quarter['Q2'].apply(format_indian_number)
                agg_trans_growth_quarter['Q3'] = agg_trans_growth_quarter['Q3'].apply(format_indian_number)
                agg_trans_growth_quarter['Q4'] = agg_trans_growth_quarter['Q4'].apply(format_indian_number)
                fig = px.line(
                    agg_trans_growth_quarter,
                    x='Year',
                    y=['Q1', 'Q2', 'Q3', 'Q4'],  # List of columns for multiple lines
                    labels={'value': 'Transaction Count', 'variable': 'Quarter'},
                    title="Quarterly Transaction Counts Over Years"
                )
                st.plotly_chart(fig, use_container_width=True)

            category_trans_amount = utils.fetchfrommysql("""select name as Category_name,agg_year as Year,sum(amount) as Transaction_amount from aggregated_transaction where state=''
                        group by name,agg_year""")
            fig = px.bar(
                category_trans_amount,
                x="Category_name",
                y="Transaction_amount",
                color="Year",
                barmode="group",
                title="Transactions Grouped by category"
            )

            fig.update_layout(
                xaxis_title="Category",
                yaxis_title="Amount",
                title_font_size=20
            )
            st.plotly_chart(fig, use_container_width=True)

            col1,col2,col3,col4 = st.columns((0.25,0.25,0.25,0.25))
            with col1:
                category_trans_amount = utils.fetchfrommysql("""select name as Category,sum(count) as Transaction_count from aggregated_transaction where state='' and quarter=1
                            group by name;""")
                fig = px.pie(
                    category_trans_amount,
                    names='Category',
                    values='Transaction_count',
                    labels={'Transaction_count': 'Count'},
                    title='Q1 Transaction Count'
                )

                st.plotly_chart(fig,use_container_width=True)
            with col2:
                category_trans_amount = utils.fetchfrommysql("""select name as Category,sum(count) as Transaction_count from aggregated_transaction where state='' and quarter=2
                            group by name;""")
                fig = px.pie(
                    category_trans_amount,
                    names='Category',
                    values='Transaction_count',
                    labels={'Transaction_count': 'Count'},
                    title='Q2 Transaction Count'
                )

                st.plotly_chart(fig,use_container_width=True)
            with col3:
                category_trans_amount = utils.fetchfrommysql("""select name as Category,sum(count) as Transaction_count from aggregated_transaction where state='' and quarter=3
                            group by name;""")
                fig = px.pie(
                    category_trans_amount,
                    names='Category',
                    values='Transaction_count',
                    labels={'Transaction_count': 'Count'},
                    title='Q3 Transaction Count'
                )

                st.plotly_chart(fig,use_container_width=True)
            with col4:
                category_trans_amount = utils.fetchfrommysql("""select name as Category,sum(count) as Transaction_count from aggregated_transaction where state='' and quarter=4
                            group by name;""")
                fig = px.pie(
                    category_trans_amount,
                    names='Category',
                    values='Transaction_count',
                    labels={'Transaction_count': 'Count'},
                    title='Q4 Transaction Count'
                )

                st.plotly_chart(fig,use_container_width=True)

            agg_trans_state = utils.fetchfrommysql("""select state as State,sum(count) as Transaction_count from aggregated_transaction where state!=''
                            group by state;
            """)
            fig = px.bar(
                agg_trans_state,
                x='State',
                y='Transaction_count',
                color='State',
                labels={'Transaction_count': 'Count'},
                title='Transaction Count Grouped by State'
            )

            st.plotly_chart(fig, use_container_width=True)
        if select_chart=='Device and User Engagement Analysis':
            agg_state_user = utils.fetchfrommysql("select state as State,brand as Brand, sum(count) as Count from aggregated_user where state!='' group by state,brand;")
            fig = px.bar(agg_state_user, x='Brand', y='Count', color='State',
                         title='Total Registered Users all over India',
                         labels={'Count': 'Registered Users', 'State': 'State'},
                         color_discrete_sequence=px.colors.qualitative.Pastel2_r, height=500)

            fig.update_layout(barmode='stack', legend_title="State", xaxis_title="State", yaxis_title="Registered Users")

            fig.update_traces(showlegend=True, selector=dict(type='bar'))


            st.plotly_chart(fig, use_container_width=True)
            col1,col2 = st.columns((0.5,0.5),gap='small')
            with col1:
                agg_state_user = utils.fetchfrommysql(
                    "select brand as Brand, sum(count) as Count from aggregated_user where state!='' group by state,brand;")
                fig = px.bar(agg_state_user, x='Brand', y='Count', color='Brand',
                             title='Brand wise Registered Users',
                             color_discrete_sequence=px.colors.qualitative.Pastel2_r, height=500)

                fig.update_layout(barmode='stack', legend_title="State", xaxis_title="State",
                                  yaxis_title="Registered Users")

                fig.update_traces(showlegend=True, selector=dict(type='bar'))

                st.plotly_chart(fig, use_container_width=True)
            with col2:
                agg_user = utils.fetchfrommysql("select sum(reg_users) as Registered_Users,sum(app_opens) as App_opens,agg_year as Year from aggregated_user where state='' group by agg_year")
                fig = px.line(
                        agg_user,
                        x='Year',
                        y=['Registered_Users', 'App_opens'],  # List of columns for multiple lines
                        title="Yearly App registered & Opens"
                    )
                st.plotly_chart(fig, use_container_width=True)

            agg_user_quarter = utils.fetchfrommysql("SELECT  agg_year as Year, quarter as Quarter, SUM(reg_users) AS Registered_Users,sum(app_opens) as App_opens FROM map_user where district='' GROUP BY agg_year,quarter;")
            total = agg_user_quarter[['Registered_Users', 'App_opens']].sum()
            agg_user_quarter['Registered_Users_percent'] = agg_user_quarter['Registered_Users'] / total['Registered_Users'] * 100
            agg_user_quarter['App_opens_percent'] = agg_user_quarter['App_opens'] / total['App_opens'] * 100
            fig = px.area(
                agg_user_quarter,
                x='Quarter',
                y=['Registered_Users_percent', 'App_opens_percent'],
                color='Year',
                title="Reg Users & App Opens Each Quarter wise",
                labels={'Quarter': 'Quarter',
                'Registered_Users_percent': 'Registered Users (%)',
                'App_opens_percent': 'App Opens (%)'}
            )
            fig.update_layout(margin=dict(t=50, b=50, l=50, r=50))
            fig.update_traces(line_shape='spline', opacity=0.7)
            fig.update_xaxes(tickmode='array', tickvals=[1, 2, 3, 4])
            st.plotly_chart(fig, use_container_width=True)
        if select_chart=="Insurance Analysis":
            st.markdown(f"### {select_chart}")
            col1, col2 = st.columns((0.5, 0.5), gap="medium")
            with col1:
                agg_ins_growth = utils.fetchfrommysql("select agg_year as Year,sum(amount) Transaction_amount from aggregated_insurance where state='' group by agg_year;")
                agg_ins_growth['Transaction_amount'] = agg_ins_growth['Transaction_amount'].apply(format_amount)
                fig = px.line(agg_ins_growth, x='Year', y='Transaction_amount',
                              labels={'Year': 'Year', 'Transaction_amount': 'Transaction Amount'},
                              title="Insurance Amounts Over Years")
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                agg_ins_growth = utils.fetchfrommysql("select agg_year as Year,sum(count) Transaction_count from aggregated_insurance where state='' group by agg_year;")
                agg_ins_growth['Transaction_count'] = agg_ins_growth['Transaction_count'].apply(format_indian_number)
                fig = px.line(agg_ins_growth, x='Year', y='Transaction_count',
                              labels={'Year': 'Year', 'Transaction_count': 'Transaction Count'},
                              title="Insurance Counts Over Years")
                st.plotly_chart(fig, use_container_width=True)
            st.markdown("***")
            agg_ins_quarter =utils.fetchfrommysql("""select concat(agg_year,'-',concat('Q',quarter)) as Year,sum(amount) Transaction_amount from aggregated_insurance where state='' group by concat(agg_year,'-',concat('Q',quarter))
order by concat(agg_year,'-',concat('Q',quarter));""")
            #agg_ins_quarter['Transaction_amount'] = agg_ins_quarter['Transaction_amount'].apply(format_amount)
            fig = px.line(agg_ins_quarter, x='Year', y='Transaction_amount',
                          labels={'Year': 'Year', 'Transaction_amount': 'Transaction Amount'},
                          title="Each Quarter wise changes")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("***")
            agg_ins_state = utils.fetchfrommysql("select state as State,sum(count) Transaction_count from map_insurance where district='' group by state;")
            fig = px.bar(agg_ins_state,x="State",y="Transaction_count",
                         color="State",
                         labels={'Year': 'Year', 'Transaction_count': 'Transaction Count'},
                         title="State wise Insurance Count",
                         color_discrete_sequence=px.colors.qualitative.Pastel2_r, height=500)
            fig.update_layout(barmode='stack')
            fig.update_traces(showlegend=True, selector=dict(type='bar'))
            st.plotly_chart(fig,use_container_width=True)
    with tab2:
        statewiseapp()