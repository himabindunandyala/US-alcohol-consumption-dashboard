\# U.S. Alcohol Consumption Trends (1977–2023)



\## Analytical Objective

This dashboard analyzes U.S. apparent per capita alcohol consumption data to understand how drinking patterns have changed over 47 years, evaluate shifts in beverage preferences, and examine how consumption varies across states and regions. The goal is to identify long-term structural trends, understand the geographic distribution of alcohol consumption, and assess the impact of major events — including policy changes and the COVID-19 pandemic — on American drinking behavior.



\## Live Dashboard

&nbsp;https://alcohol-dashboard-301168671061.us-central1.run.app



\## Data Source

The data used in this dashboard comes from the National Institute on Alcohol Abuse and Alcoholism (NIAAA), a division of the U.S. National Institutes of Health. Dataset obtained from Kaggle: \[U.S. Alcohol Consumption by State (1977–2023)](https://www.kaggle.com/datasets/sanaijlalshahrukh/us-alcohol-consumption-by-state-19772023)



This dataset contains state-level apparent per capita alcohol consumption records, including total ethanol consumption and breakdowns by beverage type (beer, wine, and spirits). Dataset link: https://www.kaggle.com/datasets/sanaijlalshahrukh/us-alcohol-consumption-by-state-19772023



\## Data Collection Method

The dataset was obtained through direct download from Kaggle as a CSV file. No API access or web scraping was required. The file was stored locally and uploaded to this GitHub repository for use in the Streamlit dashboard.



\*\*Dataset details:\*\*

\- 2,632 rows × 11 columns

\- Coverage: 1977 – 2023 (47 years)

\- Geography: 51 states + DC + 4 U.S. census regions + national total

\- Missing values: None



\## Data Update Procedure (Future Years)

To keep the dashboard updated as new NIAAA data is released:

1\. Visit the Kaggle dataset page or the official NIAAA website for updated consumption data.

2\. Download the updated dataset including new yearly records.

3\. Replace the existing CSV file in the repository.

4\. Commit and push the updated file to GitHub.

5\. Rebuild and redeploy the Docker container to Google Cloud Run to reflect the updated data.



\## Sustainability of the Dashboard

Because the dataset can be replaced with updated NIAAA releases each year, this dashboard can be continuously updated to reflect current alcohol consumption trends. This ensures the application functions as a living analytical tool rather than a one-time analysis.



\## Key Findings

\- U.S. consumption peaked in 1981 at 2.76 gallons per capita and reached a 30-year low in 1997

\- Spirits overtook beer as the dominant beverage type in 2022 — the first time in recorded history

\- The geographic hierarchy (New Hampshire highest, Utah lowest) has remained stable for nearly five decades

\- COVID-19 caused the largest single-year increase in spirits consumption in the modern data record, and the shift has not reversed



\## Technologies Used

Python, Pandas, Plotly, Streamlit, Docker, Google Cloud Run, Google Artifact Registry, and GitHub.

