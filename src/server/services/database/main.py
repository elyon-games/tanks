import common.path as path
import common.utils as utils
import json
import os.path

def get_table_path(table) -> str:
    return os.path.join(path.get_path("server_database"), f"{table}-{utils.getMode()}.json")

class BaseModel:
    def __init__(self, schema: dict, default_data: list=[]):
        self.table = self.__class__.__name__.lower()
        self.db_path = get_table_path(self.table)
        self.schema = schema
        utils.create_file_if_not_exists(self.db_path, "[]")
        self.data = self.load()
        if not self.data:
            self.initialize_default_data(default_data)
        self.clean_data()

    def save(self) -> None:
        with open(self.db_path, 'w') as file:
            json.dump(self.data, file)

    def load(self) -> list:
        if os.path.getsize(self.db_path) == 0:
            return []
        with open(self.db_path, 'r') as file:
            return json.load(file)

    def initialize_default_data(self, default_data):
        for record in default_data:
            self.insert(record)

    def remove_extra_fields(self, record):
        return {key: record[key] for key in self.schema.keys()}
    
    def get_all(self):
        return self.data
    
    def get(self, record_id):
        return next((item for item in self.data if item['id'] == record_id), None)
    
    def delete(self, record_id):
        record = next((item for item in self.data if item['id'] == record_id), None)
        if not record:
            raise ValueError(f"Enregistrement avec l'id {record_id} non trouvé")
        self.data.remove(record)
        self.save()
        return record

    def insert(self, record):
        self.validate(record)
        if any(item['id'] == record['id'] for item in self.data):
            raise ValueError(f"Un enregistrement avec l'id {record['id']} existe déjà")
        self.data.append(record)
        self.save()
        return record

    def update(self, record_id, updates):
        record = next((item for item in self.data if item['id'] == record_id), None)
        if not record:
            raise ValueError(f"Enregistrement avec l'id {record_id} non trouvé")
        
        for key, value in updates.items():
            if key in self.schema:
                if not isinstance(value, self.schema[key]['type']):
                    raise TypeError(f"Le champ {key} doit être de type {self.schema[key]['type'].__name__}")
                if self.schema[key].get('unique') and any(item[key] == value for item in self.data if item['id'] != record_id):
                    raise ValueError(f"Le champ {key} doit être unique")
                record[key] = value
        self.save()

    def validate(self, record):
        for field, properties in self.schema.items():
            if properties.get('required') and field not in record:
                raise ValueError(f"Champ manquant: {field}")
            
            if field in record:
                if not isinstance(record[field], properties['type']):
                    raise TypeError(f"Le champ {field} doit être de type {properties['type'].__name__}")
                
                if properties.get('unique') and any(item[field] == record[field] 
                    for item in self.data if item.get('id') != record.get('id')):
                    raise ValueError(f"Le champ {field} doit être unique")

            if 'default' in properties and field not in record:
                record[field] = properties['default']

        if 'id' not in record:
            raise ValueError("L'enregistrement doit avoir un champ 'id'")

    def clean_data(self):
        self.data = [self.clean_record(record) for record in self.data]
        self.data = [self.remove_extra_fields(record) for record in self.data]
        self.save()

    def clean_record(self, record):
        cleaned = {}
        for field, properties in self.schema.items():
            if field in record:
                cleaned[field] = record[field]
            elif 'default' in properties:
                cleaned[field] = properties['default']
            else:
                raise ValueError(f"Champ manquant: {field}")
        return cleaned
    
    def insert_or_get_existing(self, record):
        self.validate(record)
        existing = next((item for item in self.data if item['id'] == record['id']), None)
        if existing:
            return existing
        self.data.append(record)
        self.save()
        return record
    
    def len_data(self):
        return len(self.data)