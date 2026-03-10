import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="U.S. Alcohol Consumption Trends(1977-2023)",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# DESIGN TOKENS
# ─────────────────────────────────────────────
PLOT_BG    = "#0d1117"
PAPER_BG   = "#0d1117"
FONT_COLOR = "#e6edf3"
GRID_COLOR = "#21262d"
BORDER     = "#30363d"

AMBER  = "#f0a500"
TEAL   = "#00b4d8"
SAGE   = "#7bc47f"
ROSE   = "#f06292"
VIOLET = "#b39ddb"
CORAL  = "#ff7043"

PALETTE = [AMBER, TEAL, SAGE, ROSE, VIOLET, CORAL]

REGION_COLOR = {
    "Midwest Region":   TEAL,
    "Northeast Region": AMBER,
    "South Region":     SAGE,
    "West Region":      ROSE,
}

def plot_layout(title="", height=420, legend=True):
    return dict(
        title=dict(
            text=title,
            font=dict(family="Georgia, serif", size=17, color=FONT_COLOR),
            x=0.01, y=0.97
        ),
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(family="DM Sans, sans-serif", color=FONT_COLOR, size=12),
        height=height,
        margin=dict(l=50, r=30, t=55, b=45),
        xaxis=dict(gridcolor=GRID_COLOR, linecolor=BORDER, tickcolor=BORDER,
                   showgrid=True, zeroline=False),
        yaxis=dict(gridcolor=GRID_COLOR, linecolor=BORDER, tickcolor=BORDER,
                   showgrid=True, zeroline=False),
        hoverlabel=dict(bgcolor="#161b22", bordercolor=BORDER,
                        font=dict(color=FONT_COLOR, size=12)),
        showlegend=legend,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11),
                    bordercolor=BORDER, borderwidth=1)
    )

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display:ital@0;1&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0d1117;
    color: #e6edf3;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #111827 100%);
    border-right: 1px solid #21262d;
}
[data-testid="stSidebar"] * { color: #c9d1d9 !important; }
.chapter-tag {
    display: inline-block;
    background: #f0a500;
    color: #0d1117;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 2px;
    margin-bottom: 0.5rem;
}
.page-headline {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    font-weight: 400;
    color: #e6edf3;
    line-height: 1.15;
    margin: 0.2rem 0 0.8rem 0;
}
.page-deck {
    font-size: 1.0rem;
    color: #374151;
    font-weight: 300;
    line-height: 1.6;
    max-width: 720px;
    margin-bottom: 1.5rem;
}
.section-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #f0a500;
    margin: 2rem 0 0.4rem 0;
}
.story-box {
    background: #161b22;
    border: 1px solid #21262d;
    border-left: 3px solid #f0a500;
    border-radius: 6px;
    padding: 1.1rem 1.4rem;
    margin: 0.6rem 0 1.6rem 0;
    color: #c9d1d9;
    font-size: 0.93rem;
    line-height: 1.72;
}
.story-box strong { color: #e6edf3; }
.stat-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 1.1rem 1.2rem;
    text-align: center;
}
.stat-num {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem;
    color: #f0a500;
    line-height: 1;
}
.stat-lbl {
    font-size: 0.72rem;
    color: #6e7681;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.35rem;
}
.quest-phase {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
}
.quest-letter {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem;
    color: #f0a500;
    float: left;
    margin-right: 0.8rem;
    line-height: 1;
}
.quest-title {
    font-size: 1.0rem;
    font-weight: 600;
    color: #e6edf3;
    margin-bottom: 0.3rem;
}
.quest-body { font-size: 0.88rem; color: #8b949e; line-height: 1.65; clear: both; }
.divider { border: none; border-top: 1px solid #21262d; margin: 1.4rem 0; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# STATE ABBREVIATION MAP
# ─────────────────────────────────────────────
ABBREV = {
    'alabama':'AL','alaska':'AK','arizona':'AZ','arkansas':'AR','california':'CA',
    'colorado':'CO','connecticut':'CT','delaware':'DE','district of columbia':'DC',
    'florida':'FL','georgia':'GA','hawaii':'HI','idaho':'ID','illinois':'IL',
    'indiana':'IN','iowa':'IA','kansas':'KS','kentucky':'KY','louisiana':'LA',
    'maine':'ME','maryland':'MD','massachusetts':'MA','michigan':'MI','minnesota':'MN',
    'mississippi':'MS','missouri':'MO','montana':'MT','nebraska':'NE','nevada':'NV',
    'new hampshire':'NH','new jersey':'NJ','new mexico':'NM','new york':'NY',
    'north carolina':'NC','north dakota':'ND','ohio':'OH','oklahoma':'OK','oregon':'OR',
    'pennsylvania':'PA','rhode island':'RI','south carolina':'SC','south dakota':'SD',
    'tennessee':'TN','texas':'TX','utah':'UT','vermont':'VT','virginia':'VA',
    'washington':'WA','west virginia':'WV','wisconsin':'WI','wyoming':'WY'
}

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data
def load():
    df = pd.read_csv("niaaa_apparent_per_capita_consumption_1977_2023.csv")
    non_states = ['Midwest Region','Northeast Region','South Region','West Region','Us Total']
    s = df[~df['state_name'].isin(non_states)].copy()
    s['abbrev'] = s['state'].map(ABBREV)
    u = df[df['state_name'] == 'Us Total'].copy()
    r = df[df['state_name'].isin(['Midwest Region','Northeast Region','South Region','West Region'])].copy()
    return df, s, u, r

df, states_df, us_df, regions_df = load()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Navigation")
    st.markdown("---")
    nav = st.radio("", [
        "Introduction",
        "Chapter 1 — The National Arc",
        "Chapter 2 — A Nation Divided",
        "Chapter 3 — What America Drinks",
        "Chapter 4 — The COVID Shock",
        "Chapter 5 — Regions & States",
        "QUEST Framework",
        "Data Source"
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**Year Range**")
    yr = st.slider("", 1977, 2023, (1977, 2023), key="yr")

    st.markdown("**Compare States**")
    all_states = sorted(states_df["state_name"].unique())
    sel_states = st.multiselect("", all_states,
        default=["New Hampshire","Utah","Nevada","New York","Texas","California"],
        key="sel")

    st.markdown("---")
    st.markdown('<p style="font-size:0.7rem;color:#4a5568;">NIAAA Surveillance Data<br>1977-2023</p>',
                unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FILTERED SLICES
# ─────────────────────────────────────────────
y0, y1 = yr
us_f  = us_df[(us_df["year"] >= y0) & (us_df["year"] <= y1)]
st_f  = states_df[(states_df["year"] >= y0) & (states_df["year"] <= y1)]
reg_f = regions_df[(regions_df["year"] >= y0) & (regions_df["year"] <= y1)]

latest = us_df[us_df["year"] == 2023].iloc[0]
peak   = us_df.loc[us_df["ethanol_all_drinks_gallons_per_capita"].idxmax()]

# ══════════════════════════════════════════════════════════════
# INTRODUCTION
# ══════════════════════════════════════════════════════════════
if nav == "Introduction":
    st.markdown('<h1 class="page-headline">U.S. Alcohol Consumption Trends<br><em style="color:#c8922a;">47 Years of Drinking Patterns(1977-2023)</em></h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-deck">This dashboard shows how drinking habits in the United States have changed from 1977 to 2023. It highlights how much people drink, the types of alcohol they prefer, and how these patterns shift over time. The data reflects the influence of cultural trends, public policies, and major events like the COVID-19 pandemic, showing how American drinking preferences have gradually evolved.</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="stat-card"><div class="stat-num">{latest["ethanol_all_drinks_gallons_per_capita"]:.2f}</div><div class="stat-lbl">Gallons per capita 2023</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-card"><div class="stat-num">{int(peak["year"])}</div><div class="stat-lbl">Peak consumption year</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="stat-card"><div class="stat-num">3.2x</div><div class="stat-lbl">NH drinks vs Utah</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="stat-card"><div class="stat-num">2022</div><div class="stat-lbl">Spirits overtook beer</div></div>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col_a, col_b = st.columns([1.15, 1])
    with col_a:
        st.markdown('<p class="section-label">The big picture</p>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=us_df["year"], y=us_df["ethanol_all_drinks_gallons_per_capita"],
            mode="lines", line=dict(color=AMBER, width=2.8),
            fill="tozeroy", fillcolor="rgba(240,165,0,0.07)",
            hovertemplate="<b>%{x}</b> — %{y:.2f} gal/capita<extra></extra>"
        ))
        fig.add_vline(x=1981, line_dash="dash", line_color="#444c56", line_width=1.2,
                      annotation_text="1981 Peak", annotation_font_color="#8b949e",
                      annotation_font_size=10)
        fig.add_vline(x=2020, line_dash="dash", line_color=TEAL, line_width=1.2,
                      annotation_text="COVID-19", annotation_font_color=TEAL,
                      annotation_font_size=10)
        l = plot_layout("US Per-Capita Ethanol Consumption, 1977-2023", height=340, legend=False)
        l["yaxis"]["title"] = "Gallons of Ethanol"
        fig.update_layout(**l)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown('<p class="section-label">How to use this dashboard</p>', unsafe_allow_html=True)
        st.markdown("""
        <div class="story-box">
        Use the sidebar to move through five chapters, each built around a specific question.<br><br>
        <strong>Chapter 1</strong> — How has the nation changed over 47 years?<br>
        <strong>Chapter 2</strong> — Which states drink the most and least?<br>
        <strong>Chapter 3</strong> — Is America ditching beer for spirits?<br>
        <strong>Chapter 4</strong> — What did COVID-19 do to our drinking?<br>
        <strong>Chapter 5</strong> — How do regions and states compare?<br><br>
        Use the <strong>year range slider</strong> to zoom into any period. Use the <strong>state selector</strong> to build custom comparisons in Chapter 5.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="story-box" style="border-left-color:#00b4d8;">
        <strong>What is apparent consumption?</strong><br><br>
        Apparent consumption means alcohol sales per person in a state, not the exact amount people actually drink. Some states may show higher numbers because of cross-border purchases or tourism, so the data reflects where alcohol is sold rather than strictly where it is consumed.
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# CHAPTER 1
# ══════════════════════════════════════════════════════════════
elif nav == "Chapter 1 — The National Arc":
    st.markdown('<span class="chapter-tag">Chapter 1</span>', unsafe_allow_html=True)
    st.markdown('<h1 class="page-headline">The Long Arc of<br><em style="color:#f0a500;">American Drinking</em></h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-deck">The national trend shows how drinking habits in the U.S. have changed over time. Alcohol consumption was highest around 1981, then declined during the 1990s as awareness and regulations increased. After 2000, consumption slowly rose again, and the COVID-19 period created another noticeable shift.</p>', unsafe_allow_html=True)

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=us_f["year"], y=us_f["ethanol_all_drinks_gallons_per_capita"],
        mode="lines", line=dict(color=AMBER, width=3),
        fill="tozeroy", fillcolor="rgba(240,165,0,0.06)",
        hovertemplate="<b>%{x}</b><br>%{y:.3f} gallons/capita<extra></extra>"
    ))
    fig1.update_layout(**{
        **plot_layout("US Total Ethanol Per Capita, 1977 to 2023", height=420, legend=False),
        "yaxis": dict(title="Gallons of Ethanol Per Capita", gridcolor=GRID_COLOR,
                      linecolor=BORDER, tickcolor=BORDER, showgrid=True, zeroline=False),
        "annotations": [
            dict(x=1981, y=2.76, text="All-time peak 2.76 gal", showarrow=True,
                 arrowhead=2, ax=45, ay=-40, font=dict(color=AMBER, size=11), arrowcolor=AMBER),
            dict(x=1997, y=2.14, text="30-year low 2.14 gal", showarrow=True,
                 arrowhead=2, ax=-55, ay=-35, font=dict(color=TEAL, size=11), arrowcolor=TEAL),
            dict(x=2020, y=2.40, text="COVID spike", showarrow=True,
                 arrowhead=2, ax=40, ay=-45, font=dict(color=ROSE, size=11), arrowcolor=ROSE),
        ]
    })
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("""
    <div class="story-box">
    Alcohol consumption in the United States reached its highest level around 1981, when people were drinking about 2.76 gallons of ethanol per person. After that, drinking gradually declined through the 1980s and 1990s, reaching a low point around 1997. This decline likely reflects stronger drunk-driving laws, a higher legal drinking age, and growing public awareness about alcohol related risks. After 2000, consumption slowly began to increase again, showing a gradual change in drinking trends. Around 2020, there was a noticeable spike during the COVID-19 period, when many people shifted their social activities including drinking to their homes.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-label">Translated into standard drinks</p>', unsafe_allow_html=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=us_f["year"], y=us_f["number_of_drinks_total"],
        marker=dict(
            color=us_f["number_of_drinks_total"],
            colorscale=[[0,"#161b22"],[0.4,"#2d3748"],[0.7,"#744210"],[1.0,AMBER]],
            showscale=False
        ),
        hovertemplate="<b>%{x}</b><br>%{y:.0f} drinks/person/year<extra></extra>"
    ))
    l2 = plot_layout("Annual Standard Drinks Per Person, United States", height=360, legend=False)
    l2["yaxis"]["title"] = "Standard Drinks Per Year"
    fig2.update_layout(**l2)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("""
    <div class="story-box">
    When ethanol consumption is converted into standard drinks, it becomes easier to understand. At the 1981 peak, the average American consumed the equivalent of about 590 drinks per year (around 11 drinks per week), even when the calculation includes non-drinkers and children. By the late 1990s, this dropped to about 455 drinks per year. By 2023, the number rose again to around 529 drinks, showing that while consumption declined after the 1980s, it has partially increased again since 2000.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# CHAPTER 2 — STATE COMPARISONS
# ══════════════════════════════════════════════════════════════
elif nav == "Chapter 2 — A Nation Divided":
    st.markdown('<span class="chapter-tag">Chapter 2</span>', unsafe_allow_html=True)
    st.markdown('<h1 class="page-headline">A Nation Divided<br><em style="color:#f0a500;">State by State</em></h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-deck">Alcohol consumption varies widely across states. For example, New Hampshire’s consumption is more than three times higher than Utah’s. This large difference is not random, it reflects long standing influences such as state alcohol policies, religious and cultural norms, tourism, and pricing, which have shaped drinking patterns for decades.</p>', unsafe_allow_html=True)

    col_ctrl1, col_ctrl2 = st.columns(2)
    with col_ctrl1:
        map_year = st.select_slider("Select year", options=list(range(1977, 2024)), value=2023)
    with col_ctrl2:
        drink_opt = st.selectbox("Measure by", [
            ("ethanol_all_drinks_gallons_per_capita", "All Drinks Combined"),
            ("ethanol_beer_gallons_per_capita",       "Beer Only"),
            ("ethanol_wine_gallons_per_capita",       "Wine Only"),
            ("ethanol_spirit_gallons_per_capita",     "Spirits Only"),
        ], format_func=lambda x: x[1])
    drink_col, drink_label = drink_opt

    snap = states_df[states_df["year"] == map_year].copy()

    st.markdown('<p class="section-label">Geographic heat map — use the year slider above</p>', unsafe_allow_html=True)

    fig3 = go.Figure(data=go.Choropleth(
        locations=snap["abbrev"],
        z=snap[drink_col],
        locationmode="USA-states",
        colorscale=[
            [0.00, "#0d1117"],
            [0.20, "#1a2744"],
            [0.45, "#0c4a6e"],
            [0.65, "#0369a1"],
            [0.80, "#f0a500"],
            [1.00, "#fde68a"],
        ],
        zmin=snap[drink_col].min(),
        zmax=snap[drink_col].max(),
        colorbar=dict(
            title=dict(text="Gal/Capita", font=dict(color=FONT_COLOR, size=11)),
            tickfont=dict(color=FONT_COLOR, size=10),
            bgcolor="rgba(0,0,0,0)",
            bordercolor=BORDER,
            thickness=14, len=0.7
        ),
        hovertemplate="<b>%{location}</b><br>%{z:.3f} gal/capita<extra></extra>",
        marker_line_color="#21262d",
        marker_line_width=0.5
    ))
    fig3.update_layout(
        geo=dict(
            scope="usa",
            bgcolor=PAPER_BG,
            lakecolor="#0d1117",
            landcolor="#161b22",
            showlakes=True, showland=True,
            coastlinecolor=BORDER, subunitcolor=BORDER,
            showcoastlines=True
        ),
        paper_bgcolor=PAPER_BG,
        font=dict(color=FONT_COLOR),
        title=dict(
            text=f"{drink_label} by State, {map_year}",
            font=dict(family="Georgia, serif", size=16, color=FONT_COLOR)
        ),
        height=490,
        margin=dict(l=0, r=0, t=50, b=0),
        hoverlabel=dict(bgcolor="#161b22", bordercolor=BORDER, font=dict(color=FONT_COLOR))
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("""
    <div class="story-box">
    The map shows clear regional differences in alcohol consumption across the United States. States in the Northeast and parts of the Mountain West tend to have higher consumption levels, influenced by factors such as tourism and easier access to alcohol. In contrast, many Southern states show lower consumption, reflecting long standing cultural traditions, stronger religious influence, and stricter alcohol regulations. These patterns highlight how geography, culture, and policy shape drinking habits across the country.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-label">All states ranked</p>', unsafe_allow_html=True)
    snap_s = snap.sort_values(drink_col, ascending=True)
    q75 = snap_s[drink_col].quantile(0.75)
    q25 = snap_s[drink_col].quantile(0.25)
    bar_c = [AMBER if v >= q75 else TEAL if v <= q25 else "#2d3748" for v in snap_s[drink_col]]

    fig4 = go.Figure(go.Bar(
        x=snap_s[drink_col], y=snap_s["state_name"],
        orientation="h", marker=dict(color=bar_c),
        hovertemplate="<b>%{y}</b><br>%{x:.3f} gal/capita<extra></extra>"
    ))
    l4 = plot_layout(f"All States Ranked — {drink_label}, {map_year}", height=950, legend=False)
    l4["xaxis"]["title"] = "Gallons of Ethanol Per Capita"
    l4["margin"]["l"] = 155
    fig4.update_layout(**l4)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("""
    <div class="story-box">
    This ranking shows how alcohol consumption differs across U.S. states in 2023. New Hampshire has the highest consumption, followed by states like Delaware, District of Columbia, and Nevada, while Utah has the lowest. The gap between the highest and lowest states is large, with New Hampshire consuming more than three times as much alcohol as Utah. These differences reflect factors such as state alcohol policies, pricing, tourism, and cultural or religious influences. For example, lower alcohol prices and cross border purchases increase sales in some states, while stronger religious traditions and stricter alcohol regulations contribute to lower consumption in others. Overall, the ranking highlights how local culture, laws, and economic factors shape drinking patterns across states.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# CHAPTER 3
# ══════════════════════════════════════════════════════════════
elif nav == "Chapter 3 — What America Drinks":
    st.markdown('<span class="chapter-tag">Chapter 3</span>', unsafe_allow_html=True)
    st.markdown('<h1 class="page-headline">Beer Is Losing.<br><em style="color:#f0a500;">Spirits Have Won.</em></h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-deck">In 2022, spirits became the largest source of alcohol consumption in the United States, surpassing beer for the first time. This shift did not happen suddenly but developed gradually over about 25 years, reflecting changing drinking preferences and trends.</p>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: show_beer = st.checkbox("Show Beer",    value=True)
    with c2: show_wine = st.checkbox("Show Wine",    value=True)
    with c3: show_spir = st.checkbox("Show Spirits", value=True)

    st.markdown('<p class="section-label">Ethanol contribution by drink type</p>', unsafe_allow_html=True)
    fig5 = go.Figure()
    if show_beer:
        fig5.add_trace(go.Scatter(
            x=us_f["year"], y=us_f["ethanol_beer_gallons_per_capita"],
            mode="lines", name="Beer", line=dict(color=TEAL, width=2.5),
            hovertemplate="Beer %{x}: %{y:.3f} gal<extra></extra>"
        ))
    if show_wine:
        fig5.add_trace(go.Scatter(
            x=us_f["year"], y=us_f["ethanol_wine_gallons_per_capita"],
            mode="lines", name="Wine", line=dict(color=SAGE, width=2.5),
            hovertemplate="Wine %{x}: %{y:.3f} gal<extra></extra>"
        ))
    if show_spir:
        fig5.add_trace(go.Scatter(
            x=us_f["year"], y=us_f["ethanol_spirit_gallons_per_capita"],
            mode="lines", name="Spirits", line=dict(color=AMBER, width=2.5),
            hovertemplate="Spirits %{x}: %{y:.3f} gal<extra></extra>"
        ))
    if y1 >= 2022:
        fig5.add_vline(x=2022, line_dash="dot", line_color=ROSE, line_width=1.5,
                       annotation_text="Spirits pass Beer — 2022",
                       annotation_font_color=ROSE, annotation_font_size=11,
                       annotation_position="top left")
    l5 = plot_layout("Ethanol by Drink Type — US National", height=420)
    l5["yaxis"]["title"] = "Gallons of Ethanol Per Capita"
    fig5.update_layout(**l5)
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown("""
    <div class="story-box">
    This chart shows how different types of alcohol have contributed to overall drinking in the United States over time. Beer was the dominant drink for many decades, but its consumption has slowly declined since the mid 1980s. Spirits dropped during the 1990s but began rising again after 2000, eventually surpassing beer in 2022 to become the largest source of ethanol consumed. Meanwhile, wine consumption has grown gradually, showing a steady but smaller increase over the years. Overall, the chart reflects a shift in American drinking preferences from beer toward spirits and wine.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-label">Market share of each drink type over time</p>', unsafe_allow_html=True)
    us_sh = us_f.copy()
    tot = us_sh["ethanol_all_drinks_gallons_per_capita"].replace(0, 1)
    us_sh["beer_pct"]   = us_sh["ethanol_beer_gallons_per_capita"]   / tot * 100
    us_sh["wine_pct"]   = us_sh["ethanol_wine_gallons_per_capita"]   / tot * 100
    us_sh["spirit_pct"] = us_sh["ethanol_spirit_gallons_per_capita"] / tot * 100

    fig6 = go.Figure()
    fig6.add_trace(go.Scatter(
        x=us_sh["year"], y=us_sh["spirit_pct"], name="Spirits",
        stackgroup="one", mode="lines", line=dict(width=0),
        fillcolor="rgba(240,165,0,0.82)",
        hovertemplate="Spirits: %{y:.1f}%<extra></extra>"
    ))
    fig6.add_trace(go.Scatter(
        x=us_sh["year"], y=us_sh["wine_pct"], name="Wine",
        stackgroup="one", mode="lines", line=dict(width=0),
        fillcolor="rgba(123,196,127,0.82)",
        hovertemplate="Wine: %{y:.1f}%<extra></extra>"
    ))
    fig6.add_trace(go.Scatter(
        x=us_sh["year"], y=us_sh["beer_pct"], name="Beer",
        stackgroup="one", mode="lines", line=dict(width=0),
        fillcolor="rgba(0,180,216,0.82)",
        hovertemplate="Beer: %{y:.1f}%<extra></extra>"
    ))
    l6 = plot_layout("Share of Total Ethanol by Drink Type (%)", height=380)
    l6["yaxis"]["title"] = "Share of Total (%)"
    l6["yaxis"]["range"] = [0, 100]
    fig6.update_layout(**l6)
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown("""
    <div class="story-box">
     This chart shows how the share of different types of alcohol has changed in the United States over time. Beer once dominated alcohol consumption, making up nearly half of all ethanol consumed in the late 1970s, but its share has gradually declined to about 40% today. Spirits have steadily gained popularity, rising to their highest share in recent years and becoming a major part of overall consumption. Wine has also grown slowly, increasing its share over time. Overall, the chart highlights a shift in drinking preferences, with beer losing dominance while spirits and wine gain ground.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# CHAPTER 4
# ══════════════════════════════════════════════════════════════
elif nav == "Chapter 4 — The COVID Shock":
    st.markdown('<span class="chapter-tag">Chapter 4</span>', unsafe_allow_html=True)
    st.markdown('<h1 class="page-headline">The Pandemic<br><em style="color:#f0a500;">Changed Everything</em></h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-deck">In 2020, when bars and restaurants closed during COVID 19, people did not stop drinking. Instead, many shifted to drinking at home. During this period, spirits consumption increased sharply and continued to stay high even after restrictions were lifted. This shows how the pandemic changed drinking habits and strengthened the popularity of spirits.</p>', unsafe_allow_html=True)

    covid_us = us_df[(us_df["year"] >= 2015) & (us_df["year"] <= 2023)].copy()

    st.markdown('<p class="section-label">Drink-by-drink breakdown, 2015 to 2023</p>', unsafe_allow_html=True)
    fig7 = make_subplots(
        rows=1, cols=3, subplot_titles=["Beer", "Wine", "Spirits"],
        horizontal_spacing=0.08
    )
    for i, (col, color) in enumerate([
        ("ethanol_beer_gallons_per_capita",   TEAL),
        ("ethanol_wine_gallons_per_capita",   SAGE),
        ("ethanol_spirit_gallons_per_capita", AMBER)
    ], start=1):
        bar_c = [ROSE if y == 2020 else color for y in covid_us["year"]]
        fig7.add_trace(go.Bar(
            x=covid_us["year"], y=covid_us[col],
            marker_color=bar_c, showlegend=False,
            hovertemplate="%{x}: %{y:.3f} gal<extra></extra>"
        ), row=1, col=i)
    fig7.update_layout(
        paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(family="DM Sans, sans-serif", color=FONT_COLOR, size=11),
        height=400,
        title=dict(
            text="Consumption by Type, 2015-2023  (Pink bar = 2020 pandemic year)",
            font=dict(family="Georgia, serif", size=15, color=FONT_COLOR)
        ),
        margin=dict(l=45, r=20, t=60, b=40),
        hoverlabel=dict(bgcolor="#161b22", bordercolor=BORDER, font=dict(color=FONT_COLOR))
    )
    for i in range(1, 4):
        fig7.update_xaxes(gridcolor=GRID_COLOR, linecolor=BORDER, row=1, col=i)
        fig7.update_yaxes(gridcolor=GRID_COLOR, linecolor=BORDER, row=1, col=i)
    for ann in fig7.layout.annotations:
        ann.font.color = FONT_COLOR
    st.plotly_chart(fig7, use_container_width=True)
    st.markdown("""
    <div class="story-box">
    The charts show how beer, wine, and spirits consumption changed from 2015 to 2023. Beer consumption remained mostly stable, with only small changes even during the pandemic. Wine increased slightly around 2020 but stayed fairly steady overall. Spirits showed the biggest change, rising sharply in 2020 and continuing to increase in the following years. This suggests that the pandemic accelerated a shift in drinking preferences toward spirits.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-label">Which states changed most during COVID?</p>', unsafe_allow_html=True)
    pre  = states_df[states_df["year"]==2019][["state_name","ethanol_all_drinks_gallons_per_capita"]].rename(columns={"ethanol_all_drinks_gallons_per_capita":"pre"})
    post = states_df[states_df["year"]==2021][["state_name","ethanol_all_drinks_gallons_per_capita"]].rename(columns={"ethanol_all_drinks_gallons_per_capita":"post"})
    cov  = pre.merge(post, on="state_name")
    cov["change"] = cov["post"] - cov["pre"]
    cov  = cov.sort_values("change", ascending=True)
    c_colors = [SAGE if v > 0 else VIOLET for v in cov["change"]]

    fig8 = go.Figure(go.Bar(
        x=cov["change"], y=cov["state_name"],
        orientation="h", marker=dict(color=c_colors),
        hovertemplate="<b>%{y}</b>  %{x:+.3f} gal<extra></extra>"
    ))
    fig8.add_vline(x=0, line_color=BORDER, line_width=1.5)
    l8 = plot_layout("State-Level Change in Consumption: 2019 to 2021  (Green = increase, Violet = decrease)", height=950, legend=False)
    l8["xaxis"]["title"] = "Change in Gallons/Capita"
    l8["margin"]["l"] = 155
    fig8.update_layout(**l8)
    st.plotly_chart(fig8, use_container_width=True)
    st.markdown("""
    <div class="story-box">
    This chart shows how alcohol consumption changed across U.S. states between 2019 and 2021 during the COVID period. Most states experienced an increase in alcohol consumption, shown by the green bars, suggesting that many people drank more while staying at home during lockdowns. A few states recorded declines, possibly due to reduced tourism or local demographic factors. Overall, the chart indicates that the pandemic generally led to higher alcohol consumption across much of the country.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# CHAPTER 5
# ══════════════════════════════════════════════════════════════
elif nav == "Chapter 5 — Regions & States":
    st.markdown('<span class="chapter-tag">Chapter 5</span>', unsafe_allow_html=True)
    st.markdown('<h1 class="page-headline">Four Regions,<br><em style="color:#f0a500;">One Country</em></h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-deck">Alcohol consumption trends are not the same across the United States. States in the West generally show higher consumption, while many Southern states remain lower. Even though national trends have changed over time, the difference between these regions has stayed fairly consistent for nearly five decades.</p>', unsafe_allow_html=True)

    st.markdown('<p class="section-label">Regional trajectories over time</p>', unsafe_allow_html=True)
    fig9 = go.Figure()
    for region, color in REGION_COLOR.items():
        rd = reg_f[reg_f["state_name"] == region]
        fig9.add_trace(go.Scatter(
            x=rd["year"], y=rd["ethanol_all_drinks_gallons_per_capita"],
            mode="lines", name=region.replace(" Region", ""),
            line=dict(color=color, width=2.3),
            hovertemplate=f"{region.replace(' Region','')} %{{x}}: %{{y:.2f}} gal<extra></extra>"
        ))
    l9 = plot_layout("Total Ethanol Per Capita by US Region", height=420)
    l9["yaxis"]["title"] = "Gallons of Ethanol Per Capita"
    fig9.update_layout(**l9)
    st.plotly_chart(fig9, use_container_width=True)
    st.markdown("""
    <div class="story-box">
    This chart shows how alcohol consumption has changed across different U.S. regions over time. All regions follow a similar pattern with higher consumption around 1980, a decline during the 1990s, and a gradual increase after 2000. However, the levels differ by region. The West consistently shows the highest consumption, followed by the Northeast, while the Midwest remains in the middle. The South has the lowest levels throughout the period. Despite changes over time, the gap between regions has remained fairly consistent.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-label">Beer vs wine vs spirits by region </p>', unsafe_allow_html=True)
    region_names = ["Midwest Region","Northeast Region","South Region","West Region"]
    fig10 = make_subplots(
        rows=2, cols=2,
        subplot_titles=[r.replace(" Region","") for r in region_names],
        horizontal_spacing=0.1, vertical_spacing=0.14
    )
    positions = [(1,1),(1,2),(2,1),(2,2)]
    for (row, col_n), region in zip(positions, region_names):
        rd = reg_f[reg_f["state_name"] == region]
        show = (region == "Midwest Region")
        fig10.add_trace(go.Scatter(
            x=rd["year"], y=rd["ethanol_beer_gallons_per_capita"],
            mode="lines", name="Beer", line=dict(color=TEAL, width=1.8),
            showlegend=show,
            hovertemplate="Beer %{x}: %{y:.3f}<extra></extra>"
        ), row=row, col=col_n)
        fig10.add_trace(go.Scatter(
            x=rd["year"], y=rd["ethanol_wine_gallons_per_capita"],
            mode="lines", name="Wine", line=dict(color=SAGE, width=1.8),
            showlegend=show,
            hovertemplate="Wine %{x}: %{y:.3f}<extra></extra>"
        ), row=row, col=col_n)
        fig10.add_trace(go.Scatter(
            x=rd["year"], y=rd["ethanol_spirit_gallons_per_capita"],
            mode="lines", name="Spirits", line=dict(color=AMBER, width=1.8),
            showlegend=show,
            hovertemplate="Spirits %{x}: %{y:.3f}<extra></extra>"
        ), row=row, col=col_n)
    fig10.update_layout(
        paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
        font=dict(family="DM Sans, sans-serif", color=FONT_COLOR, size=11),
        height=520,
        title=dict(
            text="Beer vs Wine vs Spirits by Region",
            font=dict(family="Georgia, serif", size=15, color=FONT_COLOR)
        ),
        margin=dict(l=45, r=20, t=60, b=40),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
        hoverlabel=dict(bgcolor="#161b22", bordercolor=BORDER, font=dict(color=FONT_COLOR))
    )
    for i in range(1, 3):
        for j in range(1, 3):
            fig10.update_xaxes(gridcolor=GRID_COLOR, linecolor=BORDER, row=i, col=j)
            fig10.update_yaxes(gridcolor=GRID_COLOR, linecolor=BORDER, row=i, col=j)
    for ann in fig10.layout.annotations:
        ann.font.color = FONT_COLOR
    st.plotly_chart(fig10, use_container_width=True)
    st.markdown("""
    <div class="story-box">
    These charts compare how beer, wine, and spirits consumption has changed across different U.S. regions. In every region, beer was once the most consumed drink but has gradually declined over time. Spirits dropped during the 1990s but later increased strongly, especially in recent years, showing a growing preference for spirits. Wine has increased slowly and steadily across all regions. While the general trend is similar everywhere, the timing and strength of these changes vary slightly by region.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-label">COMPARE STATE DRINKING TRENDS</p>', unsafe_allow_html=True)
    if sel_states:
        sel_data = st_f[st_f["state_name"].isin(sel_states)]
        fig11 = px.line(
            sel_data, x="year", y="ethanol_all_drinks_gallons_per_capita",
            color="state_name", color_discrete_sequence=PALETTE,
            labels={"ethanol_all_drinks_gallons_per_capita": "Gallons/Capita",
                    "year": "Year", "state_name": "State"}
        )
        l11 = plot_layout("Per-Capita Consumption — Selected States", height=420)
        l11["yaxis"]["title"] = "Gallons of Ethanol Per Capita"
        fig11.update_layout(**l11)
        fig11.update_traces(line=dict(width=2.3))
        st.plotly_chart(fig11, use_container_width=True)
        st.markdown("""
        <div class="story-box">
        This chart compares alcohol consumption trends across selected U.S. states over time. States such as Nevada and New Hampshire consistently show higher consumption levels, while Utah remains much lower throughout the period. Although most states follow similar national trends, including a decline in the 1990s and a gradual increase after 2000, the gap between higher and lower consumption states remains fairly consistent. This suggests that local policies, culture, and demographics play an important role in shaping drinking patterns.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Select at least one state from the sidebar to display this chart.")

# ══════════════════════════════════════════════════════════════
# QUEST FRAMEWORK
# ══════════════════════════════════════════════════════════════
elif nav == "QUEST Framework":
    st.markdown('<span class="chapter-tag">Analytical Methodology</span>', unsafe_allow_html=True)
    st.markdown('<h1 class="page-headline">The QUEST Framework<br><em style="color:#f0a500;">How We Analyzed This Data</em></h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-deck">Every visualization in this dashboard was created using the QUEST methodology, a five phase approach to exploratory data analysis. In this method, each chart is designed to answer a specific question, and the insights from that chart help generate the next question, guiding the analysis step by step.</p>', unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    phases = [
        ("Q", "Question — Define the Analytical Mission",
         "In the first step, the focus was on defining the main analytical questions before working with the data. Five clear and testable questions were established to guide the entire project:<br><br>"
         "1. How has total US alcohol consumption changed from 1977 to 2023?<br>"
         "2. Which states consume the most and least, and has that ranking changed over time?<br>"
         "3. Has the composition shifted between beer, wine, and spirits — and when?<br>"
         "4. How did COVID-19 affect consumption nationally and at the state level?<br>"
         "5. What structural differences exist across the four US census regions?<br><br>"
         "At this stage, no charts were created yet. The goal was to first understand what needed to be investigated. Following the QUEST approach, the analysis begins with clear questions, and each visualization in the dashboard is later designed to answer one of these specific questions."),

        ("U", "Understand — Audit the Data",
         "The dataset was sourced from the NIAAA via Kaggle. Our audit confirmed:<br><br>"
         "Shape: 2,632 rows x 11 columns covering 47 years across 51 states + DC + 4 regions + US Total<br>"
         "Missing values: <strong>zero</strong> — the dataset is fully complete<br>"
         "Data types: all numeric except state/state_name (string)<br><br>"
         "Key audit finding: the dataset includes regional aggregates (Midwest, Northeast, South, West, US Total) along with state-level rows. These were separated before any state-level analysis to avoid double counting. The state abbreviation column contained full lowercase state names rather than standard two letter codes, so a custom mapping table was created to allow the choropleth map to render correctly.<br><br>"
         "Key limitation: the dataset measures apparent alcohol consumption based on sales data, not actual drinking behavior from surveys. States such as New Hampshire and Nevada show higher values partly because of cross-border purchases and tourism, which can inflate sales figures."),

        ("E", "Explore — Individual Variables",
         "After auditing the dataset, each variable was examined individually to understand its patterns and distribution.<br><br>"
         "<strong>ethanol_all_drinks_gallons_per_capita</strong>: values range from 0.79 gallons (Utah in low years) to 7.58 gallons (New Hampshire in peak years). The distribution is positively skewed, mainly because New Hampshire and Washington DC consistently appear as high outliers.<br><br>"
         "<strong>year</strong>: the data is evenly distributed from 1977 to 2023, with no missing years or gaps in the timeline.<br><br>"
         "<strong>Beer variable</strong>: shows a steady decline nationally across the 47 year period, indicating a gradual reduction in beer’s share of alcohol consumption.<br>"
         "<strong>Spirits variable</strong>follows a U shaped pattern, declining through the 1990s, then increasing again after 2000, eventually reaching its highest share in recent years.<br>"
         "<strong>Wine variable</strong>: displays a slow and consistent increase across the entire period, with no major drops or reversals.<br><br>"
         "Across most years, state level distributions are right skewed, with New Hampshire and Nevada regularly appearing as high consumption outliers, while Utah consistently remains the lowest."),

        ("S", "Study — Relationships and Patterns",
         "In this phase, we analyzed how variables interact and looked for broader patterns in the data. Three important relationships emerged.<br><br>"
         "<strong>Beer-spirits inverse relationship</strong>: as spirits consumption increases, beer consumption tends to decrease. This pattern appears both in the national data and across all four regions. The shift became especially clear when spirits overtook beer in 2022.<br><br>"
         "<strong>Geographic clustering</strong>: states form clear regional patterns. Higher consumption is generally seen in the Northeast, Mountain West, and Pacific regions, while Southeastern states and parts of the Midwest tend to show lower consumption. This pattern has remained stable for nearly 47 years, suggesting that long-term structural factors such as policy, religion, and demographics play a larger role than short-term economic changes.<br><br>"
         "<strong>COVID asymmetric shock</strong>: the 2020–2021 period caused a noticeable shift in drinking behavior. Spirits consumption increased much more sharply than beer or wine, creating a lasting change in the overall mix of alcohol consumption. This pattern was observed in both national trends and state level comparisons."),

        ("T", "Tell — Synthesize and Communicate",
         "In the Tell phase, the results were organized into a clear narrative so the dashboard could communicate insights to a non technical audience. Instead of showing charts as separate outputs, the visualizations were structured into a logical story.<br><br>"
         "<strong>Chapter 1</strong> introduces the long term national trend, providing important context before comparing individual states.<br>"
         "<strong>Chapter 2</strong> focuses on geographic differences, showing how alcohol consumption varies across states and why relying only on the national average can be misleading.<br>"
         "<strong>Chapter 3</strong> highlights the structural shift in drinking preferences, particularly the long transition from beer dominance to the rise of spirits.<br>"
         "<strong>Chapter 4</strong> examines the impact of COVID 19, identifying how the pandemic changed consumption patterns in recent years.<br>"
         "<strong>Chapter 5</strong> links individual state trends back to broader regional patterns using faceted comparisons.<br><br>"
         "Throughout the dashboard, consistent colors are used to make the visuals easy to interpret. Amber represents the primary metric and spirits, teal represents beer, and green represents wine. Each chart is followed by a plain English interpretation so that the findings are easy to understand for readers without a technical background, aligning with the QUEST principle that exploratory analysis should communicate insights, not just present charts."),
    ]

    for letter, title, body in phases:
        st.markdown(f"""
        <div class="quest-phase">
            <div class="quest-letter">{letter}</div>
            <div class="quest-title">{title}</div>
            <div class="quest-body">{body}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Iterative Insights in the QUEST Process</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="story-box">
    The QUEST process is iterative, meaning new findings can send the analysis back to earlier phases.
                
    <strong>Discovery Loop (Tell to Question):</strong> During the Tell phase, the COVID 19 findings raised a new question that was not part of the original five: did the pandemic affect all types of alcohol equally, or did it favor spirits more than beer and wine? This new question led to additional analysis and resulted in the state level diverging bar chart presented in Chapter 4.<br><br>
    <strong>Quality Loop (Any Phase to Understand):</strong> While creating the map in Chapter 2, the choropleth initially failed to render because the state column contained full lowercase state names instead of standard two letter postal abbreviations. This required returning to the Understand phase to build a complete state to abbreviation mapping table. This is a typical example of a data quality issue appearing during later stages of analysis rather than during the initial audit.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# DATA SOURCE
# ══════════════════════════════════════════════════════════════
elif nav == "Data Source":
    st.markdown('<span class="chapter-tag">Data Documentation</span>', unsafe_allow_html=True)
    st.markdown('<h1 class="page-headline">Data Source<br><em style="color:#f0a500;">and Documentation</em></h1>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class="story-box">
        <strong>Primary Source</strong><br>
        National Institute on Alcohol Abuse and Alcoholism (NIAAA)<br>
        Surveillance Report: Apparent Per Capita Alcohol Consumption<br>
        niaaa.nih.gov/research/surveillance-programs<br><br>
        <strong>Kaggle Dataset</strong><br>
        US Alcohol Consumption by State, 1977-2023<br>
        Author: Sana Ijlal Shahrukh<br>
        kaggle.com/datasets/sanaijlalshahrukh<br><br>
        <strong>Date of Access:</strong> March 2026<br>
        <strong>License:</strong> Public domain — US government data
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class="story-box">
        <strong>Dataset Dimensions</strong><br>
        Rows: 2,632 | Columns: 11<br>
        Coverage: 1977-2023 (47 years)<br>
        States: 51 + DC + 4 US regions + US Total<br>
        Missing Values: None<br><br>
        <strong>Key Variables</strong><br>
        ethanol_beer_gallons_per_capita<br>
        ethanol_wine_gallons_per_capita<br>
        ethanol_spirit_gallons_per_capita<br>
        ethanol_all_drinks_gallons_per_capita<br>
        number_of_drinks_total
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<p class="section-label">Dashboard Update Guide</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="story-box">
    The NIAAA publishes updated surveillance reports every year, usually releasing data for the previous year around mid-year.<br><br>
    To update this dashboard:<br>
    1. Visit niaaa.nih.gov/research/surveillance-programs<br>
    2. Download the latest apparent per capita consumption table<br>
    3. Append the new rows to the existing CSV file, keeping the same column structure<br>
    4. Re-deploy the dashboard to Google Cloud Run using the same build and deployment commands from the deployment guide<br><br>
    Once the new data is added, the dashboard automatically updates all charts, KPI cards, and year filters to reflect the latest year available in the dataset. No additional code changes are needed for regular annual updates.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-label">Important caveat on apparent consumption</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="story-box" style="border-left-color:#00b4d8;">
    This dataset measures the amount of alcohol sold in each state divided by the total population, rather than actual drinking behavior reported in surveys. Because of this, a few important considerations are necessary when interpreting the data.<br><br>
    First, New Hampshire’s high consumption values partly reflect cross-border purchases. Residents from nearby states such as Massachusetts and Vermont often travel to New Hampshire to buy alcohol because of its lower prices and state-run liquor stores. These purchases are counted in New Hampshire’s sales data, which increases its apparent per-capita consumption beyond what its residents alone actually drink.<br><br>
    Second, Nevada’s figures are strongly influenced by tourism. Cities like Las Vegas and Reno attract millions of visitors each year, and alcohol consumed by tourists is recorded in Nevada’s sales data even though those visitors are not part of the state’s resident population. <br><br>
    Third, the population denominator includes non-drinkers, such as children, pregnant women, people who abstain for health reasons, and individuals whose religion discourages alcohol consumption. As a result, the average per-capita values in the dataset are lower than the actual consumption among people who drink alcohol.
    </div>
    """, unsafe_allow_html=True)

  