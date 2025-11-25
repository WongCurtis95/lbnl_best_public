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
    
    def convert_string_to_float(string_input):
        try:
            float_output = float(string_input)
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

def validate_inputs_electricity_generation_inputs(self):
    input_errors = []
    
    def convert_string_to_float(string_input):
        try:
            float_output = float(string_input)
        except ValueError:
            float_output = 0
        return float_output
    
    electricity_purchased_or_generated = convert_string_to_float(self.ui.total_energy_purchased_input.text()) + convert_string_to_float(self.ui.total_electricity_generated_onsite_input.text())
    
    if electricity_purchased_or_generated == 0:
        input_errors.append("Total electricity purchased and generated must be greater than zero.")
    
    if convert_string_to_float(self.ui.total_electricity_generated_onsite_input.text()) < convert_string_to_float(self.ui.electricity_generated_input.text()):
        input_errors.append("Electricity generated onsite and sold to the grid cannot be greater than electricity generated onsite.")
    
    if convert_string_to_float(self.ui.total_electricity_generated_onsite_input.text()) < (convert_string_to_float(self.ui.waste_heat_input_page5.text()) + convert_string_to_float(self.ui.onsite_renewables_input_page5.text())):
        input_errors.append("The sum of waste heat electricity generation and onsite renewable generation cannot be greater than electricity generated onsite.")
    
    from utils.save_progress import load_progress_json, get_user_data_dir
    import json
    
    data_dir = get_user_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)
    json_folder = data_dir / "Saved Progress"
    json_folder.mkdir(parents=True, exist_ok=True)
    filepath = json_folder / "Electricity_Generation_Input.json"
    
    with open(filepath, "r") as f:
        electricity_generation_input_dict = json.load(f)
    
    if convert_string_to_float(self.ui.total_electricity_generated_onsite_input.text()) < (electricity_generation_input_dict["Energy used for electricity generation (kWh/year) - waste heat"] + convert_string_to_float(self.ui.onsite_renewables_input_page5.text())):
        input_errors.append("The sum of waste heat electricity generation and onsite renewable generation cannot be greater than electricity generated onsite.")

    if input_errors:
        QMessageBox.critical(
            self,
            "Input Error",
            "Total electricity purchased and generated must be greater than zero; \nElectricity generated onsite and sold to the grid cannot be greater than electricity generated onsite; \nThe sum of waste heat electricity generation and onsite renewable generation cannot be greater than electricity generated onsite."
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
    
    def convert_string_to_float(string_input):
        try:
            float_output = float(string_input)
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

def validate_inputs_energy_quick_inputs(self):
    input_errors = []
    
    list_of_fuel_inputs =[
        self.ui.coal_quick_input_page6.text(),
        self.ui.coke_quick_input_page6.text(),
        self.ui.natural_gas_quick_input_page6.text(),
        self.ui.biomass_quick_input_page6.text(),
        self.ui.msw_quick_input_page6.text()
        ]
    
    def convert_string_to_float(string_input):
        try:
            float_output = float(string_input)
        except ValueError:
            float_output = 0
        return float_output
    
    Total_fuel = 0
    for fuel in list_of_fuel_inputs:
        Total_fuel += convert_string_to_float(fuel)
    
    if Total_fuel == 0:
        input_errors.append("Total fuel input must be greater than zero.")
    
    Total_electricity = convert_string_to_float(self.ui.electricity_quick_input_page6.text())
    if Total_electricity == 0:
        input_errors.append("Electricity input must be greater than zero.")
    
    from utils.save_progress import load_progress_json, get_user_data_dir
    import json
    
    data_dir = get_user_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)
    json_folder = data_dir / "Saved Progress"
    json_folder.mkdir(parents=True, exist_ok=True)
    filepath = json_folder / "Electricity_Generation_Input.json"
    
    with open(filepath, "r") as f:
        electricity_generation_input_dict = json.load(f)
        
    Total_electricity_produced_or_purchased = electricity_generation_input_dict["Total electricity purchased (kWh/year)"] + electricity_generation_input_dict["Electricity generated and used at cement plant (kWh/year)"]
    
    difference_total_process_electricity_and_input_electricity = Total_electricity_produced_or_purchased - Total_electricity
    total_process_electricity_to_input_electricity = abs(difference_total_process_electricity_and_input_electricity) / Total_electricity_produced_or_purchased
    if difference_total_process_electricity_and_input_electricity < 0:
        input_errors.append("Total process electricity input is greater than electricity generated and used at cement plant.")
    elif total_process_electricity_to_input_electricity > 0.05:
        input_errors.append("Total process electricity input is lower than 95% of total electricity generated & used and purchased at cement plant.")
        
    if input_errors:
        QMessageBox.critical(
            self,
            "Input Error",
            "Electricity and total fuel input must both be greater than zero. \nTotal process electricity input should be between 95-100% of electricity generated & used and purchased at cement plant. \nYour total process electricity input is "+str(Total_electricity)+"kWh/year and electricity generated & used and purchased at cement plant is "+str(Total_electricity_produced_or_purchased)+"kWh/year."
        )
        return False

    return True

