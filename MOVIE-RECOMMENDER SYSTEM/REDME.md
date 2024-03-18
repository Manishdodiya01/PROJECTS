# Movie Recommendation System

# Get similarity.pkl from notebook Movie_recommender_system.ipynb

A simple movie recommendation system based on collaborative filtering using Streamlit, Python, and the MovieLens dataset.

## Overview

This project implements a movie recommendation system using collaborative filtering techniques. It suggests similar movies based on user input using a precomputed similarity matrix.

## Features

- **Search for a Movie:** Users can search for a movie by its title.
- **Display Recommendations:** Upon entering a movie title and clicking the "Show Recommendation" button, the system displays similar movie recommendations along with their posters.
- **Clickable Posters:** Users can click on the movie posters to view more information about each movie on IMDb.
- **Caching:** The system caches API requests to improve performance.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your_username/movie-recommendation-system.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

## Data Sources

- **MovieLens Dataset:** The project uses the MovieLens dataset for movie information and ratings.

## File Structure

- **app.py:** Main Streamlit application file.
- **movie_list.pkl:** Pickled file containing movie information.
- **similarity.pkl:** Pickled file containing the similarity matrix.
- **requirements.txt:** File containing dependencies.

## Technologies Used

- Python
- Streamlit
- Requests
- Pandas
- Pickle
- Cachetools

## Contributors

- Your Name

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
