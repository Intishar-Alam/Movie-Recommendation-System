import html

import httpx
import streamlit as st

API_BASE = "https://movie-recommendation-system-fk1g.onrender.com" or "http://127.0.0.1:8000"
IMG_500 = "https://image.tmdb.org/t/p/w500"
NO_POSTER = "https://placehold.co/500x750/1D2029/8E93A0?text=No+poster"

CATEGORIES = {
    "Popular": "popular",
    "Trending": "trending",
    "Top rated": "top_rated",
    "Upcoming": "upcoming",
    "Now playing": "now_playing",
}

st.set_page_config(
    page_title="Matinee",
    page_icon="🎞️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------------------
# Styling
# ink #14161C, panel #1D2029, paper #ECE8E1, mist #8E93A0, marquee #E9B44C
# ----------------------------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=DM+Sans:wght@400;500;700&display=swap');

html, body, [class*="css"], .stApp, .stMarkdown, button, input {
    font-family: 'DM Sans', system-ui, sans-serif;
}
.stApp { background: #14161C; color: #ECE8E1; }
header[data-testid="stHeader"], #MainMenu, footer { display: none; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1400px; }

.brand {
    font-family: 'Fraunces', serif;
    font-weight: 700;
    font-size: 2rem;
    letter-spacing: -0.02em;
    color: #ECE8E1;
    line-height: 2.6rem;
}
.brand span { color: #E9B44C; }

.stTextInput input {
    background: #1D2029;
    border: 1px solid #2A2E3A;
    border-radius: 999px;
    color: #ECE8E1;
    padding: 0.7rem 1.2rem;
}
.stTextInput input:focus { border-color: #E9B44C; box-shadow: none; }

.section-title {
    font-family: 'Fraunces', serif;
    font-weight: 500;
    font-size: 1.5rem;
    margin: 2.2rem 0 1rem;
    color: #ECE8E1;
}

div[data-testid="stImage"] img {
    border-radius: 10px;
    aspect-ratio: 2 / 3;
    object-fit: cover;
    background: #1D2029;
}
.mtitle {
    font-weight: 500;
    font-size: 0.95rem;
    margin-top: 0.5rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.meta { color: #8E93A0; font-size: 0.82rem; display: flex; gap: 0.8rem; margin: 0.15rem 0 0.4rem; }
.meta .match { color: #E9B44C; font-weight: 500; }

.stButton > button {
    background: transparent;
    color: #ECE8E1;
    border: 1px solid #2A2E3A;
    border-radius: 8px;
    padding: 0.25rem 0.5rem;
    transition: border-color 0.15s, color 0.15s;
}
.stButton > button:hover { border-color: #E9B44C; color: #E9B44C; }
.stButton > button:focus-visible { outline: 2px solid #E9B44C; outline-offset: 2px; }

.hero {
    border-radius: 16px;
    padding: 4.5rem 3rem;
    min-height: 380px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    background-size: cover;
    background-position: center top;
    margin: 0.5rem 0 0.5rem;
}
.hero h1 {
    font-family: 'Fraunces', serif;
    font-weight: 700;
    font-size: clamp(2rem, 5vw, 3.6rem);
    letter-spacing: -0.02em;
    line-height: 1.05;
    margin: 0 0 0.8rem;
    max-width: 18ch;
}
.hero .facts { color: #C9C5BD; font-size: 0.95rem; display: flex; gap: 1rem; margin-bottom: 0.9rem; }
.hero .facts .star { color: #E9B44C; }
.chips { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1.1rem; }
.chip { border: 1px solid #4A4F5E; border-radius: 999px; padding: 0.15rem 0.8rem; font-size: 0.85rem; color: #ECE8E1; }
.hero p { max-width: 62ch; line-height: 1.6; color: #D8D4CC; margin: 0; }

.note { color: #8E93A0; font-size: 0.95rem; margin: 0.5rem 0 1rem; }

div[data-testid="stPills"] button[aria-checked="true"],
div[data-testid="stPills"] button[aria-pressed="true"] {
    background: #E9B44C; color: #14161C; border-color: #E9B44C;
}
</style>
""",
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------------
# API access
# ----------------------------------------------------------------------------
@st.cache_data(ttl=300, show_spinner=False)
def _get(path: str, params_items: tuple):
    r = httpx.get(f"{API_BASE}{path}", params=dict(params_items), timeout=60)
    r.raise_for_status()
    return r.json()


def get(path: str, **params):
    """Cached GET. Returns None (and shows a message) if the call fails."""
    try:
        return _get(path, tuple(sorted(params.items())))
    except httpx.HTTPError as e:
        st.error(
            f"Couldn't load data from the API ({e}). "
            f"Check that the FastAPI server is running at {API_BASE}."
        )
        return None


# ----------------------------------------------------------------------------
# Normalising the different response shapes into one dict
# ----------------------------------------------------------------------------
def from_tmdb_raw(m: dict) -> dict:
    p = m.get("poster_path")
    return {
        "id": m["id"],
        "title": m.get("title") or "",
        "poster": f"{IMG_500}{p}" if p else None,
        "date": m.get("release_date"),
        "rating": m.get("vote_average"),
        "score": None,
    }


def from_card(c: dict, score: float | None = None) -> dict:
    return {
        "id": c["tmdb_id"],
        "title": c.get("title") or "",
        "poster": c.get("poster_url"),
        "date": c.get("release_date"),
        "rating": c.get("vote_average"),
        "score": score,
    }


# ----------------------------------------------------------------------------
# State
# ----------------------------------------------------------------------------
st.session_state.setdefault("selected", None)
st.session_state.setdefault("last_query", "")


def open_movie(movie_id: int):
    st.session_state.selected = movie_id


def close_movie():
    st.session_state.selected = None


# ----------------------------------------------------------------------------
# Components
# ----------------------------------------------------------------------------
def poster_grid(movies: list[dict], prefix: str, per_row: int = 6):
    for start in range(0, len(movies), per_row):
        cols = st.columns(per_row)
        for offset, (col, m) in enumerate(zip(cols, movies[start : start + per_row])):
            with col:
                st.image(m["poster"] or NO_POSTER, use_container_width=True)
                bits = []
                if m["date"]:
                    bits.append(f"<span>{html.escape(m['date'][:4])}</span>")
                if m["rating"]:
                    bits.append(f"<span>★ {m['rating']:.1f}</span>")
                if m["score"] is not None:
                    bits.append(f"<span class='match'>{round(m['score'] * 100)}% match</span>")
                st.markdown(
                    f"<div class='mtitle' title='{html.escape(m['title'])}'>{html.escape(m['title'])}</div>"
                    f"<div class='meta'>{''.join(bits)}</div>",
                    unsafe_allow_html=True,
                )
                st.button(
                    "View",
                    key=f"{prefix}_{m['id']}_{start + offset}",
                    on_click=open_movie,
                    args=(m["id"],),
                    use_container_width=True,
                )


def section(title: str):
    st.markdown(f"<div class='section-title'>{html.escape(title)}</div>", unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# Pages
# ----------------------------------------------------------------------------
def home_page():
    choice = st.radio(
        "Browse",
        options=list(CATEGORIES),
        index=list(CATEGORIES).index("Popular"),
        horizontal=True,
        label_visibility="collapsed"
    )
    choice = choice or "Popular"
    data = get("/home", category=CATEGORIES[choice], limit=24)
    if data is None:
        return
    section(choice)
    poster_grid([from_card(c) for c in data], prefix=f"home_{choice}")


def search_page(query: str):
    data = get("/tmdb/search", query=query, page=1)
    if data is None:
        return
    results = [from_tmdb_raw(m) for m in data.get("results", []) if m.get("id")]
    section(f"Results for “{query}”")
    if not results:
        st.markdown(
            "<div class='note'>No movies matched. Try a shorter or different title.</div>",
            unsafe_allow_html=True,
        )
        return
    poster_grid(results, prefix="search")


def detail_page(movie_id: int):
    st.button("Back to browse", on_click=close_movie, key="back")

    d = get(f"/movie/id/{movie_id}")
    if d is None:
        return

    genres = d.get("genres") or d.get("genre") or []
    genre_names = [g.get("name", "") for g in genres if g.get("name")]
    backdrop = d.get("backdrop_url") or d.get("poster_url") or ""
    year = (d.get("release_date") or "")[:4]

    facts = f"<span>{html.escape(year)}</span>" if year else ""
    chips = "".join(f"<span class='chip'>{html.escape(n)}</span>" for n in genre_names)
    overview = html.escape(d.get("overview") or "No overview available.")
    bg = (
        "linear-gradient(90deg, #14161C 12%, rgba(20,22,28,0.7) 55%, rgba(20,22,28,0.25) 100%)"
        + (f", url('{html.escape(backdrop, quote=True)}')" if backdrop else "")
    )

    st.markdown(
        f"""
        <div class="hero" style="background-image: {bg}; background-color:#1D2029;">
            <h1>{html.escape(d['title'])}</h1>
            <div class="facts">{facts}</div>
            <div class="chips">{chips}</div>
            <p>{overview}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # The recommendation models run here, only once a movie has been opened.
    with st.spinner("Finding movies you might like"):
        bundle = get("/movie/search", query=d["title"], tfidf_top_n=12, genre_limit=12)
    if bundle is None:
        return

    tfidf_raw = bundle.get("tfidf_recommendations") or bundle.get("tfidf_reccomendation") or []
    genre_raw = bundle.get("genre_recommendations") or bundle.get("genre_reccomendation") or []

    tfidf_cards = [
        from_card(item["tmdb"], score=item.get("score"))
        for item in tfidf_raw
        if item.get("tmdb")
    ]

    if tfidf_cards:
        section("More like this")
        poster_grid(tfidf_cards, prefix="tfidf")
    else:
        st.markdown(
            "<div class='note'>This title isn't in the recommendation dataset, "
            "so only genre picks are shown.</div>",
            unsafe_allow_html=True,
        )

    if genre_raw:
        label = genre_names[0] if genre_names else "this genre"
        section(f"Popular in {label}")
        poster_grid([from_card(c) for c in genre_raw], prefix="genre")


# ----------------------------------------------------------------------------
# Layout
# ----------------------------------------------------------------------------
left, right = st.columns([1, 2], vertical_alignment="center")
with left:
    st.markdown("<div class='brand'>Matinee<span>.</span></div>", unsafe_allow_html=True)
with right:
    query = st.text_input(
        "Search",
        placeholder="Search for a movie",
        label_visibility="collapsed",
    ).strip()

# A new search always takes you out of a movie page.
if query != st.session_state.last_query:
    st.session_state.last_query = query
    st.session_state.selected = None

if st.session_state.selected:
    detail_page(st.session_state.selected)
elif query:
    search_page(query)
else:
    home_page()