# Movie Recommender

A content-based movie recommendation app built with Streamlit. Choose a movie
to see five recommendations based on similarities in its overview, genres,
keywords, cast, and crew.

Movie features are combined and vectorized in the included notebook, then
compared using cosine similarity. The app loads the resulting precomputed
data files and uses The Movie Database (TMDB) API to retrieve posters.

## Project files

- `app.py` - Streamlit application.
- `MovieRecommender.ipynb` - notebook that prepares movie features, computes
  similarities, and saves the recommender data.
- `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` - source movie data used
  by the notebook.
- `movie_list.pkl` and `similarity.pkl` - precomputed movie data and
  similarity scores used by the app.

## Run the app

Use Python 3 and run these commands from the project directory in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install streamlit requests pandas numpy
```

TMDB posters are optional. To enable them, set your TMDB API key for the
current PowerShell session:

```powershell
$env:TMDB_API_KEY = "your_tmdb_api_key"
```

Then start the app:

```powershell
streamlit run app.py
```

Without a TMDB API key, the app still provides recommendations and displays a
placeholder image instead of movie posters.

## Rebuild the recommender data

To regenerate `movie_list.pkl` and `similarity.pkl`, install the notebook
dependencies and run the notebook:

```powershell
python -m pip install jupyter numpy pandas scikit-learn nltk
jupyter notebook MovieRecommender.ipynb
```

Run the notebook cells in order. Keep both CSV files in the project directory;
the notebook writes the generated pickle files there for the app to load.
