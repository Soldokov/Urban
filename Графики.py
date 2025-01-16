import plotly.express as px
import plotly.io as pio
import plotly.offline as pyo
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Чтение данных и очистка от пропусков
data = pd.read_csv("VideoGames.csv")
data.columns = data.columns.str.strip()
cleaned_data = data.dropna()

#----------------------------------------------------------------------------- Первый холст
fig1 = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Продажи игр по жанрам",
                    "Доля выпущенных игр по платформам",
                    "Продажи игр по годам",
                    "Распределение игр по годам на различных платформах",
                    ),
    vertical_spacing=0.4,
    horizontal_spacing=0.25,
    specs=[[
        {"type": "bar"}, {"type": "pie"}],
        [{"type": "bar"}, {"type": "heatmap"}],
    ],
)

#----------------------------------------------------------------------------- Визуал графиков
fig1.update_layout(
    showlegend=True,
    height=1000,
    width=1400,
    title_font=dict(size=20),
    font=dict(size=14),
    margin=dict(t=100, b=100, l=100, r=100),
    legend = dict(
        orientation = 'h',
        yanchor = 'bottom',
        y = -0.2,
        xanchor = 'center',
        x = 0.5
    )
)
for annotations in fig1['layout']['annotations']: annotations['y'] += 0.05
#------------------------------------------------------------------------- Первый график (Жанры игр)
genre_counts = cleaned_data['Genre'].value_counts().reset_index()
genre_counts.columns = ['Genre', 'Counts']

fig1.add_trace(
    go.Bar(
        x=genre_counts["Genre"],
        y=genre_counts["Counts"],
        marker=dict(color="royalblue"),
        name="Жанр"
    ),
    row=1, col=1
)

#-------------------------------------------------------------------------------- Второй график (Доля продаж по платформам)
platform_sales = cleaned_data.groupby('Platform')['Global_Sales'].sum().reset_index()

total_sales = platform_sales["Global_Sales"].sum()
platform_sales['Share'] = platform_sales['Global_Sales'] / total_sales * 100
platform_sales['Platform'] = platform_sales.apply(
    lambda row: 'Other' if row['Share'] < 2.45 else row['Platform'], axis=1
)
platform_sales = platform_sales.groupby('Platform').agg({'Global_Sales': 'sum'}).reset_index()
fig1.add_trace(
    go.Pie(
        labels = platform_sales["Platform"],
        values = platform_sales["Global_Sales"],
        name = 'Доля платформ',
        showlegend = False
    ),
    row=1, col=2
)

#-------------------------------------------------------------------------------- Третий график (Продажи по годам)
filtered_data = cleaned_data[(cleaned_data['Year_of_Release'] >= 1990) &
                             (cleaned_data['Year_of_Release'] <= 2016)]
year_sales = filtered_data.groupby('Year_of_Release')['Global_Sales'].sum().reset_index()
fig1.add_trace(
    go.Scatter(
        x=year_sales['Year_of_Release'],
        y=year_sales['Global_Sales'],
        mode='lines',
        name='Количество продаж'
    ),
    row=2, col=1
)

#-------------------------------------------------------------------------------- Четвертый график (Корреляция 3D)
correlation = cleaned_data['Critic_Score'].corr(cleaned_data['Global_Sales'])
print(f"Корреляция между оценкой критиков и продажами: {correlation:.2f}")

# Для 3D-графика создаем отдельную фигуру
fig_3d = go.Figure()

fig_3d.add_trace(
    go.Scatter3d(
        x=cleaned_data['Critic_Score'],
        y=cleaned_data['User_Score'],
        z=cleaned_data['Global_Sales'],
        mode='markers',
        marker=dict(
            color=cleaned_data['Global_Sales'],
            colorscale='Viridis',
            size=5
        ),
    )
)

fig_3d.update_layout(
    scene=dict(
        xaxis_title='Оценка критиков',
        yaxis_title='Оценка игроков',
        zaxis_title='Глобальные продажи'
    ),
    title='Взаимосвязь между оценкой критиков, игроков и глобальными продажами',
    height=800,
    width=1000,
)
#-------------------------------------------------------------------------------- Пятый график (Тепловая карта по платформам)
games_by_year_platform = cleaned_data.groupby(['Platform', 'Year_of_Release']).size().unstack(fill_value=0)

fig1.add_trace(
    go.Heatmap(
        z = games_by_year_platform.values,
        x = games_by_year_platform.columns,
        y = games_by_year_platform.index,
        colorscale = 'YlGnBu',
        colorbar = dict(
            title = 'Количество игр',
            thickness = 10,
            len = 0.5,
            y = 0.17,
            x = 1.05
         )
    ),
    row = 2, col = 2
)
#--------------------------------------------------------------------------------- Первый график (оси)
fig1.update_xaxes(
    title_text="Жанр",
    tickangle=45,
    row=1, col=1
)
fig1.update_yaxes(
    title_text="Количество игр (млн копий)",
    row=1, col=1
)
#--------------------------------------------------------------------------------- Второй график (оси)
# row = 1, col = 2
#--------------------------------------------------------------------------------- Третий график (оси)
fig1.update_xaxes(
    title_text="Год релиза",
    row=2, col=1
)
fig1.update_yaxes(
    title_text="Количество продаж",
    row=2, col=1
)
#-------------------------------------------------------------------------------- Четвертый график (оси)

