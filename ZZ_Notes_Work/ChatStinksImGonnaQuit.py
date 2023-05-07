from bs4 import BeautifulSoup

html_doc = '''
<div id="demographic_questions">
  <strong>U.S. Standard Demographic Questions</strong>

     We invite applicants to share their demographic background. If you choose to complete this survey, your responses may be used to identify areas of improvement in our hiring process.


    <div class="field demographic_question ">
      How would you describe your gender identity? (mark all that apply)
      <span class="select-one">
        
      </span>

      <br>
      <input type="hidden" name="job_application[demographic_answers][][question_id]" value="4012270004">


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4073033004" class="">&nbsp;&nbsp;Man
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4073031004" class="">&nbsp;&nbsp;Non-binary
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4073029004" class="">&nbsp;&nbsp;Woman
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4073027004" class="free-form-checkbox">&nbsp;&nbsp;I prefer to self-describe
        </label>
        <br>

          <div class="free-form-text">
            <input type="text" name="job_application[demographic_answers][][answer_options][][text]" disabled="disabled" maxlength="255" aria-label="I prefer to self-describe" aria-required="false">
          </div>

        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4073025004" class="">&nbsp;&nbsp;I don't wish to answer
        </label>
        <br>

    </div>

    <div class="field demographic_question ">
      How would you describe your racial/ethnic background? (mark all that apply)
      <span class="select-one">
        
      </span>

      <br>
      <input type="hidden" name="job_application[demographic_answers][][question_id]" value="4012268004">


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4073022004" class="">&nbsp;&nbsp;Black or of African descent
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4073021004" class="">&nbsp;&nbsp;East Asian
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4073019004" class="">&nbsp;&nbsp;Hispanic, Latinx or of Spanish Origin
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4073018004" class="">&nbsp;&nbsp;Indigenous, American Indian or Alaska Native
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4073016004" class="">&nbsp;&nbsp;Middle Eastern or North African
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4073014004" class="">&nbsp;&nbsp;Native Hawaiian or Pacific Islander
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4073012004" class="">&nbsp;&nbsp;South Asian
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4073010004" class="">&nbsp;&nbsp;Southeast Asian
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4073009004" class="">&nbsp;&nbsp;White or European
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4073008004" class="free-form-checkbox">&nbsp;&nbsp;I prefer to self-describe
        </label>
        <br>

          <div class="free-form-text">
            <input type="text" name="job_application[demographic_answers][][answer_options][][text]" disabled="disabled" maxlength="255" aria-label="I prefer to self-describe" aria-required="false">
          </div>

        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4073007004" class="">&nbsp;&nbsp;I don't wish to answer
        </label>
        <br>

    </div>

    <div class="field demographic_question ">
      How would you describe your sexual orientation? (mark all that apply)
      <span class="select-one">
        
      </span>

      <br>
      <input type="hidden" name="job_application[demographic_answers][][question_id]" value="4012267004">


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4073004004" class="">&nbsp;&nbsp;Asexual
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4073002004" class="">&nbsp;&nbsp;Bisexual and/or pansexual
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4073001004" class="">&nbsp;&nbsp;Gay
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4072999004" class="">&nbsp;&nbsp;Heterosexual
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4072997004" class="">&nbsp;&nbsp;Lesbian
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4072996004" class="">&nbsp;&nbsp;Queer
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4072994004" class="free-form-checkbox">&nbsp;&nbsp;I prefer to self-describe
        </label>
        <br>

          <div class="free-form-text">
            <input type="text" name="job_application[demographic_answers][][answer_options][][text]" disabled="disabled" maxlength="255" aria-label="I prefer to self-describe" aria-required="false">
          </div>

        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4072992004" class="">&nbsp;&nbsp;I don't wish to answer
        </label>
        <br>

    </div>

    <div class="field demographic_question ">
      Do you identify as transgender?
      <span class="select-one">
        (Select one)
      </span>

      <br>
      <input type="hidden" name="job_application[demographic_answers][][question_id]" value="4012265004">


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4072990004" class="single-select">&nbsp;&nbsp;Yes
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4072989004" class="single-select">&nbsp;&nbsp;No
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4072988004" class="single-select free-form-checkbox">&nbsp;&nbsp;I prefer to self-describe
        </label>
        <br>

          <div class="free-form-text">
            <input type="text" name="job_application[demographic_answers][][answer_options][][text]" disabled="disabled" maxlength="255" aria-label="I prefer to self-describe" aria-required="false">
          </div>

        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4072986004" class="single-select">&nbsp;&nbsp;I don't wish to answer
        </label>
        <br>

    </div>

    <div class="field demographic_question ">
      Do you have a disability or chronic condition (physical, visual, auditory, cognitive, mental, emotional, or other) that substantially limits one or more of your major life activities, including mobility, communication (seeing, hearing, speaking), and learning?
      <span class="select-one">
        (Select one)
      </span>

      <br>
      <input type="hidden" name="job_application[demographic_answers][][question_id]" value="4012264004">


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4072984004" class="single-select">&nbsp;&nbsp;Yes
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4072983004" class="single-select">&nbsp;&nbsp;No
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4072982004" class="single-select free-form-checkbox">&nbsp;&nbsp;I prefer to self-describe
        </label>
        <br>

          <div class="free-form-text">
            <input type="text" name="job_application[demographic_answers][][answer_options][][text]" disabled="disabled" maxlength="255" aria-label="I prefer to self-describe" aria-required="false">
          </div>

        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4072981004" class="single-select">&nbsp;&nbsp;I don't wish to answer
        </label>
        <br>

    </div>

    <div class="field demographic_question ">
      Are you a veteran or active member of the United States Armed Forces?
      <span class="select-one">
        (Select one)
      </span>

      <br>
      <input type="hidden" name="job_application[demographic_answers][][question_id]" value="4012262004">


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4072978004" class="single-select">&nbsp;&nbsp;Yes, I am a veteran or active member
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4072977004" class="single-select">&nbsp;&nbsp;No, I am not a veteran or active member
        </label>
        <br>


        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4072976004" class="single-select free-form-checkbox">&nbsp;&nbsp;I prefer to self-describe
        </label>
        <br>

          <div class="free-form-text">
            <input type="text" name="job_application[demographic_answers][][answer_options][][text]" disabled="disabled" maxlength="255" aria-label="I prefer to self-describe" aria-required="false">
          </div>

        <label>
          <input type="checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" value="4072975004" class="single-select">&nbsp;&nbsp;I don't wish to answer
        </label>
        <br>

    </div>
</div>
'''

