import pandas as pd
import altair as alt

data = pd.read_csv('VideoGames.csv')
data.columns = data.columns.str.strip()
cleaned_data = data.dropna()

genre_counts = cleaned_data['Genre'].value_counts().reset_index()
genre_counts.columns = ['Genre', 'Counts']
#------------------------------------------------------------------------- Первый график (Жанры игр)
line = alt.Chart(genre_counts).mark_bar().encode(
    x = 'Genre:N',
    y = 'Counts:Q',
    color = 'Genre:N',
    tooltip = ['Genre:N', 'Counts:Q']
).properties(
    title = 'Продажи игр по жанрам',
    width = 800,
    height = 600
)
#------------------------------------------------------------------------- Второй график (Доля продаж по платформам)
platform_sales = cleaned_data.groupby('Platform')['Global_Sales'].sum().reset_index()

pie = alt.Chart(platform_sales).mark_arc().encode(
    theta = 'Global_Sales:Q',
    color = 'Platform:N',
    tooltip = ['Platform:N', 'Global_Sales:Q']
).properties(
    title = 'Доля выпущенных игр по платформам',
    width = 800,
    height = 600
)
#------------------------------------------------------------------------- Третий график (Продажи по годам)
filtered_data = cleaned_data[(cleaned_data['Year_of_Release'] >= 1990) &
                             (cleaned_data['Year_of_Release'] <= 2016)]
year_sales = filtered_data.groupby('Year_of_Release')['Global_Sales'].sum().reset_index()

line2 = alt.Chart(year_sales).mark_line().encode(
    x = 'Year_of_Release:O',
    y = 'Global_Sales:Q',
    tooltip = ['Year_of_Release', 'Global_Sales']
).properties(
    title = 'Продажи игр по годам',
    width = 800,
    height = 600
)
#-------------------------------------------------------------------------------- Четвертый график (Тепловая карта по платформам)
games_by_year_platform = cleaned_data.groupby(['Platform', 'Year_of_Release']).size().unstack(fill_value=0)
heatmap_data = games_by_year_platform.reset_index().melt(id_vars = 'Platform', var_name = 'Year_of_Release', value_name = 'Game_Count')

heatmap = alt.Chart(heatmap_data).mark_rect().encode(
    x = 'Year_of_Release:O',
    y = 'Platform:N',
    color = 'Game_Count:Q',
    tooltip = ['Platform:N', 'Year_of_Release:O', 'Game_Count:Q']
).properties(
    title = 'Распределение игр по годам на различных платформах',
    width = 800,
    height = 600
)
#-------------------------------------------------------------------------------- Пятый график (Распределение оценок критиков)
critic_score = cleaned_data[['Critic_Score']].sample(n=5000, random_state=42)

histogram = alt.Chart(critic_score).mark_bar().encode(
    x = alt.X('Critic_Score:Q', bin = True),
    y = 'count():Q',
    color = 'Critic_Score:Q',
    tooltip = ['Critic_Score:Q', 'count():Q']
).properties(
    title = 'Распределение оценок критиков',
    width = 800,
    height = 600
)
#-------------------------------------------------------------------------------- Шестой график (Продажи по регионам для популярных платформ)
popular_platform = ['PS4', 'PC', 'Wii', 'XOne', '3DS']
regional_sales = cleaned_data[cleaned_data['Platform'].isin(popular_platform)].groupby('Platform')[['NA_Sales', 'EU_Sales', 'JP_Sales']].sum()
regional_sales_long = regional_sales.reset_index().melt(id_vars = 'Platform', var_name = 'Region', value_name = 'Sales')
bars = alt.Chart(regional_sales_long).mark_bar().encode(
    x = 'Platform:N',
    y = 'Sales:Q',
    color = 'Region:N',
    tooltip = ['Platform:N', 'Region:N', 'Sales:Q']
).properties(
    title = 'Продажи по регионам для популярных платформ',
    width = 800,
    height = 600
)
#--------------------------------------------------------------------------------- Седьмой график (тренд продаж игр со временем)
filtered_data2 = cleaned_data[(cleaned_data['Year_of_Release'] >= 1995) &
                             (cleaned_data['Year_of_Release'] <= 2016)]
genre_year_sales = filtered_data2.groupby(['Year_of_Release', 'Genre'])['Global_Sales'].sum().reset_index()

line3 = alt.Chart(genre_year_sales).mark_line().encode(
    x = 'Year_of_Release:O',
    y = 'Global_Sales:Q',
    color = 'Genre:N',
    tooltip = ['Year_of_Release', 'Global_Sales', 'Genre:N']
).properties(
    title = 'Тренд продаж игр со временем по жанрам',
    width = 800,
    height = 600
)
# --------------------------------------------------------------------------------- Восьмой график (Продажи игр по возрастному рейтингу)
age_rating_sales = cleaned_data.groupby('Rating')['Global_Sales'].sum().reset_index()

bars2 = alt.Chart(age_rating_sales).mark_bar().encode(
    x = 'Rating:O',
    y = 'Global_Sales:Q',
    color = 'Rating:O',
    tooltip = ['Rating:O', 'Global_Sales:Q']
).properties(
    title = '',
    width = 800,
    height = 600
)
# --------------------------------------------------------------------------------- Девятый график (Корреляция между оценками игроков, критиков и продажами)
cleaned_data.columns = cleaned_data.columns.astype(str)
corr_data = cleaned_data[['Critic_Score', 'User_Score', 'Global_Sales']].sample(n=5000, random_state=42)

corr = alt.Chart(corr_data).mark_point().encode(
    x = 'Critic_Score:Q',
    y = 'User_Score:Q',
    color = 'Global_Sales:Q',
    size = 'Global_Sales:Q',
    tooltip = ['Critic_Score:Q', 'User_Score:Q', 'Global_Sales:Q']
).properties(
    title = 'Взаимосвязь между оценкой критиков, игроков и глобальными продажами',
    width = 800,
    height = 600
)
#--------------------------------------------------------------------------------- Отображение графиков
combine = line | pie + line2 | line2 + heatmap | histogram + bars| line3 + bars2 | corr
combine.display()
line.save('line_chart.html')
pie.save('pie_chart.html')
line2.save('line2_chart.html')
heatmap.save('heatmap_chart.html')
histogram.save('histogram_chart.html')
bars.save('bars_chart.html')
line3.save('line3_chart.html')
bars2.save('bars2_chart.html')
corr.save('corr_chart.html')