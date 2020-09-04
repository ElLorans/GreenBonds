import eikon as ek

with open('key.secret') as file:
    KEY = file.read()

def get_first_announcement_date(id) -> dict
    """
    : param id: str or list
    """
    bonds, err = ek.get_data(id, 'TR.FirstAnnounceDate')
    
    ids_to_dates = dict(zip(bonds.Instrument, bonds['First Announcement Date']))
    return ids_to_dates