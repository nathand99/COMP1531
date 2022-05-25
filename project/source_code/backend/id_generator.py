import string
import random

class IDGenerator:
    def __init__(self, id_length = 4, charactor_set=None):
        self._id_length = id_length
        self._charactor_set = charactor_set if charactor_set is not None else string.ascii_letters + string.digits
    
    @property
    def id_length(self):
        return self._id_length

    @property
    def charactor_set(self):
        return self._charactor_set

    def generate_id(self, exist_ids=[]):
        temp = self._get_random_string()
        while temp in exist_ids:
            temp = self._get_random_string()
        return temp
    
    def _get_random_string(self):
        return "".join(random.choice(self._charactor_set) for i in range(self._id_length))

    
if __name__ == "__main__":
    generator = IDGenerator(6)
    generated_ids = []
    for i in range(100):
        temp_id = generator.generate_id()
        generated_ids.append(temp_id)
        print(f"{generator.generate_id(generated_ids)}")
    