#--------------------------------------------------------------------------------- Пятый график (оси)
fig1.update_xaxes(
    title_text="Год",
    row=2, col=2
)
fig1.update_yaxes(
    title_text="Платформа",
    row=2, col=2
)
#----------------------------------------------------------------------------- Второй холст
fig2 = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Распределение оценок критиков",
                    "Продажи по регионам для популярных платформ",
                    "Тренд продаж игр со временем по жанрам",
                    "Продажи игр по возрастным рейтингам",
                    ),
    vertical_spacing=0.4,
    horizontal_spacing=0.25,
    specs=[[
        {"type": "bar"}, {"type": "bar"}],
        [{"type": "bar"}, {"type": "bar"}],
    ],
)

#----------------------------------------------------------------------------- Визуал графиков
fig2.update_layout(
    showlegend=True,
    height=1000,
    width=1400,
    title_font=dict(size=20),
    font=dict(size=14),
    margin=dict(t=100, b=100, l=100, r=100),
    legend = dict(
        orientation = 'h',
        yanchor = 'bottom',
        y = -0.2,
        xanchor = 'center',
        x = 0.5
    )
)
for annotations in fig2['layout']['annotations']: annotations['y'] += 0.05
#-------------------------------------------------------------------------------- Первый график (Распределение оценок критиков)
critic_score = cleaned_data['Critic_Score']
fig2.add_trace(
    go.Histogram(
    x = critic_score,
    nbinsx = 10,
    marker = dict(color = 'pink'),
    name = 'Распределение оценок критиков',
    showlegend= False
    ),
    row = 1, col = 1
)
#-------------------------------------------------------------------------------- Второй график (Продажи по регионам для популярных платформ)
popular_platform = ['PS4', 'PC', 'XOne', 'Wii', '3DS']
regional_sales = cleaned_data[cleaned_data['Platform'].isin(popular_platform)].groupby('Platform')[['NA_Sales', 'EU_Sales', 'JP_Sales']].sum().reset_index()

fig2.add_trace(
    go.Bar(
        x = regional_sales['Platform'],
        y = regional_sales['NA_Sales'],
        name = 'Северная Америка',
        marker = dict(color = 'Red')
    ),
    row = 1, col = 2
)

fig2.add_trace(
    go.Bar(
        x = regional_sales['Platform'],
        y = regional_sales['EU_Sales'],
        name = 'Европа',
        marker = dict(color = 'Green')
    ),
    row = 1, col = 2
)

fig2.add_trace(
    go.Bar(
        x = regional_sales['Platform'],
        y = regional_sales['JP_Sales'],
        name = 'Япония',
        marker = dict(color = 'Blue')
    ),
    row = 1, col = 2
)
#--------------------------------------------------------------------------------- Третий график (тренд продаж игр со временем)
filtered_data = cleaned_data[(cleaned_data['Year_of_Release'] >= 1995) &
                             (cleaned_data['Year_of_Release'] <= 2016)]
genre_year_sales = filtered_data.groupby(['Year_of_Release', 'Genre'])['Global_Sales'].sum().reset_index()

for genre in genre_year_sales['Genre'].unique():
    genre_data = genre_year_sales[genre_year_sales['Genre'] == genre]
    fig2.add_trace(go.Scatter(
        x = genre_data['Year_of_Release'],
        y = genre_data['Global_Sales'],
        mode = 'lines',
        name = genre,
        showlegend= False
    ),
    row = 2, col = 1
)
# --------------------------------------------------------------------------------- Четвертый график (Продажи игр по возрастному рейтингу)
age_rating_sales = cleaned_data.groupby('Rating')['Global_Sales'].sum().reset_index()

fig2.add_trace(
    go.Bar(
        x = age_rating_sales['Rating'],
        y = age_rating_sales['Global_Sales'],
        marker = dict(color = 'Salmon'),
        name = 'Продажи по возрастным рейтингам',
        showlegend= False
    ),
    row = 2, col = 2
)
#--------------------------------------------------------------------------------- Первый  график (оси)
fig2.update_xaxes(
    title_text="Оценка критиков",
    row=1, col=1
)
fig2.update_yaxes(
    title_text="Количество игр",
    row=1, col=1
)
#--------------------------------------------------------------------------------- Второй  график (оси)
fig2.update_xaxes(
    title_text="Платформы",
    row=1, col=2
)
fig2.update_yaxes(
    title_text="Продажи (млн копий)",
    row=1, col=2
)
#--------------------------------------------------------------------------------- Третий  график (оси)
fig2.update_xaxes(
    title_text="Год релиза",
    row=2, col=1
)
fig2.update_yaxes(
    title_text="Продажи (млн копий)",
    row=2, col=1
)
#--------------------------------------------------------------------------------- Четвертый график (оси)
fig2.update_xaxes(
    title_text="Возрастной рейтинг",
    row=2, col=2
)
fig2.update_yaxes(
    title_text="Продажи (млн копий)",
    row=2, col=2
)
#--------------------------------------------------------------------------------- Отображение графиков
print(cleaned_data.head())
fig1.show()  # Отображаем 2D-графики
fig2.show()  # Отображаем 2D-графики
fig_3d.show()  # Отображаем 3D-график