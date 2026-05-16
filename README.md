# 🎬 Netflix Analytics Dashboard

A professional, interactive Streamlit dashboard for comprehensive Netflix content analysis. This project demonstrates advanced data science, visualization, and web app development skills.

## 📋 Project Overview

This dashboard provides in-depth analytics of Netflix's content library with interactive visualizations, advanced filtering, and detailed insights. Built with Python, Pandas, Plotly, and Streamlit, it showcases data cleaning, exploratory data analysis, and professional UI/UX design.

## ✨ Key Features

### Data Processing
- **Complete Data Cleaning**: Removes duplicates, handles missing values, converts data types
- **Feature Engineering**: Extracts year/month from dates, separates duration values
- **Smart Parsing**: Explodes multi-value columns (countries, genres, directors) for detailed analysis

### Analytics & Insights
- **Content Distribution**: Movies vs TV Shows breakdown
- **Geographic Analysis**: Top content-producing countries
- **Genre Analysis**: Most popular categories and genres
- **Growth Trends**: Content addition over years
- **Rating Analysis**: Distribution across different rating categories
- **Director Insights**: Most prolific directors
- **Duration Analysis**: Movie runtime distribution

### Interactive Features
- **Advanced Filtering**: Filter by content type, rating, release year
- **Search Functionality**: Real-time search by title
- **Dynamic Charts**: Interactive Plotly visualizations with hover details
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Live Data Updates**: Filters apply instantly to all visualizations

