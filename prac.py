import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie

# Page Configuration
st.set_page_config(page_title="Google Playstore Analysis", layout="wide")

# ========== DATA LOADING FUNCTIONS ==========
@st.cache_data
def load_playstore_data():
    return pd.read_csv("googleplaystore.csv")

@st.cache_data
def load_cleaned_data():
    return pd.read_csv("preprocessed_GPS.csv")

@st.cache_data
def load_reviews_data():
    return pd.read_csv("googleplaystore_user_reviews.csv")

@st.cache_data
def load_merged_data():
    return pd.read_csv("Mergetdatasets.csv")

# ========== LOTTIE URLS ==========
LOTTIE_MAIN = "https://lottie.host/4e8d1f22-b420-4473-a3a0-97f05dc2c02f/KGfTwHTy0u.json"
LOTTIE_DATASET = "https://lottie.host/abaea818-8861-44c8-884c-8d7888810699/kScLGeM8LN.json"
LOTTIE_DESCRIPTIVE = "https://lottie.host/273c7831-bcda-4296-9d2b-ab145375b316/PcxCfTTnEu.json"
LOTTIE_VIZHUB = "https://lottie.host/8d009708-cb3c-4d8f-8536-d1d7790de87e/wgZQje80me.json"

# ========== SIDEBAR NAVIGATION ==========
with st.sidebar:
    option_main = option_menu(
        "Navigation",
        ["Main", "Dataset", "Descriptive Analysis", "Viz Hub", "Visualization 1", "Visualization 2"],
        icons=["house", "database", "info-circle", "bar-chart", "book", "eye"],
        menu_icon="list",
        default_index=0
    )

