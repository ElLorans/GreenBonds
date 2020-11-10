def get_eikon_key() -> str:
    try:
        with open('key.secret') as file:
            key = file.read()
        return key
    except FileNotFoundError:
        input('key.secret file not found. Please create a file named key.secret with your key for '
              'Refinitiv Workspace')
