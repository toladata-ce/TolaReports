import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff
import os
import flask
from plotly import tools
app = dash.Dash(__name__)
server = app.server
app.title = 'Partner Progress Report'
df = pd.read_csv('data.csv')#reading file to get month names
a = ['January','February','March','April','May','June','July','August','September','October','November','December']
activity_arr = ['id mob', 'nursery management', 'demo', 'phh', 'marketing', 'crop management', 'seed distribution']# HARDCODING ACTIVITEES FOR NOW



app.layout = html.Div([
=======
df = pd.read_csv('data.csv')# loading csv here for month array
a = df['periodic_target'].unique()# month array
activity_arr = ['id mob', 'nursery management', 'demo', 'phh', 'marketing', 'crop management', 'seed distribution']# activity array


    html.H1('Partner Progress Report'),
    html.Div('Please select Year'),

    dcc.Dropdown(
        value='2017',
        options=[{'label': i, 'value': i} for i in ['2017', '2018']],
        multi=False,
        id='dropdown-year',
        placeholder="Select Year",
    ),
    html.Div('Please select Month'),
    dcc.Dropdown(
        value='July',
        options=[{'label': i, 'value': i} for i in list(a)],
        placeholder="Select Month",
        multi=False,
        id='dropdown-month',

    ),

    html.H2('Indicator actual results against target'),
    dcc.Graph(id = 'my-graph'),# bar graph
    html.H2('Indicator actual results by location, sex, age'),
    html.H3('Aggregated by indicators'),
    dcc.Graph(id = 'table-1-1'),
    html.H3('Disaggregated by indicators'),
    dcc.Graph(id = 'table-1-2'),
    html.Div('Please select Activity'),
    dcc.Dropdown(
        value='id mob',
        options=[{'label': i, 'value': i} for i in list(activity_arr)],
        multi=False,
        id='dropdown-activity',
        placeholder="Select Activity",
    ),

    html.H2('Overall beneficiary reached by location, sex and age'),
    html.H3('Aggregated reach data'),
    dcc.Graph(id='table-2-2'),  # Table 2
    html.H3('Disaggregated reach data'),
    dcc.Graph(id='table-2-1'),# table 1
    html.Div(id='intermediate-value', style={'display': 'none'}),
    html.Div(id='intermediate-value-1', style={'display': 'none'})




    ])
@app.callback(Output('intermediate-value', 'children'), [Input('dropdown-month', 'value'),Input('dropdown-year', 'value')])
def common_table(month, year):
    dcc.Graph(id = 'my-graph'),# Bar graph
    dcc.Graph(id = 'my-table'),# Table 1
    dcc.Graph(id = 'new-table')# Table 2

    ])

@app.callback(Output('my-graph', 'figure'), [Input('dropdown-month', 'value')])# Callback for bar graph
def update_graph(value):
    df = pd.read_csv('data.csv')
    y1 = []
    y2 = []
    indname = []
    for i in range(len(df)):
        if (df['periodic_target'].iloc[i] == value):
            indname.append(df['name'].iloc[i])
            y1.append(df['achieved'].iloc[i])
            y2.append(df['lop_target'].iloc[i])
    return {
        'data': [go.Bar(
            x = indname,
            y = y1,
            name = 'achieved',
            marker = go.Marker(
                color = 'rgb(55,83,109)'

            )

        ),
        go.Bar(
            x = indname,
            y = y2,
            name = 'target'
        )
        ]
    }

@app.callback(Output('my-table', 'figure'), [Input('dropdown-month', 'value')])# Callback for table 1 using only month
def update_table(value):
    df = pd.read_csv('data.csv')# Reading the csv again because using global objects can break dash app
    y1 = []
    y2 = []
    indname = []
    for i in range(len(df)):
        if (df['periodic_target'].iloc[i] == value):
            indname.append(df['name'].iloc[i])
            y1.append(df['achieved'].iloc[i])
            y2.append(df['lop_target'].iloc[i])

    dff = pd.DataFrame({'Indicator name': indname, 'achieved': y1, 'target': y2})
    df_fig = ff.create_table(dff)# Figure factory to create plotly graph
    return df_fig