# ========== MAIN PAGE ==========
if option_main == "Main":
    with st.expander("Welcome! Click to explore", expanded=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            st_lottie(LOTTIE_MAIN, key="main_animation", width=300, height=300)
        with col2:
            st.title("Google Playstore App Analysis")
            st.markdown("""
            This application provides a comprehensive analysis of the Google Play Store dataset.
            You can explore app ratings, downloads, sizes, pricing trends, and user sentiments.
            
            The analysis covers:
            - Dataset exploration and preprocessing
            - Statistical summaries and descriptive analysis
            - Interactive visualizations
            - User review sentiment analysis
            
            Navigate through the sidebar to explore different aspects of the data.
            """)

# ========== DATASET PAGE ==========
elif option_main == "Dataset":
    st.title("Dataset Explorer")
    
    dataset_choice = st.selectbox("Select Dataset", ["Google Playstore", "User Reviews"])
    
    if dataset_choice == "Google Playstore":
        df = load_playstore_data()
        view_option = st.selectbox(
            "View Options", 
            ["Raw Data", "Basic Information", "Missing Values", "Data Types", "Cleaned Data"]
        )
        
        if view_option == "Raw Data":
            st.dataframe(df)
            
        elif view_option == "Basic Information":
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Rows", df.shape[0])
            col2.metric("Total Columns", df.shape[1])
            col3.metric("Duplicate Rows", df.duplicated().sum())
            st.write("Column Names:", ", ".join(df.columns))
            st.write("Dataset Summary:")
            st.dataframe(df.describe())
            
        elif view_option == "Missing Values":
            missing_data = df.isnull().sum()
            missing_data = missing_data[missing_data > 0]
            if len(missing_data) > 0:
                st.dataframe(missing_data.reset_index().rename(
                    columns={"index": "Column", 0: "Missing Values"}
                ))
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.heatmap(df.isnull(), yticklabels=False, cbar=True, ax=ax)
                st.pyplot(fig)
            else:
                st.success("No missing values found in the dataset.")
                
        elif view_option == "Data Types":
            st.dataframe(df.dtypes.reset_index().rename(
                columns={"index": "Column", 0: "Data Type"}
            ))
            
        else:  # Cleaned Data
            df_clean = load_cleaned_data()
            st.dataframe(df_clean)
            
    else:  # User Reviews
        df = load_reviews_data()
        view_option = st.selectbox(
            "View Options",
            ["Raw Data", "Basic Information", "Missing Values", "Data Types", "Cleaned Data"]
        )
        
        if view_option == "Raw Data":
            st.dataframe(df)
            
        elif view_option == "Basic Information":
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Rows", df.shape[0])
            col2.metric("Total Columns", df.shape[1])
            col3.metric("Duplicate Rows", df.duplicated().sum())
            st.write("Column Names:", ", ".join(df.columns))
            
        elif view_option == "Missing Values":
            missing_data = df.isnull().sum()
            missing_data = missing_data[missing_data > 0]
            if len(missing_data) > 0:
                st.dataframe(missing_data.reset_index().rename(
                    columns={"index": "Column", 0: "Missing Values"}
                ))
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.heatmap(df.isnull(), yticklabels=False, cbar=True, ax=ax)
                st.pyplot(fig)
            else:
                st.success("No missing values found in the dataset.")
                
        elif view_option == "Data Types":
            st.dataframe(df.dtypes.reset_index().rename(
                columns={"index": "Column", 0: "Data Type"}
            ))
            
        else:  # Cleaned Data
            df_clean = load_merged_data()
            st.dataframe(df_clean)

# ========== DESCRIPTIVE ANALYSIS PAGE ==========
elif option_main == "Descriptive Analysis":
    col1, col2 = st.columns([1, 2])
    with col1:
        st_lottie(LOTTIE_DESCRIPTIVE, key="desc_animation", width=250, height=250)
    with col2:
        st.title("Descriptive Analysis")
    
    tab1, tab2 = st.tabs(["Playstore Dataset", "User Reviews Dataset"])
    
    with tab1:
        st.subheader("Playstore Dataset Description")
        st.markdown("""
        **App**: The name of the application with a brief description.
        
        **Category**: The category under which the app is listed.
        
        **Rating**: The average user rating given to the app.
        
        **Reviews**: The total number of user reviews received.
        
        **Size**: The storage space required by the app on a mobile device.
        
        **Installs**: The total number of downloads or installations.
        
        **Type**: Indicates whether the app is free or paid.
        
        **Price**: The cost to download the app (zero for free apps).
        
        **Content Rating**: Specifies the age group suitability.
        
        **Genres**: Various categories the app belongs to.
        
        **Last Updated**: The date when the app was last updated.
        
        **Current Version**: The current version number of the app.
        
        **Android Version**: The minimum Android version required.
        """)
    
    with tab2:
        st.subheader("User Reviews Dataset Description")
        st.markdown("""
        **App**: The name of the application.
        
        **Translated Review**: The English translation of the user's review.
        
        **Sentiment**: The sentiment category - Positive, Negative, or Neutral.
        
        **Sentiment Polarity**: A score ranging from -1 (negative) to 1 (positive).
        
        **Sentiment Subjectivity**: A score from 0 to 1 where higher values indicate 
        opinion-based reviews and lower values indicate factual reviews.
        """)
    
    # Preprocessing Steps
    st.markdown("---")
    st.subheader("Data Preprocessing Steps")
    
    with st.expander("Click to view preprocessing details"):
        preprocessing_steps = [
            "Identified and removed rows with non-numeric characters in Reviews column.",
            "Removed irrelevant rows containing incorrect data.",
            "Converted Reviews column to integer data type.",
            "Converted Last Updated column to datetime format.",
            "Removed dollar sign from Price column and converted to float.",
            "Removed plus sign from Installs column and converted to integer.",
            "Standardized Size column to MB format.",
            "Removed duplicate rows from all datasets.",
            "Filled missing values: numerical with median, categorical with mode.",
            "Removed outliers using 5th and 95th percentiles.",
            "Dropped unnecessary columns like Current Version and Translated Review."
        ]
        for step in preprocessing_steps:
            st.write("- " + step)

# ========== VIZ HUB PAGE ==========
elif option_main == "Viz Hub":
    col1, col2 = st.columns([1, 2])
    with col1:
        st_lottie(LOTTIE_VIZHUB, key="vizhub_animation", width=250, height=250)
    with col2:
        st.title("Visualization Hub")
        st.markdown("""
        Welcome to the Visualization Hub. This section provides access to various 
        visualizations and analytical charts.
        
        Use the sidebar navigation to explore:
        
        1. **Visualization 1**: Exploratory data analysis, distributions, and comparisons
        2. **Visualization 2**: Sentiment analysis from user reviews
        
        Each visualization provides interactive charts that can be explored further.
        """)

# ========== VISUALIZATION 1 PAGE ==========
elif option_main == "Visualization 1":
    df = load_cleaned_data()
    
    with st.sidebar:
        viz_option = option_menu(
            "Select Analysis Type",
            ["Exploratory Analysis", "Comparative Analysis Part 1", "Comparative Analysis Part 2"],
            icons=["bar-chart", "pie-chart", "scatter"],
            menu_icon="graph-up"
        )
    
    if viz_option == "Exploratory Analysis":
        st.title("Exploratory Data Analysis")
        
        # Box Plots
        st.subheader("Distribution of Numerical Features")
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=('Rating', 'Installs', 'Size (MB)', 'Price', 'Reviews')
        )
        fig.add_trace(go.Box(y=df['Rating'], name='Rating'), row=1, col=1)
        fig.add_trace(go.Box(y=df['Installs'], name='Installs'), row=1, col=2)
        fig.add_trace(go.Box(y=df['Size in mb'], name='Size (MB)'), row=2, col=1)
        fig.add_trace(go.Box(y=df['Price'], name='Price'), row=2, col=2)
        fig.add_trace(go.Box(y=df['Reviews'], name='Reviews'), row=3, col=1)
        fig.update_layout(height=700, showlegend=False)
        st.plotly_chart(fig)
        
        # Rating Distribution
        st.subheader("Rating Distribution")
        fig = px.histogram(
            df, x="Rating", 
            color_discrete_sequence=['indianred'],
            title="Distribution of App Ratings"
        )
        st.plotly_chart(fig)
        
        # Category Distribution
        st.subheader("Number of Apps by Category")
        category_counts = df['Category'].value_counts().reset_index()
        category_counts.columns = ['Category', 'Count']
        fig = px.bar(
            category_counts.head(20), 
            x='Category', 
            y='Count',
            title="Top 20 App Categories",
            color='Category'
        )
        st.plotly_chart(fig)
        
    elif viz_option == "Comparative Analysis Part 1":
        st.title("Comparative Analysis - Part 1")
        
        # Reviews vs Installs
        st.subheader("Relationship between Reviews and Installs")
        fig = px.scatter(
            df, x='Reviews', y='Installs', 
            trendline='ols',
            title='Reviews vs Installs with Regression Line'
        )
        st.plotly_chart(fig)
        
        # Free vs Paid Apps
        st.subheader("Distribution of Free vs Paid Apps")
        app_type_counts = df["Type"].value_counts().reset_index()
        app_type_counts.columns = ['Type', 'Count']
        fig = px.pie(
            app_type_counts, 
            values='Count', 
            names='Type',
            title='Free vs Paid Apps Distribution'
        )
        st.plotly_chart(fig)
        
        # Installs by Type
        st.subheader("Number of Installs by App Type")
        fig = px.box(
            df, x='Type', y='Installs',
            title='Installs Distribution by App Type',
            color='Type'
        )
        st.plotly_chart(fig)
        
        # Top Genres by Installs
        st.subheader("Top 10 Genres by Installs")
        genre_installs = df.groupby('Genres')['Installs'].sum().sort_values(ascending=False).head(10)
        fig = px.bar(
            x=genre_installs.index, 
            y=genre_installs.values,
            title='Top Genres by Total Installs',
            labels={'x': 'Genres', 'y': 'Total Installs'}
        )
        st.plotly_chart(fig)
        
        # Rating by Update Year
        st.subheader("Rating Trends by Update Year")
        fig = px.scatter(
            df, x='Update year', y='Rating', 
            trendline='ols',
            title='Rating vs Update Year'
        )
        st.plotly_chart(fig)
        
        # Top Categories by Revenue
        st.subheader("Top Categories by Average Revenue")
        category_revenue = df.groupby("Category")["Revenue"].mean().sort_values(ascending=False).head(10)
        fig = px.bar(
            x=category_revenue.index,
            y=category_revenue.values,
            title='Average Revenue by Category',
            labels={'x': 'Category', 'y': 'Average Revenue'}
        )
        st.plotly_chart(fig)
        
    else:  # Comparative Analysis Part 2
        st.title("Comparative Analysis - Part 2")
        
        # Top Paid Apps by Rating
        st.subheader("Top 5 Highest Rated Paid Apps")
        top_paid = df[df['Type'] == 'Paid'].sort_values('Rating', ascending=False).head(5)
        fig = px.scatter(
            top_paid,
            x='Rating',
            y='App',
            size='Installs',
            color='Reviews',
            title='Top Paid Apps by Rating'
        )
        st.plotly_chart(fig)
        
        # Top Free Apps by Rating
        st.subheader("Top 10 Highest Rated Free Apps")
        top_free = df[df['Type'] == 'Free'].sort_values('Rating', ascending=False).head(10)
        fig = px.bar(
            top_free,
            x='App',
            y='Rating',
            title='Top Free Apps by Rating',
            color='Rating'
        )
        st.plotly_chart(fig)
        
        # Top Free Apps by Reviews
        st.subheader("Top 5 Free Apps with Most Reviews")
        top_reviewed_free = df[df['Type'] == 'Free'].sort_values('Reviews', ascending=False).head(5)
        fig = px.scatter(
            top_reviewed_free,
            x='Rating',
            y='App',
            size='Installs',
            color='Reviews',
            title='Top Free Apps by Reviews'
        )
        st.plotly_chart(fig)
        
        # Revenue vs Installs
        st.subheader("Revenue vs Installs by Category")
        category_data = df.groupby('Category').agg({
            'Revenue': 'mean',
            'Installs': 'sum',
            'Reviews': 'mean',
            'Rating': 'mean'
        }).head(10)
        fig = px.scatter(
            category_data,
            x="Revenue",
            y="Installs",
            size="Reviews",
            color=category_data.index,
            hover_name="Rating",
            title='Revenue vs Installs by Category'
        )
        st.plotly_chart(fig)
        
        # Installs Distribution
        st.subheader("Installs Distribution")
        fig = px.histogram(df, x="Installs", title="Distribution of App Installs")
        st.plotly_chart(fig)

