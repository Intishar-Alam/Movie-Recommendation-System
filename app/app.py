import os

import httpx
import streamlit as st

# =========================
# CONFIG
# =========================
API_BASE = os.getenv("API_BASE", "https://movie-recommendation-system-fk1g.onrender.com")
PLACEHOLDER = "https://via.placeholder.com/500x750?text=No+Poster"

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

st.markdown(
    """
    <style>
    .block-container {padding-top: 1.5rem;}
    .movie-title {font-weight: 600; font-size: 0.9rem; margin-top: 0.3rem;}
    .movie-meta {color: #9aa0a6; font-size: 0.8rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# STATE
# =========================
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_id" not in st.session_state:
    st.session_state.selected_id = None


def open_movie(tmdb_id: int):
    st.session_state.selected_id = tmdb_id
    st.session_state.view = "details"


def go_home():
    st.session_state.view = "home"
    st.session_state.selected_id = None


# =========================
# API HELPERS
# =========================
@st.cache_data(ttl=300, show_spinner=False)
def api_get(path: str, params: tuple = ()):
    """Returns (data, error). Params are a tuple of pairs so they're hashable for caching."""
    try:
        r = httpx.get(f"{API_BASE}{path}", params=dict(params), timeout=60)
        if r.status_code != 200:
            try:
                detail = r.json().get("detail", r.text)
            except Exception:
                detail = r.text
            return None, f"{r.status_code}: {detail}"
        return r.json(), None
    except httpx.RequestError as e:
        return None, f"Cannot reach backend at {API_BASE} ({type(e).__name__})"


def get(path: str, **params):
    return api_get(path, tuple(sorted(params.items())))


# =========================
# UI COMPONENTS
# =========================
def poster_grid(cards: list, cols_per_row: int = 6, key_prefix: str = "grid"):
    if not cards:
        st.info("Nothing to show.")
        return

    for row_start in range(0, len(cards), cols_per_row):
        cols = st.columns(cols_per_row)
        for col, card in zip(cols, cards[row_start : row_start + cols_per_row]):
            with col:
                st.image(card.get("poster_url") or PLACEHOLDER, use_container_width=True)
                st.markdown(
                    f"<div class='movie-title'>{card.get('title', '')}</div>",
                    unsafe_allow_html=True,
                )
                year = (card.get("release_date") or "")[:4]
                rating = card.get("vote_average")
                meta = " • ".join(
                    x for x in [year, f"⭐ {rating:.1f}" if rating else ""] if x
                )
                st.markdown(f"<div class='movie-meta'>{meta}</div>", unsafe_allow_html=True)
                st.button(
                    "View",
                    key=f"{key_prefix}_{card['tmdb_id']}_{row_start}",
                    on_click=open_movie,
                    args=(card["tmdb_id"],),
                    use_container_width=True,
                )


def normalize_search_results(results: list) -> list:
    """Convert raw TMDB search results into card-shaped dicts."""
    cards = []
    for m in results:
        poster = m.get("poster_path")
        cards.append(
            {
                "tmdb_id": m["id"],
                "title": m.get("title") or "",
                "poster_url": f"https://image.tmdb.org/t/p/w500{poster}" if poster else None,
                "release_date": m.get("release_date"),
                "vote_average": m.get("vote_average"),
            }
        )
    return cards


# =========================
# VIEWS
# =========================
def render_home():
    st.title("🎬 Movie Recommender")

    with st.sidebar:
        st.header("Browse")
        category = st.selectbox(
            "Category",
            ["trending", "popular", "top_rated", "upcoming", "now_playing"],
            format_func=lambda x: x.replace("_", " ").title(),
        )
        grid_cols = st.slider("Posters per row", 3, 8, 6)

    query = st.text_input("🔍 Search for a movie", placeholder="e.g. Inception, Avengers...")

    if query.strip():
        with st.spinner("Searching..."):
            data, err = get("/tmdb/search", query=query.strip(), page=1)
        if err:
            st.error(err)
            return
        cards = normalize_search_results(data.get("results", []))
        st.subheader(f"Results for “{query}”")
        if not cards:
            st.warning("No movies found.")
        else:
            poster_grid(cards, grid_cols, key_prefix="search")
        return

    with st.spinner("Loading movies..."):
        cards, err = get("/home", category=category, limit=36)
    if err:
        st.error(err)
        return
    st.subheader(category.replace("_", " ").title())
    poster_grid(cards, grid_cols, key_prefix="home")


def render_details():
    st.button("← Back", on_click=go_home)

    tmdb_id = st.session_state.selected_id
    details, err = get(f"/movie/id/{tmdb_id}")
    if err:
        st.error(err)
        return

    if details.get("backdrop_url"):
        st.image(details["backdrop_url"], use_container_width=True)

    left, right = st.columns([1, 2])
    with left:
        st.image(details.get("poster_url") or PLACEHOLDER, use_container_width=True)
    with right:
        st.title(details["title"])
        if details.get("release_date"):
            st.caption(f"Release date: {details['release_date']}")
        genres = [g["name"] for g in details.get("genres", [])]
        if genres:
            st.write(" • ".join(f"`{g}`" for g in genres))
        st.write(details.get("overview") or "No overview available.")

    st.divider()

    with st.spinner("Finding recommendations..."):
        bundle, err = get(
            "/movie/search",
            query=details["title"],
            tfidf_top_n=12,
            genre_limit=12,
        )
    if err:
        st.warning(f"Could not load recommendations: {err}")
        return

    st.subheader("🧠 Similar movies (content-based, TF-IDF)")
    tfidf_cards = []
    for item in bundle.get("tfidf_recommendations", []):
        tmdb = item.get("tmdb")
        if tmdb:  # only show items we found a TMDB match for
            tfidf_cards.append(tmdb)
    if tfidf_cards:
        poster_grid(tfidf_cards, 6, key_prefix="tfidf")
    else:
        st.info("No content-based recommendations found (title may not be in the local dataset).")

    st.divider()
    st.subheader("🎭 More from the same genre")
    poster_grid(bundle.get("genre_recommendations", []), 6, key_prefix="genre")


# =========================
# ROUTER
# =========================
if st.session_state.view == "details" and st.session_state.selected_id:
    render_details()
else:
    render_home()