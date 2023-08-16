import requests
import time

# Create Separation
create_url = 'https://mvsep.com/api/separation/create'
api_token = 'ayVlKzdaZj8Xgb6RwISmF2ZmZICHZ8'
audiofile_path = 'input/Any Way the Wind Blows.mp3'
sep_type = 9
add_opt1 = 0
add_opt2 = 1
output_format = 1
is_demo = 1

files = {
    'audiofile': ('Any Way the Wind Blows.mp3', open(audiofile_path, 'rb'))
}

payload = {
    'api_token': api_token,
    'sep_type': sep_type,
    'add_opt1': add_opt1,
    'add_opt2': add_opt2,
    'output_format': output_format,
    'is_demo': is_demo
}

response = requests.post(create_url, data=payload, files=files)

if response.status_code == 200:
    result_data = response.json()
    
    if 'data' in result_data and 'hash' in result_data['data']:
        separation_hash = result_data['data']['hash']
        
        # Retrieve the Separation Result
        get_url = f'https://mvsep.com/api/separation/get'
        params = {
            'hash': separation_hash,
            'api_token': api_token
        }
        
        response = requests.get(get_url, params=params)
        print(response)
        
    


        if response.status_code == 200:
            result_data = response.json()
            print(result_data)  # Print the entire response for inspection
            
            
            if 'data' in result_data:
                
                
                # Retrieve the Separation Result
                get_url = f'https://mvsep.com/api/separation/get'
                params = {
                    'hash': separation_hash,
                    'api_token': api_token
                }
                
                max_attempts = 10  # Maximum number of attempts
                current_attempt = 1
                
                while current_attempt <= max_attempts:
                    response = requests.get(get_url, params=params)
                    
                    if response.status_code == 200:
                        result_data = response.json()
                        
                        if 'data' in result_data and 'file_url' in result_data['data']:
                            file_url = result_data['data']['file_url']
                            
                            # Download the separated MP3 file
                            mp3_response = requests.get(file_url)
                            if mp3_response.status_code == 200:
                                output_filename = 'separated_audio.mp3'
                                with open(output_filename, 'wb') as output_file:
                                    output_file.write(mp3_response.content)
                                print(f'Separated MP3 file saved as {output_filename}')
                                break  # Exit the loop if file is downloaded successfully
                            else:
                                print('Failed to download separated MP3 file!')
                        else:
                            print('Separation result information not available in response data.')
                    else:
                        print(f'Failed to retrieve separation result (Attempt {current_attempt}/{max_attempts})')
                    
                    current_attempt += 1
                    time.sleep(120)  # Wait for 10 seconds before trying again
                    
                if current_attempt > max_attempts:
                    print('Max attempts reached. Unable to retrieve separation result.')
        else:
            print('API call failed!')
            print('Status code:', response.status_code)
            print('Response:', response.text)
