# Youtube-Data-Analysis

This is the folder of Group 24's Introduction to Data Science - IT4142E

**Topic: Trending US YouTube Videos Analysis**

## Use guide

Where to find the datasets:

Our processed datasets can be accessed at `dataset_assets\data\data_main` folder. 
The used files for our model are `all_necessary_video_data.csv` file.

Where to find the EDA:

Our EDA is in the form of a visualization via `YoutubeVideosDashboard.pbix` file. Microsoft PowerBI is required to view our dashboards.

How to use our models:

First, navigate to the Analysis-Youtube-Trending folder and install all required libraries by typing this in your terminal / command prompt:

`pip install -r requirements.txt`

Then, run `app.py` file. Our GUI will be displayed at `http://localhost:9879` address. 

Type in your channel statistics, then choose model and preprocessor (`preprocessor.pkl` file) at `prediction_model\model` folder



Source code checking:

For the data: The `dataset_assets\data\data_old` folder contains all our old datasets.

For the scrapers: The `dataset_assets\scrapers` contains 2 scrapers:

`scraper.py` will crawl all video data currently featured on the Trending page.

To use `scraper.py`, you have to get a YouTube Data API v3 key (via Google), then store it inside `api_key.txt`.
Then, type in your desired country codes (ISO 3166-1 format) inside `country_codes.txt`. 
Our project analyze US videos, but it's possible to get Trending data from other countries as well.

`ytstats.py` will crawl all video data of different channels.
To use `ytstats.py`, it will use the same `api_key.txt` file, but you now type your desired channel IDs inside `channel_id.txt`.

Channel IDs can be found using this website `https://ytlarge.com/youtube/channel-id-finder/`
There will be maximum 300 videos displayed for each channel, as we have limited the number to be safe with the API.

For the model: The model building can be checked via `prediction_model\Predict_final.ipynb` file.
