class StaffManager():
    def __init__(self):
        self._staff_codes = []
    
    @property
    def staff_codes(self):
        return self._staff_codes

    @staff_codes.setter
    def staff_codes(self, staff_codes):
        self._staff_codes = staff_codes
    
    def register(self, new_staff_code):
        return self._staff_codes.append(new_staff_code)

    def is_exist(self, staff_code):
        return staff_code in self._staff_codes