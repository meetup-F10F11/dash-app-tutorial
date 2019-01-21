# plotly를 감싸주는 웹어플리케이션 패키지
import dash

# 콜백함수에서 다량의 인풋을 받아 아웃풋을 출력해줄 수 있게 해주는 패키지
from dash.dependencies import Input, Output

# Dash에 들어가는 여러가지 기능을 구현할 수 있는 패키지
import dash_core_components as dcc

# Dash에서 HTML 스타일로 개발을 할 수 있게 해주는 패키지
import dash_html_components as html

# Dash에서 데이터 자체를 테이블로 보여줄 수 있는 패키지
import dash_table

# Plotly의 그래프를 객채화 해주는 패키지
import plotly.graph_objs as go

import numpy as np
import pandas as pd
import datetime


app = dash.Dash()
server = app.server


df = pd.read_csv('data/bikesharing.csv')
df = df.reset_index(drop=False)

# season preprocessing
df_season = df.groupby(['season']).sum()

# date preprocessing
df['dayofweek'] = df['datetime'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').weekday())
df_dayofweek = df.groupby(['dayofweek']).sum()



app.title = 'Meetup-F10F11'


app.layout = html.Div(
    html.Div([

        # 우측 상단에 버튼 만들기
        html.Div(
            html.A([
                html.Img(
                    src = 'https://upload.wikimedia.org/wikipedia/commons/7/7c/Kaggle_logo.png',
                    style = {
                        'width' : '8%', # 너비 기준으로 조절하는 것을 추천
                        'float' : 'right', # 위치
                        'position' : 'relative', # 다른 요소의 위치 따라 상대적으로 배치
                        'padding-top' : 1, #윗 경계면으로부터 간격
                        'padding-right' : 15, #우측 경계면으로부터 간격
                    },
                )
            ], href='https://www.kaggle.com/c/bike-sharing-demand') #링크
        ),

        # Title
        html.Div(
            html.H1('Kaggle Bike Sharing Demand Visualization')
        ),


        # 드랍다운 기능 삽입
        html.Div(
            dcc.Dropdown(
                options=[
                    {'label' : 'Bar plots', 'value':1},
                    {'label' : 'Heatmap', 'value':2},
                    {'label' : 'Table', 'value':3},
                ],
                id = 'dropdown',
                placeholder = '시각화 타입을 선택하세요'
                # value=4, #로드 시 가장 먼저 보여주고 싶은 특정 탭이 있다면 해당 번호 고정,

            ),
            style = {
                'width' : '40%'
            }
        ),

        # 각 드랍다운에 해당하는 시각화를 보여주기 위한 공간 할당
        html.Div(
            html.Div(
                id = 'dropdown-output'
            )
        )
    ]
    )
)


# # 콜백함수 suppression
# app.config['suppress_callback_exceptions'] = True

# 콜백함수의 Input, Output 명시
@app.callback(
    Output('dropdown-output', 'children'),
    [Input('dropdown', 'value')],
)


def display_content(value):
    

    if value == 1:
        
        data_season = [
            go.Bar(
                y=['spring', 'summer', 'autumn', 'winter'],
                x=list(df_season['count']),
                orientation='h'
                )
        ]

        data_dayofweek = [
            go.Bar(
                y=['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'],
                x=list(df_dayofweek['count']),
                orientation='h',
                marker=dict(
                    color=[
                        'rgb(57, 105, 219)',
                        'rgb(57, 105, 219)',
                        'rgb(57, 105, 219)',
                        'rgb(57, 105, 219)',
                        'rgb(57, 105, 219)',
                        'rgb(57, 105, 219)',
                        'rgb(195, 62, 0)',
                        'rgb(195, 62, 0)',
                    ]
                )
            )
        ]

        data_daily = [go.Bar(
            y=df['count'],
            x=df['datetime'],
            orientation='v',
        )]

        return html.Div([
            html.Div(
                dcc.Markdown('''
* * * *
                ''')
            ),

            html.Div(children=[
                html.Div(
                    dcc.Graph(
                        id='bar-plot1',
                        figure={
                            'title' : 'Seasonal Count',
                            'data' : data_season,
                            'layout' : {
                                'title' : 'Season',
                                'margin': {
                                    'l': 80,
                                    'r': 80,
                                    'b': 50,
                                    't': 100,
                                },
                            } 
                        },
                        style={
                            'height': '70vh',
                            'width' : '80vh',
                        }
                    ),
                    style={
                        'display' : 'inline-block'
                    },
                ),

                html.Div(
                    dcc.Graph(
                        id='bar-plot2',
                        figure={
                            'title' : 'Day of Week Count',
                            'data' : data_dayofweek,
                            'layout' : {
                                'title' : 'Day of Week',
                                'margin': {
                                    'l': 80,
                                    'r': 80,
                                    'b': 50,
                                    't': 100,
                                },
                            },
                        },
                        style={
                            'height': '70vh',
                            'width' : '80vh',
                        }
                    ),
                    style={
                        'display' : 'inline-block'
                    },
                ),

                html.Div(
                    dcc.Graph(
                        id='bar-plot3',
                        figure={
                            'data' : data_daily,
                            'layout' : {
                                'title' : 'Daily Count',
                                'margin': {
                                    'l': 80,
                                    'r': 80,
                                    'b': 50,
                                    't': 50
                                },
                            }
                        },
                        style={'height': '60vh'}
                    ),
                ),
            ])
        ])
            


    elif value == 2:
        corrMatx = df[["temp","atemp","casual","registered","humidity","windspeed","count"]].corr().values

        trace = go.Heatmap(
            z=corrMatx,
            x=df.columns,
            y=df.columns,
            colorscale='Blues'  # 히트맵 컬러스케일 ['Greys', 'YlGnBu', 'Greens', 'YlOrRd', 'Bluered', 'RdBu','Reds', 'Blues', 'Picnic', 'Rainbow', 'Portland', 'Jet','Hot', 'Blackbody', 'Earth', 'Electric', 'Viridis', 'Cividis']
            )
        data=[trace]

        return html.Div([
            # Markdown 텍스트 넣어주기 : 줄 넣기 
            html.Div(
                dcc.Markdown('''
* * * *
                ''')
            ),

            dcc.Graph(
                id='heatmap',
                figure={
                    'title' : 'Correlation Heatmap',
                    'data' : data,
                    'layout' : {
                        'title': 'Heatmap',
                    'margin': {
                        'l': 100, #left
                        'r': 100, #right
                        'b': 50,  #bottom
                        't': 100  #top
                        },
                    }
                },
                style={
                    'height': '80vh',
                    'width' : '80vh'
                    }
            ),

        ])


    # Table 보기 호출
    elif value == 3:
        
        return html.Div([
            
            # Markdown 텍스트 넣어주기 : 줄 넣기 
            html.Div(
                dcc.Markdown('''
* * * *
                ''')
            ),

            html.Div( children=[
                html.Div(
                    dash_table.DataTable(
                        id='table',
                        data=df.to_dict('rows'),
                        columns=[{'name':i, 'id':i} for i in df.columns],
                        # n_fixed_rows=1, # Header 고정
                        style_cell={
                            'textAlign': 'left',
                            'minWidth': '50px', 'maxWidth': '180px',
                            },
                        style_cell_conditional=[
                            {
                                'if':{'column_id':'index'},
                                'textAlign' : 'right'
                            }
                        ],
                        style_table={
                            'overflowX':'scroll', # X축 스크롤
                            'maxHeight':'600', # Height 고정
                            },
                    )
                )
            ])
        ])











if __name__ == '__main__':
    app.run_server(debug=True)