def validate_inputs_energy_detailed_inputs(self):
    input_errors = []
    from utils.save_progress import load_progress_json, get_user_data_dir
    import json
    
    data_dir = get_user_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)
    json_folder = data_dir / "Saved Progress"
    json_folder.mkdir(parents=True, exist_ok=True)
    filepath = json_folder / "Energy_Input.json"
    
    with open(filepath, "r") as f:
        energy_input_dict = json.load(f)
        
    filepath = json_folder / "Electricity_Generation_Input.json"
    
    with open(filepath, "r") as f:
        electricity_generation_input_dict = json.load(f)
    
    Total_fuel = energy_input_dict["Totals"]["Total process fuel"]
    Total_electricity = energy_input_dict["Totals"]["Total process electricity"]
    
    if Total_fuel == 0:
        input_errors.append("Total fuel input must be greater than zero.")
    
    if Total_electricity == 0:
        input_errors.append("Total electricity input must be greater than zero.")
        
    Total_electricity_produced_or_purchased = electricity_generation_input_dict["Total electricity purchased (kWh/year)"] + electricity_generation_input_dict["Electricity generated and used at cement plant (kWh/year)"]
    
    difference_total_process_electricity_and_input_electricity = Total_electricity_produced_or_purchased - Total_electricity
    total_process_electricity_to_input_electricity = abs(difference_total_process_electricity_and_input_electricity) / Total_electricity_produced_or_purchased
    if difference_total_process_electricity_and_input_electricity < 0:
        input_errors.append("Total process electricity input is greater than electricity generated and used at cement plant.")
    elif total_process_electricity_to_input_electricity > 0.05:
        input_errors.append("Total process electricity input is lower than 95% of total electricity generated & used and purchased at cement plant.")
        
    if input_errors:
        QMessageBox.critical(
            self,
            "Input Error",
            "Electricity and total fuel input must both be greater than zero. \nTotal process electricity input should be between 95-100% of electricity generated & used and purchased at cement plant. \nYour total process electricity input is "+str(Total_electricity)+"kWh/year and electricity generated & used and purchased at cement plant is "+str(Total_electricity_produced_or_purchased)+"kWh/year."
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
    
    def convert_string_to_float(string_input):
        try:
            float_output = float(string_input)
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
            "Please ensure that the total new fuel share must add up to 100%."
        )
        return False

    return True

def validate_inputs_DT_measures(self):
    input_errors = []
    
    list_of_SCM_and_Filler_Measures = [
        self.ui.page_10_comboBox.currentText(),
        self.ui.page_10_comboBox_2.currentText(),
        self.ui.page_10_comboBox_3.currentText(),
        self.ui.page_10_comboBox_4.currentText(),
        self.ui.page_10_comboBox_5.currentText()
        ]
    
    SCM_and_Filler_Measures_count = 0
    for i in list_of_SCM_and_Filler_Measures:
        if i == "Yes (100%)":
            SCM_and_Filler_Measures_count += 1
        elif i == "Yes, Partially":
            SCM_and_Filler_Measures_count += 1
    
    valid_count_input = 1
    
    list_of_CCUS_measures = [
        self.ui.page_10_comboBox_6.currentText(),
        self.ui.page_10_comboBox_7.currentText()
        ]
    
    def convert_string_to_float(string_input):
        try:
            float_output = float(string_input)
        except ValueError:
            float_output = 0
        return float_output
    
    CCUS_measure_sum = convert_string_to_float(self.ui.page_10_input_6.text()) + convert_string_to_float(self.ui.page_10_input_7.text())
    
    for i in list_of_CCUS_measures:
        if i == "Yes (100%)":
            CCUS_measure_sum += 100

    
    list_of_alternative_cement_measures = [
        self.ui.page_10_comboBox_8.currentText(),
        self.ui.page_10_comboBox_9.currentText()
        ]
    
    alternative_cment_measure_sum = convert_string_to_float(self.ui.page_10_input_8.text()) + convert_string_to_float(self.ui.page_10_input_9.text())
    for i in list_of_alternative_cement_measures:
        if i == "Yes (100%)":
            alternative_cment_measure_sum += 100

    valid_sum_input = 100
    
    if SCM_and_Filler_Measures_count > valid_count_input:
        input_errors.append("Only one SCM and Filler measure can be selected")
    
    if CCUS_measure_sum > valid_sum_input:
        input_errors.append("Total CCUS measure must not exceed 100%")
        
    if alternative_cment_measure_sum > valid_sum_input:
        input_errors.append("Total alternative cement measure must not exceed 100%")
    
    if input_errors:
        QMessageBox.critical(
            self,
            "Input Error",
            "Only one SCM and Filler measure can be selected. Total application of CCUS measures and total application of alternative cement measure must both not exceed 100%."
        )
        return False

    return True
        

