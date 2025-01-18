import json
import os
'''
Extract channel IDs from 24.11.12_US_trending_videos.json
to feed it into YTStats class to fetch video data of channels in US trending videos list
'''
def extract_channel_ids_from_multiple_jsons(json_folder, output_file):

    all_channel_ids = set()

    try:
        for file_name in os.listdir(json_folder):
            if file_name.endswith('.json'):
                file_path = os.path.join(json_folder, file_name)
                print(f"Processing file: {file_path}")
                
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                
                channel_ids = [video_data["channelId"] for video_id, video_data in data.items()]
                all_channel_ids.update(channel_ids)
        
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write("\n".join(all_channel_ids))
        
        print(f"Successfully extracted {len(all_channel_ids)} unique channel IDs to {output_file}")
    
    except Exception as e:
        print(f"An error occurred: {e}")