import pandas as pd
import streamlit as st
import pickle
import requests
import validate_email
import sqlite3



# Set page configuration
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=546b07c5b020b0206dc54a5bb6a9a6b0&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/original/" + data['poster_path']


def fetch_trailer(video):
    return "https://www.youtube.com/embed/{}".format(video)


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_movies_poster = []
    recommended_movies_trailer = []

    for i in movies_list:
        video = movies.iloc[i[0]].video[:][0]
        recommended_movies_trailer.append(video)

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        video = movies.iloc[i[0]].video[:][0]

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster, recommended_movies_trailer

# Load movie data
movie_dict = pickle.load(open('static/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

# Load similarity data
similarity = pickle.load(open('static/similarity.pkl', 'rb'))


st.markdown(
    """
    <style>
    :root {
        --primary-color: #FF5A5F;
        --background-color: #E9E0F9;
        --secondary-background-color: #F9F9F9;
        --text-color: #707070;
        --font: Arial, sans-serif;
    }
    
    .title {
        color: var(--primary-color);
        text-align: center;
        font-size: 48px;
        margin-bottom: 1.5em;
        text-shadow: 2px 2px #FCDADA;
        font-family: var(--font);
    }
    
    .subtitle {
        text-align: center;
        font-size: 24px;
        margin-bottom: 2em;
        color: var(--text-color);
        font-family: var(--font);
    }
    
    body {
        background-color: var(--background-color);
        background-image: url('background_image.jpg');
        background-repeat: no-repeat;
        background-size: cover;
        margin: 0;
        padding: 0;
    }
    
    .recommendation {
        background-color: var(--secondary-background-color);
        padding: 1.5em;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5em;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    
    .movie-title {
        font-size: 15px;
        font-weight: bold;
        color: var(--primary-color);
        margin-top: 1.0em;
        margin-bottom: 0.5em;
        font-family: var(--font);
    }
    
    .movie-poster {
        width: 250px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
        cursor: pointer;
    }
    
    .movie-poster:hover {
        transform: scale(1.05);
    }
    
    .movie-trailer {
        width: 100%;
        height: 200px;
        border-radius: 10px;
        margin-top: 0.5em;
    }
    
    footer {
        text-align: center;
        margin-top: 2em;
        color: var(--text-color);
        font-family: var(--font);
    }
    
    footer a {
        color: var(--primary-color);
        text-decoration: none;
    }
    
    footer a:hover {
        text-decoration: underline;
    }
    
    .footer-content {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .footer-icon {
        margin-right: 0.5em;
    }
    
    @media only screen and (max-width: 768px) {
        body {
            padding: 0 20px;
        }
        
        .recommendation {
            padding: 1em;
        }
        
        .movie-poster {
            width: 150px;
        }
        
        .movie-trailer {
            height: 150px;
        }
    }
    
    </style>
    """,
    unsafe_allow_html=True
)

# Define the page variable with a default value
page = "Home"

# Sidebar navigation
st.sidebar.title("Navigation")

# Add the selectbox to the sidebar
selected_page = st.sidebar.selectbox(
    "Go to",
    ["Home", "About Us", "Contact Us", "View Records"],
    index=0,
    format_func=lambda x: f"• {x}"
)

# Update the page variable based on the selected page
if selected_page:
    page = selected_page


# Home page
if page == "Home":
    st.title("  ")
    st.write("  ")
    col1, col2= st.columns(2)
    with col1:
        st.title("Welcome to Movie Recommender System!")
        st.write("Select a movie from the dropdown on the left and click 'Recommend' to get personalized movie recommendations.")

    with col2:  
        st.image("images/index2.png", width=600)
    
    selected_movie_name = st.selectbox(
        "Select a movie:",
        movies['title'].values,
        key="movie-selection"
    )
    
    if st.button('Recommend', key="recommend-button"):
        names, posters, trailers = recommend(selected_movie_name)

        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]

        for i in range(10):
            with cols[i % 5]:
                st.markdown(
                    f"""
                    <div class="recommendation">
                        <a href="{fetch_trailer(trailers[i])}" target="_blank">
                            <img class="movie-poster" src="{posters[i]}" alt="{names[i]} Poster">
                        </a>
                        <p class="movie-title">{names[i]}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# About Us page
elif page == "About Us":
    st.title("About Us")
    st.write("Learn more about us!")

    
    col1, col2 = st.columns(2)
    with col1:
        st.image("images/person2.jpg", width=250)
    with col2:
        st.markdown("<h3 style='text-align: center;'>Prabhakar Pal</h3>", unsafe_allow_html=True)
        st.write("Fetched 15,000 movie data from TMDB website and stored it in a data frame.")
        st.write("Cleaned and preprocessed the data.")
        st.write("Built a recommender model using machine learning concepts.")
        st.markdown("[LinkedIn](https://www.linkedin.com/in/prabhakarpal/) [GitHub](https://github.com/1prabhakarpal) <i class='fab fa-linkedin'></i><i class='fab fa-github'></i>", unsafe_allow_html=True)




# Contact Us page
if page == "Contact Us":
    st.title("Contact Us")
    st.write("Contact us for any inquiries or feedback!")

    # Database connection
    conn = sqlite3.connect('contact_us.db')

    # Create a table if it doesn't exist
    conn.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    ''')

    # Contact form
    with st.form(key='contact-form'):
        st.subheader("Send us a message")

        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message")

        form_warning = st.empty()

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if not name:
                form_warning.warning("Please enter your name.")
            elif not email:
                form_warning.warning("Please enter your email.")
            elif not validate_email.validate_email(email):
                form_warning.warning("Please enter a valid email address.")
            elif not message:
                form_warning.warning("Please enter your message.")
            else:
                # Insert the form data into the database
                conn.execute('''
                    INSERT INTO contact_messages (name, email, message)
                    VALUES (?, ?, ?)
                ''', (name, email, message))

                # Commit the transaction
                conn.commit()
                

                # Close the database connection
                conn.close()

                # Display success message
                st.success("Thank you for your message! We'll get back to you soon.")

# View Records page
elif page == "View Records":
    st.title("View Records")

    # Login form
    st.subheader("Login")
    login_id = st.text_input("Login ID")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        # Perform login authentication
        if login_id == "admin" and password == "password":
            # Fetch records from the database
            conn = sqlite3.connect('contact_us.db')
            cursor = conn.execute('SELECT * FROM contact_messages')
            records = cursor.fetchall()

            # Display the records in a table
            st.subheader("Records")

            # Create a DataFrame from the records
            df = pd.DataFrame(records, columns=['ID', 'Name', 'Email', 'Message'])

            # Set up table styling
            table_style = """
                <style>
                    .styled-table {
                        width: 100%;
                        border-collapse: collapse;
                        margin: 20px 0;
                        font-size: 0.9em;
                        font-family: Arial, sans-serif;
                    }
                    .styled-table thead tr {
                        background-color: #f5f5f5;
                        color: #000;
                        text-align: left;
                    }
                    .styled-table th,
                    .styled-table td {
                        padding: 12px 15px;
                    }
                    .styled-table tbody tr {
                        border-bottom: 1px solid #ddd;
                    }
                    .styled-table tbody tr:nth-of-type(even) {
                        background-color: #f9f9f9;
                    }
                    .styled-table tbody tr:last-of-type {
                        border-bottom: 2px solid #000;
                    }
                    .styled-table td:nth-child(3) {
                        width: 20%;
                    }
                    .styled-table td:nth-child(4) {
                        width: 40%;
                    }
                </style>
            """
            st.write(table_style, unsafe_allow_html=True)

            # Display the DataFrame as a table with styling
            st.table(df[['Name', 'Email', 'Message']].style
                      .set_table_attributes("class='styled-table'")
                      .set_properties(subset=['Name'], width='300px')
                      .set_properties(subset=['Email'], width='300px')
                      .set_properties(subset=['Message'], width='1000px'))

            # Close the database connection
            conn.close()
        else:
            st.error("Invalid login credentials. Please try again.")


# Add Footer HTML and CSS
footer_html = """
<footer>
    <div class="footer-content">
        <p>Created by <a href="https://www.linkedin.com/in/prabhakarpal/">Prabhakar Pal</a></p>
    </div>
</footer>
"""

st.markdown(footer_html, unsafe_allow_html=True)