import requests


def get_plugin_info(github_url):
    splitted_url = github_url.split('/')
    repository_name = splitted_url[-1]
    user_name = splitted_url[-2]
    default_branch = requests.get('https://api.github.com/repos/' + user_name + '/' + repository_name).json()['default_branch']
    result = requests.get(f'https://raw.githubusercontent.com/{user_name}/{repository_name}/{default_branch}/deinplugin.yaml')

    # parse the file
    if result.status_code == 200:
        # bytes to string
        content = result.content.decode('utf-8')
    else:
        content = None
    return content
