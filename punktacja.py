from bson.objectid import ObjectId

PUNKTY_ZA_OBOWIAZKOWA = 5
PUNKTY_ZA_NIEOBOWIAZKOWA = 2

def oblicz_bilans_punktow(db=None, ministrant_id=None):
    obecnosci_wszystkie = db.obecnosci.count_documents({'ministrant_id': ministrant_id})
    obecnosci_obowiazkowe = 0
    sluzby = db.sluzby.find({'ministrant_id': ministrant_id})
    for sluzba in sluzby:
        obecnosci_obowiazkowe += db.obecnosci.count_documents({'ministrant_id': ministrant_id, 'msza_id': sluzba["msza_id"]})
    return PUNKTY_ZA_OBOWIAZKOWA*obecnosci_obowiazkowe + PUNKTY_ZA_NIEOBOWIAZKOWA*(obecnosci_wszystkie-obecnosci_obowiazkowe)



