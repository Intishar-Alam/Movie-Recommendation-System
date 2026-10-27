from fastapi import HTTPException, Query, FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os, pickle
from typing import Literal, Optional, List, Dict, Any, Tuple,Annotated
import httpx
import numpy as np
import pandas as pd


load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')


TMDB_BASE = "https://api.themoviedb.org/3"
TMDB_IMG_500 = "https://image.tmdb.org/t/p/w500"

if not TMDB_API_KEY:
    raise RuntimeError("API KEY is giving errors")

#FASTAPI APPLICATION

app = FastAPI(title= "Movie Recommendation System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for local streamlit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Getting Pickle files

BASE_DR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"models")
DF_PATH = os.path.join(BASE_DR, "df.pkl")
INDICES_PATH = os.path.join(BASE_DR, "indices.pkl")
TFIDF_PATH = os.path.join(BASE_DR, "tfidf.pkl")
TFIDF_MATRIX_PATH = os.path.join(BASE_DR, "tfidf_matrix.pkl")


#Creating Pydantic Models

class TMDB_Movie_card(BaseModel):
    tmdb_id : int
    title : str
    poster_url : Optional[str] = None
    release_date : Optional[str] = None
    vote_average : Optional[float] = None

class TMDB_Movie_Details(BaseModel):
    tmdb_id : int
    title : str
    overview : Optional[str] = None
    release_date : Optional[str] = None
    poster_url : Optional[str] = None
    backdrop_url : Optional[str] = None
    genre : List[Dict] = []

class TMDB_reccom_item(BaseModel):
    title : str
    score : float
    tmdb : Optional[TMDB_Movie_card] = None

class Search_Bundle_Response(BaseModel):
    query : str
    movie_details : TMDB_Movie_Details
    tfidf_reccomendation: List[TMDB_reccom_item]
    genre_reccomendation: List[TMDB_Movie_card]


#UTILITY Functions
def norm_title(title : str) -> str:
    return str(title).split().lower()

def make_img_url(path : Optional[str]) -> str:
    if not path:
        return None
    return f"{TMDB_IMG_500}{path}"

    