# soup = BeautifulSoup(html_doc, 'html.parser')

# form_inputs = []

# for input_element in soup.find_all(['input', 'select', 'textarea']):
#     label = input_element.get('aria-label') or input_element.get('placeholder') or input_element.find_previous('label')
#     label = label.get_text(strip=True) if hasattr(label, 'get_text') else None
#     input_type = input_element.get('type') or input_element.name
#     input_values = []

#     if input_type == 'select' or input_type == 'checkbox':
#         for option in input_element.find_all('option'):
#             input_values.append(option.get_text(strip=True))
#     elif input_type == 'radio':
#         for radio in input_element.find_all('input', type='radio'):
#             input_values.append(radio.get_text(strip=True))

#     form_inputs.append({
#         'label': label,
#         'type': input_type,
#         'values': input_values,
#     })

# for form_input in form_inputs:
#     print(f"{form_input['label']} ({form_input['type']}): {', '.join(form_input['values']) if form_input['values'] else 'N/A'}")



'''

soup = BeautifulSoup(html_doc, 'html.parser')

form_inputs = []

for input_element in soup.find_all(['input', 'select', 'textarea']):
    input_type = input_element.get('type') or input_element.name

    if input_type == 'checkbox':
        fieldset = input_element.find_parent('fieldset')
        if fieldset:
            label = fieldset.find_previous('legend') if fieldset else None
            label = label.get_text(strip=True) if label else None

            input_values = []
            for checkbox in fieldset.find_all('input', type='checkbox'):
                value = checkbox.find_next_sibling('label')
                value = value.get_text(strip=True) if value else None
                input_values.append(value)

            form_inputs.append({
                'label': label,
                'type': input_type,
                'values': input_values,
                'html': str(fieldset)
            })

for form_input in form_inputs:
    print(f"Input {form_inputs.index(form_input) + 1}:")
    print(f"  Label: {form_input['label']}")
    print(f"  Type: {form_input['type']}")
    print(f"  Values: {form_input['values']}")
    print(f"  HTML: {form_input['html']}\n")


print(form_inputs)


































# Field: <input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073033004"/>
# Checkbox group: [<input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073033004"/>, <input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073031004"/>, <input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073029004"/>, <input class="free-form-checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073027004"/>, <input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073025004"/>, <input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073022004"/>, <input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073021004"/>, <input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073019004"/>, <input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073018004"/>, <input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073016004"/>, <input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073014004"/>, <input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073012004"/>, <input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073010004"/>, <input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073009004"/>, <input class="free-form-checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073008004"/>, <input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073007004"/>, <input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073004004"/>, <input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073002004"/>, <input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073001004"/>, <input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072999004"/>, <input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072997004"/>, <input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072996004"/>, <input class="free-form-checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072994004"/>, <input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072992004"/>, <input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072990004"/>, <input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072989004"/>, <input class="single-select free-form-checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072988004"/>, <input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072986004"/>, <input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072984004"/>, <input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072983004"/>, <input class="single-select free-form-checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072982004"/>, <input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072981004"/>, <input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072978004"/>, <input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072977004"/>, <input class="single-select free-form-checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072976004"/>, <input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072975004"/>]
# Checkbox options: []
# Field: <input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073033004"/>
# Tyrants
# SPACE people in space! Fowl
# Form input details: [{'label': 'First Name *', 'type': 'text', 'values': [], 'is_hidden': False, 'html': '<input aria-required="true" autocomplete="given-name" id="first_name" maxlength="255" name="job_application[first_name]" type="text"/>', 'dynamic': False, 'related_elements': []}, {'label': 'Last Name *', 'type': 'text', 'values': [], 'is_hidden': False, 'html': '<input aria-required="true" autocomplete="family-name" id="last_name" maxlength="255" name="job_application[last_name]" type="text"/>', 'dynamic': False, 'related_elements': []}, {'label': 'Email *', 'type': 'text', 'values': [], 'is_hidden': False, 'html': '<input aria-required="true" autocomplete="email" id="email" maxlength="255" name="job_application[email]" type="text"/>', 'dynamic': False, 'related_elements': []}, {'label': 'Phone *', 'type': 'text', 'values': [], 'is_hidden': False, 'html': '<input aria-required="true" autocomplete="tel" id="phone" maxlength="255" name="job_application[phone]" required="required" type="text"/>', 'dynamic': False, 'related_elements': []}, {'label': '', 'type': 'text', 'values': [], 'is_hidden': False, 'html': '<input autocomplete="off" id="dev-field-1" maxlength="255" name="dev_field_1" type="text"/>', 'dynamic': False, 'related_elements': []}, {'label': None, 'type': 'button', 'values': [], 'is_hidden': False, 'html': '<button aria-label="Remove attachment" class="unstyled-button remove" name="button" type="button"><img alt="Remove attachment" height="11" src="https://boards.cdn.greenhouse.io/assets/cancellation/x-00cb7c69bded92bc90f03e0028a3457a4905b1e28c8a7fe16b792086c4288c29.png" width="11"/></button>', 'dynamic': False, 'related_elements': []}, {'label': None, 'type': 'button', 'values': [], 'is_hidden': False, 'html': '<button aria-describedby="resume-allowable-file-types" class="unstyled-button link-button" data-source="attach" name="button" type="button">Attach</button>', 'dynamic': False, 'related_elements': []}, {'label': None, 'type': 'button', 'values': [], 'is_hidden': False, 'html': '<button aria-pressed="false" class="unstyled-button link-button" data-source="paste" name="button" type="button">or enter manually</button>', 'dynamic': False, 'related_elements': []}, {'label': None, 'type': 'textarea', 'values': [], 'is_hidden': False, 'html': '<textarea class="paste" id="resume_text" name="job_application[resume_text]" title="Enter manually">\n</textarea>', 'dynamic': False, 'related_elements': []}, {'label': 'LinkedIn Profile *', 'type': 'text', 'values': [], 'is_hidden': False, 'html': '<input aria-required="true" autocomplete="custom-question-linkedin-profile" id="job_application_answers_attributes_0_text_value" maxlength="255" name="job_application[answers_attributes][0][text_value]" type="text"/>', 'dynamic': False, 'related_elements': []}, {'label': 'Would you feel comfortable moving forward with a compensation range of $175-200k? *', 'type': 'select', 'values': ['--', 'Yes', 'No'], 'is_hidden': False, 'html': '<select aria-required="true" id="job_application_answers_attributes_1_boolean_value" name="job_application[answers_attributes][1][boolean_value]"><option value="">--</option>\n<option value="1">Yes</option>\n<option value="0">No</option></select>', 'dynamic': False, 'related_elements': []}, {'label': 'We respect the law and value the health and safety of our colleagues. Accordingly, we require all employees, regardless of location, to take a covid rapid test before entering the office. Are you able to comply with this if you were to be gainfully employed by the company? *', 'type': 'select', 'values': ['--', 'Yes', 'No'], 'is_hidden': False, 'html': '<select aria-required="true" id="job_application_answers_attributes_2_boolean_value" name="job_application[answers_attributes][2][boolean_value]"><option value="">--</option>\n<option value="1">Yes</option>\n<option value="0">No</option></select>', 'dynamic': False, 'related_elements': []}, {'label': 'Would you be willing to visit our office 3-4x per year? (company sponsored) *', 'type': 'select', 'values': ['Please select', 'Yes', 'Perhaps', 'No'], 'is_hidden': False, 'html': '<select aria-required="true" id="job_application_answers_attributes_3_answer_selected_options_attributes_3_question_option_id" name="job_application[answers_attributes][3][answer_selected_options_attributes][3][question_option_id]" style="width: 200px;"><option value="">Please select</option><option value="27691651004">Yes</option>\n<option value="27691652004">Perhaps</option>\n<option value="27691653004">No</option></select>', 'dynamic': False, 'related_elements': []}, {'label': 'Are you authorized to work lawfully in the United States for our company? *', 'type': 'select', 'values': ['Please select', 'Yes', 'No'], 'is_hidden': False, 'html': '<select aria-required="true" id="job_application_answers_attributes_4_answer_selected_options_attributes_4_question_option_id" name="job_application[answers_attributes][4][answer_selected_options_attributes][4][question_option_id]" style="width: 200px;"><option value="">Please select</option><option value="27691654004">Yes</option>\n<option value="27691655004">No</option></select>', 'dynamic': False, 'related_elements': []}, {'label': 'Will you now or in the future require the company to sponsor an immigration case in order to employ you (for example, H-1B, STEM-OPT or other employment-based immigration case)? *', 'type': 'select', 'values': ['--', 'Yes', 'No'], 'is_hidden': False, 'html': '<select aria-required="true" id="job_application_answers_attributes_5_boolean_value" name="job_application[answers_attributes][5][boolean_value]"><option value="">--</option>\n<option value="1">Yes</option>\n<option value="0">No</option></select>', 'dynamic': False, 'related_elements': []}, {'label': None, 'type': 'checkbox', 'values': [], 'is_hidden': False, 'html': '<input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073033004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073031004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073029004"/><input class="free-form-checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073027004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073025004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073022004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073021004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073019004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073018004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073016004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073014004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073012004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073010004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073009004"/><input class="free-form-checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073008004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073007004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073004004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073002004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073001004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072999004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072997004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072996004"/><input class="free-form-checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072994004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072992004"/><input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072990004"/><input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072989004"/><input class="single-select free-form-checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072988004"/><input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072986004"/><input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072984004"/><input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072983004"/><input class="single-select free-form-checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072982004"/><input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072981004"/><input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072978004"/><input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072977004"/><input class="single-select free-form-checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072976004"/><input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072975004"/>', 'dynamic': False, 'related_elements': []}, {'label': None, 'type': 'text', 'values': [], 'is_hidden': False, 'html': '<input aria-label="I prefer to self-describe" aria-required="false" disabled="disabled" maxlength="255" name="job_application[demographic_answers][][answer_options][][text]" type="text"/>', 'dynamic': False, 'related_elements': []}, {'label': None, 'type': 'text', 'values': [], 'is_hidden': False, 'html': '<input aria-label="I prefer to self-describe" aria-required="false" disabled="disabled" maxlength="255" name="job_application[demographic_answers][][answer_options][][text]" type="text"/>', 'dynamic': False, 'related_elements': []}, {'label': None, 'type': 'text', 'values': [], 'is_hidden': False, 'html': '<input aria-label="I prefer to self-describe" aria-required="false" disabled="disabled" maxlength="255" name="job_application[demographic_answers][][answer_options][][text]" type="text"/>', 'dynamic': False, 'related_elements': []}, {'label': None, 'type': 'text', 'values': [], 'is_hidden': False, 'html': '<input aria-label="I prefer to self-describe" aria-required="false" disabled="disabled" maxlength="255" name="job_application[demographic_answers][][answer_options][][text]" type="text"/>', 'dynamic': False, 'related_elements': []}, {'label': None, 'type': 'text', 'values': [], 'is_hidden': False, 'html': '<input aria-label="I prefer to self-describe" aria-required="false" disabled="disabled" maxlength="255" name="job_application[demographic_answers][][answer_options][][text]" type="text"/>', 'dynamic': False, 'related_elements': []}, {'label': None, 'type': 'text', 'values': [], 'is_hidden': False, 'html': '<input aria-label="I prefer to self-describe" aria-required="false" disabled="disabled" maxlength="255" name="job_application[demographic_answers][][answer_options][][text]" type="text"/>', 'dynamic': False, 'related_elements': []}, {'label': 'Submit Application', 'type': 'button', 'values': [], 'is_hidden': False, 'html': '<input class="button" id="submit_app" type="button" value="Submit Application"/>', 'dynamic': False, 'related_elements': []}]












































def get_label(self, input_element):
        # Check for the special case: 'button' and 'submit application' in input_element
        input_element_str = str(input_element).lower()
        if 'button' in input_element_str and 'submit application' in input_element_str:
            return 'Submit Application'
        
        if input_element.get('type') == 'radio':
            label = self.find_radio_label(input_element)
            return label
        
        if input_element.get('type') == 'checkbox':
            main_label = self.get_main_label(input_element)
            return main_label

        label = None

        # Case 1: Check if the label is a direct previous sibling of the input element
        label = input_element.find_previous_sibling('label')

        # Case 2: Check if the label is inside a parent container
        if not label:
            parent = input_element.find_parent()
            if parent:
                label = parent.find('label')

        # Case 3: Check if the label is associated using the "for" attribute
        if not label:
            input_id = input_element.get('id')
            if input_id:
                label = input_element.find_previous('label', attrs={'for': input_id})

        # Case 4: Check if the input element is a child of a label element
        if not label:
            parent_label = input_element.find_parent('label')
            if parent_label:
                label = parent_label

        # Case 5: Check if a label is inside a parent container of the input element
        if not label:
            parent = input_element.find_parent()
            if parent:
                label = parent.find('label')

        # Check if the label contains a nested div element with the class "application-label" (case for Input 18)
        if label:
            app_label = label.find(lambda tag: 'class' in tag.attrs and 'application-label' in tag['class'])
            if app_label:
                label = app_label

        if label:
            label_text = label.text.strip()

            # If the standard asterisk (*) or fullwidth asterisk (✱) is present, remove everything after it
            if '*' in label_text:
                label_text = label_text.split('*')[0].strip() + ' *'
            elif '✱' in label_text:
                label_text = label_text.split('✱')[0].strip() + ' ✱'
            else:
                # If the newline character (\n) is present, remove it and everything after it
                label_text = label_text.split('\n')[0].strip()

            return label_text

        # Case 6: Check if the input_element has a placeholder attribute
        placeholder = input_element.get('placeholder')
        if placeholder:
            return f"Placeholder ~ {placeholder}"

        return None
    
    def find_radio_label(self, element, stop_level=5):
        current_level = 0
        while (current_level <= stop_level):
            print(f"Level {current_level}:")
            if current_level == 0 or current_level == 5:
                if current_level == 0:
                    print(element.prettify())
                if current_level == 5:
                    sauce = element.next_element.get_text(strip=True)
                    print(sauce)
                    return sauce
            element = element.parent
            current_level += 1

    def get_main_label(self, field):
        label = field.find_previous_sibling('label')
        if label:
            print(f"Main label: {label.text.strip()}")
            return label.get_text(strip=True)
        return None

    def get_checkbox_options(self, checkbox_group):
        options = []
        for checkbox in checkbox_group:
            option_label = checkbox.find_next_sibling('label')
            if option_label:
                options.append(option_label.get_text(strip=True))
        print(f"Checkbox options: {options}")
        return options

    def get_form_input_details(self, url):
        print("\nget_form_input_details()")
        print("URL = " + url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'lxml')

        form_fields = soup.find_all(['input', 'textarea', 'button', 'select'])

        form_input_details = []
        processed_radios = set()

        for i, field in enumerate(form_fields, start=1):
            input_type = field.get('type')
            input_id = field.get('id')
            input_label = ''
            is_hidden = field.get('style') == 'display: none;' or input_type == 'hidden'
            input_html = str(field).strip()

            if field.name == 'button':
                input_type = 'button'
                # Skip captcha buttons
                if 'h-captcha' in field.get('class', []) or 'g-recaptcha' in field.get('class', []):
                    continue
            elif field.name == 'textarea':
                input_type = 'textarea'
            elif field.name == 'select':
                input_type = 'select'

            # Add a check for the input types you want to keep
            if input_type not in ['text', 'email', 'password', 'select', 'radio', 'checkbox', 'textarea', 'button'] and input_id != 'education_school_name':
                continue

            values = []
            if input_type == 'select':
                options = field.find_all('option')
                for option in options:
                    values.append(option.text.strip())

            if input_type == 'radio':
                #print("Radio button in get_form_input_details:", field)  # Debugging line
                radio_name = field.get('name')
                if radio_name in processed_radios:
                    continue
                processed_radios.add(radio_name)
                radio_group = soup.find_all('input', {'name': radio_name})
                values = [radio.get('value') for radio in radio_group]
                input_html = ''.join([str(radio).strip() for radio in radio_group])
                
            elif input_type == 'checkbox':
                checkbox_name = field.get('name')
                if checkbox_name in processed_radios:
                    continue
                processed_radios.add(checkbox_name)
                
                # Call get_main_label for the entire checkbox group
                input_label = self.get_main_label(field)
                
                checkbox_group = soup.find_all('input', {'name': checkbox_name})
                #values = [checkbox.get('value') for checkbox in checkbox_group]
                values = self.get_checkbox_options(checkbox_group)
                input_html = ''.join([str(checkbox).strip() for checkbox in checkbox_group])
                
                # Call get_label for the entire radio button group
                input_label = self.get_label(field)
            else:
                # Call get_label for other input types
                input_label = self.get_label(field)

            # Skip hidden fields without a label
            if is_hidden and not input_label:
                continue

            is_dynamic = False
            related_elements = []

            # Check the field's ancestors for the 'data-show-if' attribute and 'display: none;' style
            current_element = field
            while current_element:
                if current_element.has_attr('data-show-if'):
                    is_dynamic = True
                    related_elements = [
                        {
                            'related_field_id': current_element['data-show-if'].split('==')[0],
                            'trigger_value': current_element['data-show-if'].split('==')[1],
                        }
                    ]
                if current_element.get('style', '') == 'display: none;':
                    is_hidden = True
                current_element = current_element.find_parent()

            form_input_details.append({
                'label': input_label,
                'type': input_type,
                'values': values,
                'is_hidden': is_hidden,
                'html': input_html,
                'dynamic': is_dynamic,
                'related_elements': related_elements,
            })
        self.print_form_details(form_input_details)
        time.sleep(6)
        return form_input_details
'''