# 3rd callback using 2nd and 3rd dropdown to create table - 3
@app.callback(Output('new-table', 'figure'), [Input('dropdown-year', 'value'),Input('dropdown-month', 'value'), Input('dropdown-activity', 'value')])
def update_new_tab(year, month, activity):
    year = int(year)
    df = pd.read_csv('new_report.csv')
    df = df.drop(df.columns[31], axis=1)
    df = df.drop(df.columns[31], axis=1)
    df = df.drop(df.columns[31], axis=1)
    month_arr = ['Month_ID_Mob', 'Month_N_Mgt', 'Month_Demo', 'Month_PHH',
                 'Month_Mrk_Sales', 'Month_C_Mgt', 'Month_Seed_Dist']
    year_arr = ['Year_ID_Mob', 'Year_N_Mgt', 'Year_Demo', 'Year_PHH',
                'Year_Mrk_Sales', 'Year_C_Mgt', 'Year_Seed_Dist']
    activity_arr = ['id mob', 'nursery management', 'demo', 'phh', 'marketing', 'crop management', 'seed distribution']
    count_arr = []
    df_arr = []
    index = 10
    year = int(year)
    val = month
    valy = year
    for i in range(len(month_arr)):
        index = index + 3  # because all activites are at a difference of 3 cols
        df_tmp = df[df[month_arr[i]] == val]  # filtering by month
        df_tmp = df_tmp[df_tmp[year_arr[i]] == valy]  # filtering by year
        # count_tmp = df_tmp.iloc[:, index].value_counts()#counting
        # count_arr.append(count_tmp)
        df_arr.append(df_tmp)
    df_final = pd.DataFrame()
    for i in range(len(activity_arr)):
        dfc = df_arr[i]
        dfc = dfc.groupby(['District', 'Gender', 'Age cohorts']).size()
        dfc = pd.DataFrame(dfc)
        dfc.insert(loc=0, column='Activity', value=activity_arr[i])
        df_final = df_final.append(dfc)

    df_final.to_csv('tmp.csv')  # saving the file as temporary one as the ff does not display the row names
    df_display = pd.read_csv('tmp.csv')
    return df_display.to_json(date_format='iso', orient='split')

@app.callback(Output('intermediate-value-1', 'children'),[Input('intermediate-value', 'children')])
def section_one_table(cleaned_data):
    df_display = pd.read_json(cleaned_data, orient='split')
    df_display = df_display[['Activity', 'Gender', 'Age cohorts', 'District', '0']]
    # df_display = df_display[df_display['Activity'] == activity]
    df_display['Sum'] = df_display['0']
    indilist = pd.read_csv('indicators.csv')
    indicator_map = ['nursery management', 'phh', 'marketing', 'crop management', 'seed distribution']
    df_tmp = df_display
    arr = []
    arr_i = []
    for i in range(len(df_display)):
        flag = 0
        tmp = df_display.iloc[i, 0]
        for j in range(len(indicator_map)):
            if (tmp == indicator_map[j]):
                arr.append(indilist.iloc[j, 0])
                flag = 1
        if (flag == 0):
            arr_i.append(i)
    df_tmp = df_tmp.drop(df_tmp.index[arr_i])
    df_tmp['Indicators'] = arr
    df_tmp = df_tmp[['Indicators', 'District', 'Gender', 'Age cohorts', 'Sum']]
    df_display = df_tmp
    indi_arr = df_display['Indicators'].unique()
    df_main = pd.DataFrame()
    for i in range(len(indi_arr)):
        df_tmp_2 = df_display[df_display['Indicators'] == indi_arr[i]]
        district_arr = df_tmp_2['District'].unique()
        gender_arr = df_tmp_2['Gender'].unique()
        age_arr = df_tmp_2['Age cohorts'].unique()
        sum_arr = []
        arr = []
        for i in range(len(district_arr)):
            tmp = df_tmp_2[df_tmp_2['District'] == district_arr[i]]
            sum_ = tmp['Sum'].sum()
            sum_arr.append(sum_)
            arr.append(district_arr[i])
        for i in range(len(gender_arr)):
            tmp = df_tmp_2[df_tmp_2['Gender'] == gender_arr[i]]
            sum_ = tmp['Sum'].sum()
            sum_arr.append(sum_)
            arr.append(gender_arr[i])
        for i in range(len(age_arr)):
            tmp = df_tmp_2[df_tmp_2['Age cohorts'] == age_arr[i]]
            sum_ = tmp['Sum'].sum()
            sum_arr.append(sum_)
            arr.append(age_arr[i])
        df_tmp = pd.DataFrame(sum_arr, index=arr)
        df_tmp = df_tmp.transpose()
        df_main = df_main.append(df_tmp)
    df_main['Indicator'] = indi_arr
    df_t = df_main
    cols = ['Indicator', 'Male', 'Female', 'Gulu', 'Omoro', 'Pader', '15-18', '19-24', '25+']
    df_t = df_t[cols]
    df_t.loc[:, 'Total Actual'] = df_t['Male']+df_t['Female']
    target_arr = []
    for i in range(len(df_t)):
        for j in range(len(indilist)):
            if (df_t.iloc[i, 0] == list(indilist['Indicators'])[j]):
                target_arr.append(list(indilist['LOP Target'])[j])
    df_t['Total Target'] = target_arr
    return df_t.to_json(date_format='iso', orient='split')



