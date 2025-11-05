from PyQt6.QtWidgets import QLineEdit, QComboBox, QMessageBox

def validate_inputs(self):
    combo_errors = []
    input_errors = []

    invalid_combo_texts = {
        "Select fuel unit here",
        "Select electricity unit here",
        ""
    }
    for combo in self.findChildren(QComboBox):
        if combo.currentText().strip() in invalid_combo_texts:
            combo_errors.append(f"- Select a valid unit for: {combo.objectName()}")

    for field in self.findChildren(QLineEdit):
        if "input" in field.objectName().lower():
            if not field.text().strip():
                input_errors.append(f"- Enter a value for: {field.objectName()}")

    if combo_errors or input_errors:
        QMessageBox.critical(
            self,
            "Input Error",
            "Please ensure all required fields are filled out."
        )
        return False

    return True

def validate_inputs_production_inputs(self):
    input_errors = []
    
    list_of_raw_materials_and_additives = [
        self.ui.limestone_input.text(),
        self.ui.gypsum_input.text(),
        self.ui.calcined_clay_input.text(),
        self.ui.blast_furnace_slag_input.text(),
        self.ui.other_slag_input.text(),
        self.ui.fly_ash_input.text(),
        self.ui.natural_pozzolans_input.text()
        ]
    #print(list_of_raw_materials_and_additives)
    list_of_raw_materials_and_additives_dummy = []
    
    for item in list_of_raw_materials_and_additives:
        try:
            list_of_raw_materials_and_additives_dummy.append(float(item))
        except ValueError:
            list_of_raw_materials_and_additives_dummy.append(0)
    #print(list_of_raw_materials_and_additives_dummy)
    
    Total_raw_material_and_additive = sum(list_of_raw_materials_and_additives_dummy)
    
    def convert_string_to_float(strong_input):
        try:
            float_output = float(strong_input)
        except ValueError:
            float_output = 0
        return float_output
            
    clinker1 = convert_string_to_float(self.ui.production_1_input.text())   
    clinker2 = convert_string_to_float(self.ui.production_2_input.text())
    
    Total_clinker_input = clinker1 + clinker2
    
    list_of_cement = [
        self.ui.pure_portland_cement_production_input.text(),
        self.ui.common_portland_cement_production_input.text(),
        self.ui.slag_cement_production_input.text(),
        self.ui.fly_ash_cement_production_input.text(),
        self.ui.pozzolana_cement_production_input.text(),
        self.ui.blended_cement_production_input.text()
        ]
    list_of_cement_dummy = []
    
    for item in list_of_cement:
        list_of_cement_dummy.append(convert_string_to_float(item))
    
    Total_cement_input = sum(list_of_cement_dummy)
    
    invalid_input = 0

    if Total_raw_material_and_additive == invalid_input:
        input_errors.append("Please ensure that total raw material and additive input is greater than zero.")
    if Total_clinker_input == invalid_input:
        input_errors.append("Please ensure that total clinker production is greater than zero.")
    if Total_cement_input == invalid_input:
        input_errors.append("Please ensure that total cement production is greater than zero.")

    if input_errors:
        QMessageBox.critical(
            self,
            "Input Error",
            "Please ensure that total raw material & additive input, clinker production, and cement production are all greater than zero."
        )
        return False

    return True

def validate_inputs_grinding_inputs(self):
    input_errors = []
    
    list_of_raw_material_grinding = [
        self.ui.ball_mill_raw_input.text(),
        self.ui.vert_roller_mill_raw_input.text(),
        self.ui.horizontal_roller_mill_raw_input.text()
        ]
    list_of_fuel_grinding = [
        self.ui.vert_roller_mill_fuel_input.text(),
        self.ui.horizontal_roller_mill_fuel_input.text()
        ]
    list_of_cement_grinding = [
        self.ui.ball_mill_cement_input.text(),        
        self.ui.vert_roller_mill_cement_input.text(),        
        self.ui.horizontal_roller_mill_cement_input.text()
        ]

    
    def convert_string_to_float(strong_input):
        try:
            float_output = float(strong_input)
        except ValueError:
            float_output = 0
        return float_output
    
    Total_raw_material_grinding = 0
    for i in  list_of_raw_material_grinding:
        Total_raw_material_grinding += convert_string_to_float(i)
    
    Total_fuel_grinding = 0
    for i in list_of_fuel_grinding:
        Total_fuel_grinding += convert_string_to_float(i)
    
    Total_cement_grinding = 0
    for i in list_of_cement_grinding:
        Total_cement_grinding += convert_string_to_float(i)
    
    valid_input = 100
    
    if Total_raw_material_grinding != valid_input:
        input_errors.append("Total raw material grinding share must add up to 100%.")
    if Total_fuel_grinding != valid_input:
        input_errors.append("Total fuel grinding share must add up to 100%.")
    if Total_cement_grinding != valid_input:
        input_errors.append("Total cement grinding share must add up to 100%.")

    if input_errors:
        QMessageBox.critical(
            self,
            "Input Error",
            "Please ensure that total shares of raw material, fuel, and cement grinding all add up to 100%."
        )
        return False

    return True
    
def validate_inputs_new_fuel_share(self):
    input_errors = []
    
    list_of_fuel_sahre = [
        self.ui.coal_input_page9.text(),
        self.ui.coke_input_page9.text(),
        self.ui.natural_gas_input_page9.text(),
        self.ui.biomass_input_page9.text(),
        self.ui.msw_input_page9.text()
        ]
    
    def convert_string_to_float(strong_input):
        try:
            float_output = float(strong_input)
        except ValueError:
            float_output = 0
        return float_output
    
    Total_new_fuel_share = 0
    
    for i in list_of_fuel_sahre:
        Total_new_fuel_share += convert_string_to_float(i)
    
    valid_input = 100
    
    if Total_new_fuel_share != valid_input:
        input_errors.append("Total new fuel share must add up to 100%.")
    
    if input_errors:
        QMessageBox.critical(
            self,
            "Input Error",
            "Please ensure that the total new fuel share must add up to 100%.."
        )
        return False

    return True
        

