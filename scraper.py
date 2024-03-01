import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime


url = "https://www.unibe.ch/universitaet/campus__und__infrastruktur/universitaetssport/sportangebot/fitnessraeume/readhtml2?decoding=utf-8&url=https://www.zssw.unibe.ch/usp/zms/templates/crowdmonitoring/_display-spaces-zssw.php"

try:
    response = requests.get(url, timeout=180)  # Timeout set to 3 min
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the element with class 'go-stop-display_footer'
    footer_div = soup.find("div", class_="go-stop-display_footer")

    # Extract the text content
    text_content = footer_div.get_text(strip=True)

    # Get the occupancy numbers
    occupancy_numbers = [x.strip() for x in text_content.split("von")]

    # Concatenate old data with the newly observed line
    df_out = pd.concat(
        [
            pd.read_csv("data.csv", parse_dates=["datetime"]),
            pd.DataFrame(
                [
                    {
                        "datetime": pd.Timestamp(datetime.datetime.today()),
                        "actual_occupancy": occupancy_numbers[0],
                        "max_occupancy": occupancy_numbers[1],
                    }
                ]
            ),
        ]
    )

    # Write the data to a CSV file
    df_out.to_csv("data.csv", index=False)

except requests.exceptions.RequestException as e:
    print("Error:", e)