@app.callback(Output('my-graph', 'figure'), [Input('intermediate-value-1', 'children')])
def update_graph(cleaned_data):
    df_t = pd.read_json(cleaned_data, orient='split')
    y1 = list(df_t['Total Actual'])
    y2 = list(df_t['Total Target'])
    indname = list(df_t['Indicator'])
    return {
        'data': [go.Bar(
            x = indname,
            y = y1,
            name = 'achieved',
            marker = go.Marker(
                color = 'rgb(55,83,109)'

            )

        ),
        go.Bar(
            x = indname,
            y = y2,
            name = 'target'
        )
        ]
    }

@app.callback(Output('table-1-1', 'figure'), [Input('intermediate-value-1', 'children')])
def update_table(cleaned_data):
    df_t = pd.read_json(cleaned_data, orient='split')
    vals = []
    for i in range(len(list(df_t))):
        vals.append(df_t.iloc[:, i])
    return {
        'data': [
            go.Table(
                columnwidth=[150, 40, 40, 40, 40, 40, 40, 40,40],
                header=dict(values=list(df_t.columns),
                            font=dict(family='Roboto', size=16, color='#7f7f7f'),
                            fill=dict(color='C2D4FF')),
                cells=dict(
                    values=vals,
                    font=dict(family='Roboto', size=14, color='#7f7f7f'),
                    fill=dict(color='#F5F8FF'),
                    align=['left'] * 5)
            )
        ]
    }


@app.callback(Output('table-1-2', 'figure'), [Input('intermediate-value', 'children')])
def update_table(cleaned_data):
    df_display = pd.read_json(cleaned_data, orient='split')
    df_display = df_display[['Activity', 'Gender', 'Age cohorts', 'District', '0']]
    # df_display = df_display[df_display['Activity'] == activity]
    df_display['Sum'] = df_display['0']
    indilist = pd.read_csv('indicators.csv')
    indicator_map = ['nursery management', 'phh', 'marketing', 'crop management', 'seed distribution']
    df_tmp = df_display
    arr = []
    arr_i = []
    for i in range(len(df_display)):
        flag = 0
        tmp = df_display.iloc[i, 0]
        for j in range(len(indicator_map)):
            if (tmp == indicator_map[j]):
                arr.append(indilist.iloc[j, 0])
                flag = 1
        if (flag == 0):
            arr_i.append(i)
    df_tmp = df_tmp.drop(df_tmp.index[arr_i])
    df_tmp['Indicators'] = arr
    df_tmp = df_tmp[['Indicators', 'District', 'Gender', 'Age cohorts', 'Sum']]
    df_t = df_tmp
    df_t = df_t.rename(index=str, columns={"Age cohorts": "Age Category","Sum":"Total Actual"})
    cols = ['Indicators', 'District', 'Gender', 'Age Category', 'Total Actual']
    df_t = df_t[cols]
    # df_t['Target'] = target_arr
    table = ff.create_table(df_t, height_constant=60)
    vals = []
    for i in range(len(list(df_t))):
        vals.append(df_t.iloc[:, i])
    return {
        'data': [
            go.Table(
                columnwidth=[150, 40, 40, 40, 40],
                header=dict(values=list(df_t.columns),
                            font=dict(family='Roboto', size=16, color='#7f7f7f'),
                            fill=dict(color='C2D4FF')),
                cells=dict(
                    values=vals,
                    fill=dict(color='#F5F8FF'),
                    font=dict(family='Roboto', size=14, color='#7f7f7f'),
                    align=['left'] * 5)
            )
        ]
    }