### Professional UI/UX
- **Dark Modern Theme**: Netflix-inspired dark gradient background
- **KPI Metrics**: Key performance indicators at dashboard top
- **Custom Styling**: Professional color scheme with Netflix red (#E50914)
- **Organized Sections**: Logical grouping of related visualizations
- **Data Table**: Customizable sorting and row display

## 📊 Dashboard Sections

1. **Header Metrics**: Total content, movies, shows, average rating
2. **Content Distribution**: Pie chart vs ratings histogram
3. **Geographic Analysis**: Top countries and genres
4. **Growth Trends**: Content growth over years and movie duration distribution
5. **Top Directors**: Most prolific directors on Netflix
6. **Content Library**: Detailed, sortable data table with filtering

## 🛠️ Technology Stack

- **Python 3.8+**: Core programming language
- **Streamlit**: Web app framework for data apps
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Plotly**: Interactive visualizations
- **CSV**: Data storage format

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone or Download the Project**
```bash
cd Netflix-Dashboard
```

2. **Create Virtual Environment (Optional but Recommended)**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the Dashboard**
```bash
streamlit run app.py
```

5. **Access the Dashboard**
- Open your browser and navigate to: `http://localhost:8501`
- The dashboard will automatically reload on file changes

## 📁 File Structure

```
Netflix-Dashboard/
├── app.py                   # Main Streamlit application
├── netflix_titles.csv       # Dataset (Netflix titles)
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## 🎯 Key Code Sections Explained

### 1. Data Loading & Cleaning
```python
@st.cache_data
def load_and_clean_data(filepath):
    """
    - Loads CSV with pandas
    - Removes duplicates based on title and type
    - Converts date columns to datetime
    - Extracts numeric values from duration
    - Handles missing values intelligently
    - Returns three DataFrames: original, country-expanded, genre-expanded
    """
```

**Why this matters**: Ensures data quality and consistency for accurate analysis. Caching improves performance on re-runs.

### 2. KPI Metrics Calculation
```python
def get_overview_metrics(df):
    """
    Calculates:
    - Total content count
    - Movie vs TV show split
    - Average rating (converted to numeric scale)
    
    Returns dictionary for st.metric() display
    """
```

**Why this matters**: Provides executive summary of dataset in seconds. st.metric() offers clear KPI visualization.

### 3. Interactive Visualizations
```python
@st.plotly_chart(interactive_chart, use_container_width=True)
```

**Why this matters**: Plotly enables hover information, zoom, pan, and export capabilities. Professional interactive experience.

### 4. Sidebar Filtering
```python
with st.sidebar:
    content_type = st.multiselect(...)
    ratings = st.multiselect(...)
    selected_years = st.slider(...)
```

**Why this matters**: Allows users to customize analysis without modifying code. Enhances user engagement.

### 5. Responsive Layout
```python
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig1, use_container_width=True)
```

**Why this matters**: Two-column layout makes efficient use of space and maintains readability on all screen sizes.

## 💡 Skills Demonstrated

### Data Science
- ✅ Data cleaning and preprocessing
- ✅ Exploratory data analysis (EDA)
- ✅ Feature engineering
- ✅ Statistical analysis
- ✅ Data aggregation and grouping

### Visualization
- ✅ Multiple chart types (pie, bar, line, histogram)
- ✅ Interactive visualizations with Plotly
- ✅ Color theory and professional design
- ✅ Responsive layouts

### Web Development
- ✅ Streamlit framework expertise
- ✅ User interface design
- ✅ Performance optimization (caching)
- ✅ Error handling
- ✅ State management

### Software Engineering
- ✅ Clean, modular code structure
- ✅ Comprehensive comments and docstrings
- ✅ Proper function documentation
- ✅ Best practices and conventions
- ✅ Code organization

## 📈 Performance Optimization

- **@st.cache_data**: Caches data loading to prevent reprocessing
- **Efficient DataFrames**: Use pandas operations for speed
- **Responsive Design**: Mobile-friendly layout
- **Lazy Loading**: Charts render only when needed

## 🎨 Design Decisions

### Color Scheme
- **Primary**: Netflix Red (#E50914) for brand consistency
- **Secondary**: Dark Gray (#221F1F) for professional look
- **Background**: Dark gradient for eye comfort and modern aesthetic
- **Text**: White for high contrast and readability

### Layout
- **Sidebar**: Filters on left for intuitive navigation
- **Main Area**: Content flows top to bottom naturally
- **Metrics**: KPIs immediately visible for quick insights
- **Sections**: Logical grouping helps story telling

## 🚀 Potential Enhancements

1. **User Personalization**: Save favorite filters and visualizations
2. **Export Features**: Download charts as PNG or data as CSV
3. **Advanced Analytics**: Machine learning for recommendations
4. **Real-time Updates**: Connect to Netflix API for live data
5. **Additional Metrics**: Budget analysis, viewer trends
6. **Multi-language**: Support for multiple languages
7. **Comparison Tools**: Compare content across countries/regions
8. **Automated Reports**: Generate PDF reports

## 📚 Dataset Information

**File**: `netflix_titles.csv`

**Columns**:
- `show_id`: Unique identifier for each title
- `type`: Movie or TV Show
- `title`: Name of the content
- `director`: Director(s) of the content
- `cast`: Main cast members
- `country`: Country/countries of production
- `date_added`: Date when added to Netflix
- `release_year`: Original release year
- `rating`: Age/content rating
- `duration`: Length in minutes (movies) or seasons (TV shows)
- `listed_in`: Categories/genres
- `description`: Brief synopsis

## 🔧 Troubleshooting

### Issue: "FileNotFoundError: netflix_titles.csv"
**Solution**: Ensure the CSV file is in the same directory as app.py

### Issue: Dashboard loads slowly
**Solution**: Clear Streamlit cache with `streamlit cache clear`

### Issue: Charts not displaying
**Solution**: Verify Plotly is installed: `pip install --upgrade plotly`

### Issue: Filters not working
**Solution**: Ensure data types are correct; check column names match dataset

## 📝 License

This project is open-source and available for educational and portfolio purposes.

## 👨‍💻 Author

**Portfolio Project** - Netflix Analytics Dashboard
- Demonstrates professional data science skills
- Suitable for resume and freelance portfolios
- Production-ready code quality

## 🤝 Contributing

This is a portfolio project. For suggestions or improvements, feel free to fork and modify!

## 📞 Support

If you encounter issues:
1. Check that all files are in the correct directory
2. Verify all dependencies are installed: `pip install -r requirements.txt`
3. Clear Streamlit cache: `streamlit cache clear`
4. Restart the Streamlit server

## ⭐ Star This Project

If you find this useful, please consider starring the repository!

---

**Last Updated**: May 2024
**Status**: Production Ready ✅
**Quality Level**: Portfolio/Freelancer Grade
