"""
Netflix Analytics Dashboard
A professional, interactive Streamlit dashboard for Netflix content analysis
with advanced visualizations, data cleaning, and filtering capabilities.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Netflix Analytics Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        font-size: 28px;
        color: #E50914;
    }
    [data-testid="stMetricLabel"] {
        font-size: 14px;
        color: #ffffff;
    }
    .main {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    .stSidebar {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
    }
    h1, h2, h3 {
        color: #E50914;
        font-weight: bold;
    }
    .stSelectbox, .stMultiSelect, .stSlider {
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== DATA LOADING & CACHING ====================
@st.cache_data
def load_and_clean_data(filepath):
    """
    Load Netflix dataset and perform comprehensive data cleaning.
    
    Steps:
    1. Load CSV file
    2. Remove duplicates
    3. Handle missing values
    4. Convert and clean date columns
    5. Clean duration column
    6. Extract additional features
    
    Returns:
        pd.DataFrame: Cleaned dataset
    """
    # Load data
    df = pd.read_csv(filepath)
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['title', 'type'])
    
    # Handle missing values
    df['director'] = df['director'].fillna('Unknown')
    df['cast'] = df['cast'].fillna('Unknown')
    df['country'] = df['country'].fillna('Unknown')
    df['rating'] = df['rating'].fillna('Not Rated')
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    
    # Clean duration column: separate numeric values for movies (minutes) and TV shows (seasons)
    # Using pd.to_numeric with errors='coerce' handles NaN values safely
    # This converts failed extractions to NaN, then fillna(0) provides default values
    # Using nullable Int64 dtype to handle integer NaN values properly
    extracted_duration = df['duration'].str.extract(r'(\d+)')[0]
    df['duration_value'] = pd.to_numeric(extracted_duration, errors='coerce').fillna(0).astype('Int64')
    
    # Extract year from date_added
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month
    
    # Convert release_year to numeric
    df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
    
    # Split country and genre columns (some rows have multiple values)
    df['country_list'] = df['country'].str.split(', ')
    df['genre_list'] = df['listed_in'].str.split(', ')
    
    # Create country and genre for individual analysis
    df_expanded_country = df.explode('country_list')
    df_expanded_country['country_list'] = df_expanded_country['country_list'].str.strip()
    
    df_expanded_genre = df.explode('genre_list')
    df_expanded_genre['genre_list'] = df_expanded_genre['genre_list'].str.strip()
    
    return df, df_expanded_country, df_expanded_genre


# ==================== DATA ANALYSIS FUNCTIONS ====================
def get_overview_metrics(df):
    """
    Calculate key performance indicators for the dashboard header.
    
    Returns:
        dict: Contains total content, movies, shows, and average rating
    """
    total_content = len(df)
    total_movies = len(df[df['type'] == 'Movie'])
    total_shows = len(df[df['type'] == 'TV Show'])
    
    # Calculate average rating (convert rating to numeric scale)
    rating_mapping = {'G': 1, 'PG': 2, 'PG-13': 3, 'R': 4, 'TV-MA': 5, 'TV-14': 4}
    avg_rating = df['rating'].map(rating_mapping).mean()
    
    return {
        'total': total_content,
        'movies': total_movies,
        'shows': total_shows,
        'avg_rating': round(avg_rating, 1) if not np.isnan(avg_rating) else 0
    }


def get_content_distribution(df):
    """Generate pie chart for Movies vs TV Shows distribution."""
    distribution = df['type'].value_counts().reset_index()
    distribution.columns = ['Type', 'Count']
    
    fig = go.Figure(data=[go.Pie(
        labels=distribution['Type'],
        values=distribution['Count'],
        marker=dict(colors=['#E50914', '#221F1F']),
        textposition='inside',
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        height=400,
        showlegend=True,
        font=dict(color='white'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def get_top_countries(df_expanded_country):
    """Generate bar chart for top content-producing countries."""
    top_countries = df_expanded_country['country_list'].value_counts().head(10).reset_index()
    top_countries.columns = ['Country', 'Content Count']
    
    fig = px.bar(
        top_countries,
        x='Content Count',
        y='Country',
        orientation='h',
        title='Top 10 Countries Producing Content',
        color='Content Count',
        color_continuous_scale=['#221F1F', '#E50914'],
        labels={'Country': 'Country', 'Content Count': 'Number of Titles'}
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        font=dict(color='white'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    )
    
    fig.update_traces(marker_line_width=0)
    
    return fig


def get_top_genres(df_expanded_genre):
    """Generate bar chart for top genres/categories."""
    top_genres = df_expanded_genre['genre_list'].value_counts().head(12).reset_index()
    top_genres.columns = ['Genre', 'Count']
    
    fig = px.bar(
        top_genres.sort_values('Count'),
        x='Count',
        y='Genre',
        orientation='h',
        title='Top 12 Genres/Categories on Netflix',
        color='Count',
        color_continuous_scale='Reds',
        labels={'Genre': 'Genre', 'Count': 'Number of Titles'}
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        font=dict(color='white'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    )
    
    fig.update_traces(marker_line_width=0)
    
    return fig


def get_ratings_distribution(df):
    """Generate histogram for content ratings distribution."""
    ratings_order = ['G', 'PG', 'PG-13', 'R', 'NC-17', 'TV-Y', 'TV-Y7', 'TV-G', 
                     'TV-PG', 'TV-14', 'TV-MA', 'Not Rated', 'Unknown']
    
    rating_counts = df['rating'].value_counts().reindex(ratings_order, fill_value=0)
    rating_counts = rating_counts[rating_counts > 0]
    
    colors = ['#E50914' if i % 2 == 0 else '#221F1F' for i in range(len(rating_counts))]
    
    fig = go.Figure(data=[
        go.Bar(
            x=rating_counts.index,
            y=rating_counts.values,
            marker=dict(color=colors, line=dict(width=0)),
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='Content Distribution by Rating',
        xaxis_title='Rating',
        yaxis_title='Number of Titles',
        height=400,
        font=dict(color='white'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    )
    
    return fig


def get_content_growth(df):
    """Generate line chart showing content growth over years."""
    # Filter out null years
    df_clean = df.dropna(subset=['year_added'])
    df_clean = df_clean[df_clean['year_added'] >= 2010]
    
    growth = df_clean.groupby(['year_added', 'type']).size().reset_index(name='count')
    
    fig = px.line(
        growth,
        x='year_added',
        y='count',
        color='type',
        title='Netflix Content Growth Over Years',
        markers=True,
        color_discrete_map={'Movie': '#E50914', 'TV Show': '#221F1F'},
        labels={'year_added': 'Year Added', 'count': 'Number of Titles', 'type': 'Content Type'}
    )
    
    fig.update_layout(
        height=400,
        font=dict(color='white'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)'),
        hovermode='x unified'
    )
    
    fig.update_traces(mode='lines+markers', marker=dict(size=6))
    
    return fig


def get_top_directors(df):
    """Generate bar chart for top directors."""
    # Expand directors (some entries have multiple)
    directors_expanded = df.copy()
    directors_expanded['director'] = directors_expanded['director'].str.split(', ')
    directors_expanded = directors_expanded.explode('director')
    directors_expanded['director'] = directors_expanded['director'].str.strip()
    
    top_directors = directors_expanded[directors_expanded['director'] != 'Unknown']['director'].value_counts().head(10)
    
    fig = px.bar(
        x=top_directors.values,
        y=top_directors.index,
        orientation='h',
        title='Top 10 Most Prolific Directors',
        color=top_directors.values,
        color_continuous_scale=['#221F1F', '#E50914'],
        labels={'x': 'Number of Titles', 'y': 'Director'}
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        font=dict(color='white'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    )
    
    fig.update_traces(marker_line_width=0)
    
    return fig


def get_movie_duration_distribution(df):
    """Generate histogram for movie duration analysis."""
    movies = df[df['type'] == 'Movie'].copy()
    movies = movies[movies['duration_value'] < 300]  # Remove outliers
    
    fig = go.Figure(data=[
        go.Histogram(
            x=movies['duration_value'],
            nbinsx=30,
            marker=dict(color='#E50914', line=dict(width=1, color='#221F1F')),
            hovertemplate='Duration: %{x} min<br>Count: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='Movie Duration Distribution',
        xaxis_title='Duration (minutes)',
        yaxis_title='Number of Movies',
        height=400,
        font=dict(color='white'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    )
    
    return fig


# ==================== MAIN DASHBOARD ====================
def main():
    """Main function to build the complete dashboard."""
    
    # Load and clean data
    df, df_expanded_country, df_expanded_genre = load_and_clean_data('netflix_titles.csv')
    
    # ========== HEADER SECTION ==========
    st.title('🎬 Netflix Analytics Dashboard')
    st.markdown('---')
    
    # KPI Metrics
    metrics = get_overview_metrics(df)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total Content', metrics['total'], delta=None)
    with col2:
        st.metric('Movies', metrics['movies'], 
                 delta=f"{round((metrics['movies']/metrics['total']*100), 1)}%")
    with col3:
        st.metric('TV Shows', metrics['shows'], 
                 delta=f"{round((metrics['shows']/metrics['total']*100), 1)}%")
    with col4:
        st.metric('Avg Rating Score', metrics['avg_rating'], delta=None)
    
    st.markdown('---')
    
    # ========== SIDEBAR FILTERS ==========
    with st.sidebar:
        st.header('🎯 Filters & Search')
        
        # Content type filter
        content_type = st.multiselect(
            'Content Type',
            options=df['type'].unique(),
            default=df['type'].unique(),
            key='content_type'
        )
        
        # Rating filter
        ratings = st.multiselect(
            'Rating',
            options=sorted(df['rating'].unique()),
            default=sorted(df['rating'].unique()),
            key='rating_filter'
        )
        
        # Release year range
        year_min, year_max = int(df['release_year'].min()), int(df['release_year'].max())
        selected_years = st.slider(
            'Release Year Range',
            min_value=year_min,
            max_value=year_max,
            value=(year_min, year_max),
            key='year_range'
        )
        
        # Search by title
        search_title = st.text_input(
            'Search by Title',
            placeholder='Enter movie or show name...',
            key='search_title'
        )
        
        # Apply filters
        df_filtered = df[
            (df['type'].isin(content_type)) &
            (df['rating'].isin(ratings)) &
            (df['release_year'].between(selected_years[0], selected_years[1]))
        ]
        
        if search_title:
            df_filtered = df_filtered[df_filtered['title'].str.contains(search_title, case=False, na=False)]
        
        st.markdown('---')
        st.info(f'📊 Showing {len(df_filtered)} out of {len(df)} titles')
    
    # ========== MAIN CONTENT SECTIONS ==========
    
    # Section 1: Content Distribution & Overview
    st.header('📈 Content Distribution Overview')
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(get_content_distribution(df_filtered), use_container_width=True)
    
    with col2:
        st.plotly_chart(get_ratings_distribution(df_filtered), use_container_width=True)
    
    # Section 2: Geographic & Genre Analysis
    st.header('🌍 Geographic & Genre Analysis')
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(get_top_countries(df_expanded_country[df_expanded_country['show_id'].isin(df_filtered['show_id'])]), use_container_width=True)
    
    with col2:
        st.plotly_chart(get_top_genres(df_expanded_genre[df_expanded_genre['show_id'].isin(df_filtered['show_id'])]), use_container_width=True)
    
    # Section 3: Content Growth & Duration
    st.header('📅 Content Growth & Runtime Analysis')
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(get_content_growth(df_filtered), use_container_width=True)
    
    with col2:
        st.plotly_chart(get_movie_duration_distribution(df_filtered), use_container_width=True)
    
    # Section 4: Directors & Detailed Table
    st.header('🎥 Top Directors & Content Library')
    st.plotly_chart(get_top_directors(df_filtered), use_container_width=True)
    
    # Section 5: Detailed Data Table
    st.header('📋 Content Library Details')
    
    # Display options
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        sort_by = st.selectbox(
            'Sort by',
            options=['Release Year (Newest)', 'Release Year (Oldest)', 'Title (A-Z)'],
            key='sort_by'
        )
    
    with col2:
        rows_display = st.slider('Rows to Display', 5, 50, 10, key='rows_display')
    
    with col3:
        st.write('')  # Spacing
    
    # Apply sorting
    df_display = df_filtered.copy()
    if sort_by == 'Release Year (Newest)':
        df_display = df_display.sort_values('release_year', ascending=False)
    elif sort_by == 'Release Year (Oldest)':
        df_display = df_display.sort_values('release_year', ascending=True)
    else:
        df_display = df_display.sort_values('title', ascending=True)
    
    # Display table
    display_columns = ['title', 'type', 'release_year', 'rating', 'country', 'listed_in', 'duration']
    st.dataframe(
        df_display[display_columns].head(rows_display),
        use_container_width=True,
        height=400
    )
    
    # ========== FOOTER SECTION ==========
    st.markdown('---')
    st.markdown("""
    <div style='text-align: center; color: #888; font-size: 12px;'>
    <p>Netflix Analytics Dashboard • Data Source: Netflix Titles Dataset</p>
    <p>Built with Streamlit · Visualized with Plotly</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