'''

ok I made my code cleaner
but unfortunately I still didn't get my desired output. This was the output that the terminal just returned
Input 15:
  Label: Will you now or in the future require the company to sponsor an immigration case in order to employ you (for example, H-1B, STEM-OPT or other employment-based immigration case)? *
  Type: select
  Values: ['--', 'Yes', 'No']
  Is Hidden: False
  HTML: <select aria-required="true" id="job_application_answers_attributes_5_boolean_value" name="job_application[answers_attributes][5][boolean_value]"><option value="">--</option>
<option value="1">Yes</option>
<option value="0">No</option></select>
  Dynamic: False
  Related Elements: []
Input 16:
  Label: None
  Type: checkbox
  Values: []
  Is Hidden: False
  HTML: <input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073033004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073031004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073029004"/><input class="free-form-checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073027004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073025004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073022004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073021004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073019004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073018004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073016004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073014004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073012004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073010004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073009004"/><input class="free-form-checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073008004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073007004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073004004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073002004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4073001004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072999004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072997004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072996004"/><input class="free-form-checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072994004"/><input class="" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072992004"/><input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072990004"/><input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072989004"/><input class="single-select free-form-checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072988004"/><input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072986004"/><input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072984004"/><input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072983004"/><input class="single-select free-form-checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072982004"/><input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072981004"/><input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072978004"/><input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072977004"/><input class="single-select free-form-checkbox" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072976004"/><input class="single-select" name="job_application[demographic_answers][][answer_options][][answer_option_id]" type="checkbox" value="4072975004"/>
  Dynamic: False
  Related Elements: []
Input 17:
  Label: None
  Type: text
  Values: []
  Is Hidden: False
  HTML: <input aria-label="I prefer to self-describe" aria-required="false" disabled="disabled" maxlength="255" name="job_application[demographic_answers][][answer_options][][text]" type="text"/>
  Dynamic: False
  Related Elements: []
Input 18:
  Label: None
  Type: text
  Values: []
  Is Hidden: False
  HTML: <input aria-label="I prefer to self-describe" aria-required="false" disabled="disabled" maxlength="255" name="job_application[demographic_answers][][answer_options][][text]" type="text"/>
  Dynamic: False
  Related Elements: []
Input 19:
  Label: None
  Type: text
  Values: []
  Is Hidden: False
  HTML: <input aria-label="I prefer to self-describe" aria-required="false" disabled="disabled" maxlength="255" name="job_application[demographic_answers][][answer_options][][text]" type="text"/>
  Dynamic: False
  Related Elements: []
Input 20:
  Label: None
  Type: text
  Values: []
  Is Hidden: False
  HTML: <input aria-label="I prefer to self-describe" aria-required="false" disabled="disabled" maxlength="255" name="job_application[demographic_answers][][answer_options][][text]" type="text"/>
  Dynamic: False
  Related Elements: []
Input 21:
  Label: None
  Type: text
  Values: []
  Is Hidden: False
  HTML: <input aria-label="I prefer to self-describe" aria-required="false" disabled="disabled" maxlength="255" name="job_application[demographic_answers][][answer_options][][text]" type="text"/>
  Dynamic: False
  Related Elements: []
Input 22:
  Label: None
  Type: text
  Values: []
  Is Hidden: False
  HTML: <input aria-label="I prefer to self-describe" aria-required="false" disabled="disabled" maxlength="255" name="job_application[demographic_answers][][answer_options][][text]" type="text"/>
  Dynamic: False
  Related Elements: []
Input 23:
  Label: Submit Application
  Type: button
  Values: []
  Is Hidden: False
  HTML: <input class="button" id="submit_app" type="button" value="Submit Application"/>
  Dynamic: False
  Related Elements: []
--------------------------------------------
so what do I need to change to get my desired output

'''