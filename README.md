# 🎬 Movie Recommendation System

A content-based Movie Recommendation System built using **Natural
Language Processing (NLP)**, **Cosine Similarity**, **FastAPI**, and
**Streamlit**. The application recommends movies based on their
similarity to a movie selected by the user.

The project combines a recommendation engine, a dedicated backend API,
and an interactive frontend to deliver a complete movie recommendation
experience.

## 🌐 Live Demo

  ---------------------------------------------------------------------------------------------------------------
  Component                           Link
  ----------------------------------- ---------------------------------------------------------------------------
  🎬 Live Application                  https://intishar-project-movie-recommendation-system.streamlit.app

  ⚙️ Backend API                       https://movie-recommendation-system-7hn4.onrender.com

  ---------------------------------------------------------------------------------------------------------------

> Replace the two deployment URL placeholders with your actual links.

## 📌 Project Overview

This project uses a content-based filtering approach to recommend
movies. It processes movie-related textual information using NLP
techniques and calculates similarity scores with Cosine Similarity.

When a user selects a movie, the recommendation engine identifies other
movies with similar characteristics. Movie details and related
information are retrieved using TMDB.

## ✨ Key Features

-   **Content-based recommendations:** Suggests movies similar to the
    movie selected by the user.
-   **NLP-based processing:** Processes movie-related textual
    information for recommendation.
-   **Cosine Similarity:** Measures similarity between movie
    representations.
-   **FastAPI backend:** Handles API requests and recommendation
    operations.
-   **Streamlit interface:** Provides an interactive user experience.
-   **TMDB integration:** Retrieves movie information, posters, ratings,
    and other details.
-   **Cloud deployment:** Backend and frontend are deployed separately.

## 🛠️ Tech Stack

  -----------------------------------------------------------------------
  Technology                          Purpose
  ----------------------------------- -----------------------------------
  Python                              Core programming language

  Pandas & NumPy                      Data processing and numerical
                                      operations

  NLP                                 Text processing and feature
                                      analysis

  Scikit-learn                        Machine learning utilities and
                                      similarity calculations

  Cosine Similarity                   Measuring similarity between movies

  FastAPI                             Backend API development

  Uvicorn                             Running the backend server

  Streamlit                           Frontend development

  TMDB API                            Movie information and metadata

  Render                              Backend deployment

  Git & GitHub                        Version control and source code
                                      hosting
  -----------------------------------------------------------------------

## ⚙️ How It Works

1.  **Data preparation:** Movie-related information is collected and
    prepared for processing.
2.  **Text processing:** NLP techniques are applied to the textual
    features used by the recommendation engine.
3.  **Feature representation:** Movie information is represented in a
    form that can be compared.
4.  **Similarity calculation:** Cosine Similarity is used to calculate
    how closely movies are related.
5.  **Recommendation:** When a user selects a movie, the system finds
    movies with the highest similarity scores.
6.  **Information display:** TMDB is used to retrieve movie details and
    display relevant information in the frontend.

## 🏗️ System Architecture

The application is organized into three main components:

### Frontend --- Streamlit

-   Provides the interactive user interface.
-   Allows users to select movies.
-   Displays recommendations and movie information.

### Backend --- FastAPI

-   Handles incoming API requests.
-   Connects the frontend with the recommendation engine.
-   Returns recommendation results.

### Recommendation Engine --- NLP & Similarity

-   Processes movie-related textual features.
-   Calculates similarity scores.
-   Identifies movies similar to the selected title.

### Application Workflow

``` text
User
  |
  v
Streamlit Frontend
  |
  v
FastAPI Backend
  |
  v
Recommendation Engine
  |
  v
NLP / Feature Processing
  |
  v
Cosine Similarity
  |
  v
Recommended Movies
  |
  v
TMDB Movie Information
  |
  v
Results in Streamlit
```

## 📂 Project Structure

The repository contains the following main directories and files:

``` text
Movie-Recommendation-System/
├── app/              # Streamlit application
├── code/             # Backend and project code
├── data/             # Dataset and related data
├── models/           # Saved model assets
├── requirements.txt  # Python dependencies
├── .python-version   # Python version configuration
└── README.md
```

*This is a high-level overview. Refer to the repository for the exact
files and subdirectory structure.*

## 🚀 Getting Started

### Prerequisites

-   Python 3.11.9
-   Git
-   A TMDB API key, if required by the application configuration

### 1. Clone the repository

``` bash
git clone https://github.com/Intishar-Alam/Movie-Recommendation-System.git
cd Movie-Recommendation-System
```

### 2. Create a virtual environment

``` bash
python -m venv venv
```

Activate it:

**macOS / Linux**

``` bash
source venv/bin/activate
```

**Windows**

``` bash
venv\\Scripts\\activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Configure your TMDB API credentials using the variable names expected by
the application. Keep API keys private and do not commit them to GitHub.

### 5. Run the application

Start the FastAPI backend and Streamlit frontend using the appropriate
entry-point files in the repository. The exact commands depend on the
filenames and configuration in your project.

## ☁️ Deployment

The application is deployed using separate services:

  Component     Platform
  ------------- -----------
  Backend API   Render
  Frontend      Streamlit

The Streamlit frontend communicates with the FastAPI backend through API
requests.

## 📚 What I Learned

Working on this project helped me gain practical experience in:

-   Applying NLP techniques to real-world data.
-   Building a content-based recommendation system.
-   Using similarity-based methods to identify related items.
-   Developing REST APIs with FastAPI.
-   Connecting frontend and backend components.
-   Integrating an external API for movie metadata.
-   Deploying an application to cloud platforms.

## 🔮 Possible Future Improvements

-   Explore hybrid recommendation techniques.
-   Incorporate additional movie features to improve recommendations.
-   Add user preferences and personalized recommendations.
-   Optimize recommendation speed and API performance.
-   Experiment with more advanced NLP approaches.

## 🤝 Feedback & Contributions

Feedback, suggestions, and discussions are welcome.

If you find this project useful or interesting, consider giving the
repository a ⭐ on GitHub.

## 👨‍💻 Author

**Intishar Alam**\
Data Science Undergraduate \| Aspiring AI/ML Engineer

Interested in Machine Learning, Deep Learning, NLP, and Generative AI.

-   GitHub: [@Intishar-Alam](https://github.com/Intishar-Alam)
-   Project Repository: [Movie Recommendation
    System](https://github.com/Intishar-Alam/Movie-Recommendation-System)