# Table 3 uses 2 dropdowns so calling 2 inputs
@app.callback(Output('table-2-1', 'figure'), [Input('intermediate-value', 'children'), Input('dropdown-activity', 'value')])
def update_new_tab(cleaned_data, activity):
    df_display = pd.read_json(cleaned_data, orient='split')
    df_display = df_display[['Activity', 'Gender', 'Age cohorts','District', '0']]
    df_display = df_display[df_display['Activity'] == activity]
    df_display = df_display[['District','Gender', 'Age cohorts','0']]
    df_display['Sum'] = df_display['0']
    df_display = df_display[['District', 'Gender', 'Age cohorts', 'Sum']]
    df_display = df_display.rename(index=str, columns={"Age cohorts": "Age Category","Sum":"Total Actual"})
    vals = []
    for i in range(len(list(df_display))):
        vals.append(df_display.iloc[:, i])
    return {
        'data': [
            go.Table(
                header=dict(values=list(df_display.columns),
                            font=dict(family='Roboto', size=16, color='#7f7f7f'),
                            fill=dict(color='C2D4FF')),
                cells=dict(
                    values=vals,
                    fill=dict(color='#F5F8FF'),
                    font=dict(family='Roboto', size=14, color='#7f7f7f'),
                    align=['left'] * 5)
            )
        ]
    }
=======
    df_final.to_csv('tmp.csv')# saving file again because fig factory doesnot print row index by groupby
    df_display = pd.read_csv('tmp.csv')#loading it again
    df_display = df_display[['Activity', 'Gender', 'Age cohorts','District', '0']]# displaying only these 4 elements right now
    df_display = df_display[df_display['Activity'] == activity]
    df_display = df_display[['Gender', 'Age cohorts', 'District', '0']]
    tab = ff.create_table(df_display)
    return tab


@app.callback(Output('table-2-2', 'figure'),[Input('intermediate-value', 'children'), Input('dropdown-activity', 'value')])
def update_second_tab(cleaned_data, activity):
# saving the file as temporary one as the ff does not display the row names
    df_display = pd.read_json(cleaned_data, orient='split')
    df_display = df_display[['Activity', 'Gender', 'Age cohorts','District', '0']]
    df_display = df_display[df_display['Activity'] == activity]
    df_display = df_display[['District','Gender', 'Age cohorts','0']]
    df_display['Sum'] = df_display['0']
    df_display = df_display[['District', 'Gender', 'Age cohorts', 'Sum']]
    district_arr = df_display['District'].unique()
    gender_arr = df_display['Gender'].unique()
    age_arr = df_display['Age cohorts'].unique()
    sum_arr = []
    arr = []
    for i in range(len(district_arr)):
        tmp = df_display[df_display['District'] == district_arr[i]]
        sum_ = tmp['Sum'].sum()
        sum_arr.append(sum_)
        arr.append(district_arr[i])
    for i in range(len(gender_arr)):
        tmp = df_display[df_display['Gender'] == gender_arr[i]]
        sum_ = tmp['Sum'].sum()
        sum_arr.append(sum_)
        arr.append(gender_arr[i])
    for i in range(len(age_arr)):
        tmp = df_display[df_display['Age cohorts'] == age_arr[i]]
        sum_ = tmp['Sum'].sum()
        sum_arr.append(sum_)
        arr.append(age_arr[i])
    df_tmp = pd.DataFrame(sum_arr, index=arr)
    df_tmp = df_tmp.transpose()
    df2 = df_tmp
    if(len(df2)==0):
        return {
            'data':
                [go.Table(
                    header = dict(values = ['Message']),
                    cells = dict(values = [['No data']])
                )]
        }
    df2['Total Actual'] = df2['Male']+df2['Female']
    tab = ff.create_table(df2)
    vals = []
    for i in range(len(list(df2))):
        vals.append(df2.iloc[:, i])
    return {
        'data': [
            go.Table(
                header=dict(values=list(df2.columns),
                            font=dict(family='Roboto', size=16, color='#7f7f7f'),
                            fill=dict(color='C2D4FF')),
                cells=dict(
                    values=vals,
                    fill=dict(color='#F5F8FF'),
                    font=dict(family='Roboto', size=14, color='#7f7f7f'),
                    align=['left'] * 5)
            )
        ]
    }
if __name__ == '__main__':
    app.run_server(debug=True)