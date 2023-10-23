# integrate time based caching

import json
import os
from datetime import datetime, timedelta

def query_api(param):
    cache_file = f'cache/{param}.json'
    
    # Check if the cache file exists
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cached_data = json.load(f)
            timestamp = datetime.strptime(cached_data['timestamp'], '%Y-%m-%d %H:%M:%S')
            
            # Check if the cached data has expired
            if datetime.now() - timestamp < timedelta(hours=1):
                return cached_data['result']
    
    # If cache is missing or expired, make an actual API call
    result = actual_api_call(param)
    
    # Cache the new result along with the current timestamp
    with open(cache_file, 'w') as f:
        json.dump({'result': result, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, f)
    
    return result
