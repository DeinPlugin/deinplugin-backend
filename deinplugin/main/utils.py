import requests

def get_plugin_info(github_url):
    splitted_url = github_url.split('/')
    repository_name = splitted_url[-1]
    user_name = splitted_url[-2]
    result = requests.get('https://raw.githubusercontent.com/' + user_name + '/' + repository_name + '/master/deinplugin.yaml')
    print('https://raw.githubusercontent.com/' + user_name + '/' + repository_name + '/master/deinplugin.yaml')
    
    # parse the file
    if result.status_code == 200:
        # bytes to string
        content = result.content.decode('utf-8')
    else:
        content = None
    return content