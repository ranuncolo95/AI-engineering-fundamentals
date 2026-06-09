import os


def carica_system(SYSTEM_FILE):
    """Carica system prompt da file txt"""
    
    if os.path.exists(SYSTEM_FILE):
        with open(SYSTEM_FILE, "r", encoding="utf-8") as f:
            system_file = f.read()
            print("System file caricato")
            return system_file

    print("Nessun system file trovato")

    system_file = """
Sei l'assistente virtuale di WiData Srl, azienda IoT e smart cities di Sassari.
Rispondi SOLO basandoti sui documenti forniti nel contesto.
Se la risposta non è nei documenti, dì chiaramente: 'Non ho questa informazione nei miei documenti.'
Non inventare mai informazioni. Sii conciso e preciso.
"""

    return system_file