# ========== VISUALIZATION 2 PAGE ==========
elif option_main == "Visualization 2":
    st.title("Sentiment Analysis from User Reviews")
    
    # Load and prepare data
    df_playstore = load_cleaned_data()
    df_reviews = load_reviews_data()
    
    # Clean reviews data
    df_reviews_clean = df_reviews.copy()
    df_reviews_clean.drop_duplicates(inplace=True)
    df_reviews_clean['Sentiment_Polarity'].fillna(df_reviews_clean['Sentiment_Polarity'].median(), inplace=True)
    df_reviews_clean['Sentiment_Subjectivity'].fillna(df_reviews_clean['Sentiment_Subjectivity'].median(), inplace=True)
    df_reviews_clean['Sentiment'].fillna(df_reviews_clean['Sentiment'].mode()[0], inplace=True)
    df_reviews_clean.drop('Translated_Review', axis=1, inplace=True)
    
    # Merge datasets
    merged_df = pd.merge(df_playstore, df_reviews_clean, on='App', how='inner')
    
    # Sentiment Polarity Distribution
    st.subheader("Distribution of Sentiment Polarity")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df_reviews_clean['Sentiment_Polarity'], bins=50, kde=True, ax=ax)
    ax.set_title('Sentiment Polarity Distribution')
    ax.set_xlabel('Sentiment Polarity')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)
    
    # Sentiment Count by Category
    st.subheader("Sentiment Distribution by App Category")
    sentiment_by_category = merged_df.groupby(['Category', 'Sentiment']).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(12, 6))
    sentiment_by_category.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title('Sentiment Count by Category')
    ax.set_xlabel('Category')
    ax.set_ylabel('Number of Sentiments')
    ax.legend(title='Sentiment')
    plt.xticks(rotation=90)
    st.pyplot(fig)
    
    # Sentiment Trends Over Time
    st.subheader("Sentiment Trends Over Update Years")
    sentiment_by_year = merged_df.groupby(['Update year', 'Sentiment']).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(10, 5))
    sentiment_by_year.plot(marker='o', ax=ax)
    ax.set_title('Sentiment Trends by Update Year')
    ax.set_xlabel('Update Year')
    ax.set_ylabel('Number of Sentiments')
    ax.legend(title='Sentiment')
    st.pyplot(fig)
    
    # Sentiment Polarity vs Rating
    st.subheader("Relationship between Sentiment Polarity and App Rating")
    avg_sentiment = merged_df.groupby('App')['Sentiment_Polarity'].mean().reset_index()
    playstore_sentiment = df_playstore.merge(avg_sentiment, on='App', how='left')
    
    fig, ax = plt.subplots(figsize=(10, 5))
    scatter = ax.scatter(
        playstore_sentiment['Rating'], 
        playstore_sentiment['Sentiment_Polarity'],
        s=playstore_sentiment['Installs']/1000000 + 10,
        alpha=0.6
    )
    ax.set_title('Sentiment Polarity vs Rating')
    ax.set_xlabel('Rating')
    ax.set_ylabel('Average Sentiment Polarity')
    st.pyplot(fig)
    
    # Subjectivity vs Polarity
    st.subheader("Sentiment Subjectivity vs Polarity")
    fig, ax = plt.subplots(figsize=(10, 5))
    scatter = ax.scatter(
        merged_df['Sentiment_Subjectivity'],
        merged_df['Sentiment_Polarity'],
        c=merged_df['Sentiment'].map({'Positive': 2, 'Neutral': 1, 'Negative': 0}),
        cmap='RdYlGn',
        alpha=0.6
    )
    ax.set_title('Sentiment Subjectivity vs Polarity')
    ax.set_xlabel('Sentiment Subjectivity')
    ax.set_ylabel('Sentiment Polarity')
    st.pyplot(fig)
    
    # Correlation Heatmap
    st.subheader("Correlation Analysis")
    numeric_cols = merged_df[['Rating', 'Reviews', 'Installs', 'Price', 'Sentiment_Polarity', 'Sentiment_Subjectivity']]
    correlation_matrix = numeric_cols.corr()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    ax.set_title('Correlation Matrix of Numerical Features')
    st.pyplot(fig)