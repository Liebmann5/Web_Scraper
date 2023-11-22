Everything in Form directory

    def insert_resume(self):
        print("\ninsert_resume()")
        resume_path = self.users_information.get('RESUME_PATH')
        print(resume_path)
        if self.application_company_name == 'greenhouse':
            element = self.browser.find_element(By.XPATH, "//button[text()='Attach']")
            #element = self.browser.find_element(By.XPATH, "//button[contains(text, 'ATTACH')]")
            #element = self.browser.find_elements(By.ID, "application")
            print(element)
            if not element:
                element = self.browser.find_element(By.CLASS_NAME, "resume")
                print(element)
            if not element:
                element = self.browser.find_element(By.XPATH, "//button[text()='Attach']")
                print(element)
            if not element:
                print("That's so silly! Can't scroll")
            self.browser.execute_script("arguments[0].scrollIntoView();", element)
        resume_file_input = self.browser.find_elements(By.XPATH, '//input[data-qa="input-resume"]')
        print(resume_file_input)
        if resume_file_input:
            resume_file_input[0].send_keys(resume_path)
        else:
            self.dismiss_random_popups()
                        #self.browser.execute_script("arguments[0].scrollIntoView();", resume_file_input)
            #resume_upload_button = self.browser.find_element(By.CSS_SELECTOR, 'button.visible-resume-upload')
            #resume_upload_button = self.browser.find_element(By.CSS_SELECTOR, 'button[aria-describedby="resume-allowable-file-types"]')
            wait = WebDriverWait(self.browser, 10)
            #overlay_close_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.close-overlay')))
            #overlay_close_button.click()
            resume_upload_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-describedby="resume-allowable-file-types"]')))
            print("--------------------------------------------------------")
            print(f"resume_upload_button = {resume_upload_button}")
            print("--------------------------------------------------------")
            #print()
            print("6")
            if resume_upload_button:
                time.sleep(1)
                print("8")
                input_elements = self.get_input_tag_elements()
                input_element, is_visible = self.find_visible_input('input[type="file"]')
                print("Bargain-Mart")
                print((input_element, is_visible))
                
                upload_input = self.browser.find_element(By.CSS_SELECTOR, 'input[type="file"]')
                upload_input.send_keys(resume_path)
            else:
                raise Exception('Could not find resume upload element')
        return

    def get_label(self, input_element):
        # Check for the special case: 'button' and 'submit application' in input_element
        input_element_str = str(input_element).lower()
        if 'button' in input_element_str and 'submit application' in input_element_str:
            return 'Submit Application'
        
        if input_element.get('type') == 'radio':
            label = self.find_radio_label(input_element)
            return label
        
        if input_element.get('type') == 'checkbox':
            div_parent, parents_text = self.get_div_parent(input_element)
            if div_parent == 'None' or parents_text == 'None':
                pass
            elif div_parent and parents_text:
                #return div_parent, parents_text
                checkbox_values = [div_parent, parents_text]
                return checkbox_values

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
                
        # Case 6: Checks if the input element has an 'aria-label' meaning it's dynamic so goes & searches
        # all previous label containers to see if any have text values that are equal to the aria-label' 
        if not label:
            if 'aria-label' in input_element.attrs:
                aria_label_match = None
                parent_label = input_element.find_previous('label')
                aria_label_value = input_element["aria-label"]
                if parent_label.text.strip() == aria_label_value:
                    aria_label_match = True
                if aria_label_match:
                    dynamic_label = aria_label_value + " (dynamic " + input_element.get('type') + ")"
                    if dynamic_label:
                        return dynamic_label
                elif aria_label_match == None:
                    return aria_label_value
                        
        # Case 7: Checks if the input element's style attribute is equal to 'display: none;' meaning it's
        # dynamic so goes & searches for the most previous label container to specify its text value is dynamic
        if not label:
            if input_element.get('style') == 'display: none;':
                previous_input = input_element.find_previous('input')
                if previous_input:
                    parent_label = previous_input.find_previous('label')
                    dynamic_label = parent_label.text.strip() + " (dynamic " + input_element.get('type') + ")"
                    if dynamic_label:
                        return dynamic_label
                    
        # Case 8: Special case for Resume/CV
        if not label and self.one_resume_label == False:
            found_attach = False
            parent_label = input_element.find_previous('label')
            label = parent_label
            self.one_resume_label = True
            
            current_element = input_element
            while current_element:
                if isinstance(current_element, NavigableString) and 'attach' in str(current_element).lower():
                    found_attach = True
                    break
                current_element = current_element.next_sibling
            # Traverse up from the specific_element and find the label tag
            if found_attach:
                label_tag = input_element.find_previous('label')
                if label_tag:
                    # Check if the immediate child is a text value
                    first_child = label_tag.contents[0]
                    if isinstance(first_child, NavigableString) and first_child.strip():
                        holey_holes = first_child.strip()
                    else:
                        # Check if it has a child element and if it does, save that child's text value
                        for child in label_tag.children:
                            if not isinstance(child, NavigableString):
                                holey_holes = child.get_text(strip=True)
                                break
                    label = holey_holes
            else:
                print("No sibling found with the 'attach' keyword.")

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

    def get_div_parent(self, input_element):
        parent_element = input_element.find_previous(lambda tag: any('question' in class_name for class_name in tag.get('class', [])))
        if parent_element:
            current_element = parent_element.next_element
            while current_element:
                if isinstance(current_element, NavigableString) and current_element.strip():
                    parents_text = current_element.strip()
                    break
                current_element = current_element.next_element
        else:
            print("tisk tisk!")
            
        input_tags = input_element.name
        correct_parent = None
        count = 0
        while correct_parent:
            correct_parent = parent_element.find_all(input_tags)
            if correct_parent:
                parent_element = correct_parent
                break
            parent_element = parent_element.next_sibling
            if count > 4:
                break
            print(count)
            count =+ 1
        return parent_element, parents_text

    def get_form_input_details(self, url):
        self.one_resume_label = False
        
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
            if input_type not in ['text', 'email', 'password', 'select', 'radio', 'checkbox', 'textarea', 'button', 'file'] and input_id != 'education_school_name':
                continue

            values = []
            if input_type == 'select':
                options = field.find_all('option')
                for option in options:
                    values.append(option.text.strip())

            if input_type == 'radio':
                radio_name = field.get('name')
                if radio_name in processed_radios:
                    continue
                processed_radios.add(radio_name)
                radio_group = soup.find_all('input', {'name': radio_name})
                values = [radio.get('value') for radio in radio_group]
                input_html = ''.join([str(radio).strip() for radio in radio_group])
                
                # Call get_label for the entire radio button group
                input_label = self.get_label(field)
                
            elif input_type == 'checkbox':
                if field in processed_radios:
                    continue
                #div_parent, parents_text = self.get_label(field)
                checkbox_values = self.get_label(field)
                div_parent = checkbox_values[0]
                print("div_parent = ", div_parent)
                parents_text = checkbox_values[1]
                print("parents_text = ", parents_text)
                values = []
                input_label = parents_text
                checkbox_group = div_parent.find_all('input', {'type': [input_type, "text", "textarea"]})
                input_html = ''.join([str(checkbox).strip() for checkbox in checkbox_group])
                for index, input_element in enumerate(checkbox_group):
                    parent_label = input_element.find_previous('label')
                    if input_element.get('type') == 'text':
                        values.append(parent_label.text.strip() + "(dynamic)")
                        continue
                    values.append(parent_label.text.strip())
                    processed_radios.add(input_element)

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
        print("Tyrants")
        time.sleep(6)
        self.print_form_details(form_input_details)
        return form_input_details
    
    def print_form_details(self, form_inputs):
        print('\n\n\n')

        print('--------------------------------------------')
        print("Form Input Details: ", end="")
        for i, detail in enumerate(form_inputs, start=1):
            print(f"Input {i}:")
            print(f"  Label: {detail['label']}")
            print(f"  Type: {detail['type']}")
            print(f"  Values: {detail['values']}")
            print(f"  Is Hidden: {detail['is_hidden']}")
            print(f"  HTML: {detail['html']}")
            print(f"  Dynamic: {detail['dynamic']}")
            print(f"  Related Elements: {detail['related_elements']}")
        print('--------------------------------------------')
        print("\n")

    def get_input_tag_elements(self):
        input_elements = self.browser.find_elements(By.TAG_NAME, 'input')
        inputs_info = []
        for input_element in input_elements:
            input_id = input_element.get_attribute('id')
            input_type = input_element.get_attribute('type')
            is_hidden = input_element.get_attribute('type') == 'hidden' or not input_element.is_displayed()
            inputs_info.append((input_id, input_type, is_hidden))
        return inputs_info

    def find_visible_input(self, selector):
        input_element = self.browser.find_element(By.CSS_SELECTOR, selector)
        is_hidden = input_element.get_attribute('type') == 'hidden' or not input_element.is_displayed()
        if is_hidden:
            self.browser.execute_script("arguments[0].style.display = 'block';", input_element)
            is_hidden = input_element.get_attribute('type') == 'hidden' or not input_element.is_displayed()
        return input_element, not is_hidden

    def fill_that_form(self):
        #if self.form_input_extended['mandatory'] is True and (self.form_input_extended['env_values'] or self.form_input_extended['env_html']):
        # ^ the purpose of the if is b/c...  if we don't need(['mandatory']) to do the question then we don't!!!!
        print("fill_that_form()")
        if self.form_input_extended['env_key'] and self.form_input_extended['env_values']:
            print('\n\n')
            print(self.form_input_extended)
            print('\n\n')
            time.sleep(1)

            element = self.form_input_extended['env_html']
            value = self.form_input_extended['env_values'][0]
            print("element = ", element)
            print("value = ", value)
            success = self.troubleshoot_form_filling(element, value)
            if not success:
                print("Failed to fill in the form. See the error messages above for details.")
            else:
                print("Successfully filled in the form.")
            
            #This  v  checks if the "value" is 'empty' or 'None'
            #if self.form_input_extended['bc_nick_said']:
            if 'bc_nick_said' in self.form_input_extended:
                if self.form_input_extended['bc_nick_said'] == True:
                    pass
                elif self.form_input_extended['bc_nick_said'] == False:
                    print("Release the hounds Mr. Smithers...")
                    #self.form_input_extended['bc_nick_said'] == False
                    return

            if self.form_input_extended['text'] is True:
                #for form_input_answer in self.form_input_extended['env_values']:
                #form_input_answer = self.form_input_extended['env_values']
                print("MADE IT INTO [TEXT] - MADE IT INTO [TEXT] - MADE IT INTO [TEXT] - MADE IT INTO [TEXT]")
                for form_input_ans in self.form_input_extended['env_values']:
                    print("form_input_ans = ", form_input_ans)
                    form_input_answer = form_input_ans
                form_input_html = self.form_input_extended['env_html']
                
                if form_input_answer:
                    #form_input_html.click()
                    #self.browser.form_input_html.send_keys(form_input_answer)
                    #self.form_input_html.send_keys(form_input_answer)
                    form_input_html.send_keys(form_input_answer)
                    print("Text should be inserted => ", form_input_answer)
                    time.sleep(3)
                    return
                
            elif self.form_input_extended['select'] is True:
                #form_input_answer = self.form_input_extended['env_values']
                for form_input_ans in self.form_input_extended['env_values']:
                    print("form_input_ans = ", form_input_ans)
                    form_input_answer = form_input_ans
                
                if answer:
                    form_input_html = self.form_input_extended['env_html']
                    input_select_element = self.form_input_html.find_element(By.TAG_NAME, "input")
                    #select_button = self.form_input_extended(By.)

                    input_select_element.click()
                    answer = form_input_html.find_element(By.ID, form_input_answer)
                    answer.click()
                    return
                elif form_input_answer is None:
                    form_input_html = self.form_input_extended['env_html']
                    input_select_element = self.form_input_html.find_element(By.TAG_NAME, "input")
                    
                    input_select_element.click()
                    self.input_select_element.send_keys(By.TEXT, form_input_answer)
                    self.send_keys("ENTER")
                    if input_select_element == form_input_answer:
                        return
                    elif input_select_element is None:
                        print("Try pressing the `down-arrow` key and then click `ENTER`!!")
                        print("Otherwise click the correct school!")
                    elif input_select_element is not form_input_answer:
                        raise BreakLoopException
                        
            if self.form_input_extended['radio'] is True:
                form_input_answer = self.form_input_extended['env_values']
                form_input_html = self.form_input_extended['env_html']
                
                answer = form_input_html.find_element(By.ID, form_input_answer)
                if answer:
                    answer.click()
                    return
                elif answer is None:
                    answer = self.browser.find_element(By.TEXT, form_input_answer)
                    if answer:
                        answer.click()
                    elif answer is None:
                        print("Ummmm I have no clue about this [radio] call the police maybe??")
                        
            if self.form_input_extended['checkbox'] is True:
                #TODO: Utilize the `select_all` || `select_one` from  self.form_input_extended['']
                form_input_answer = self.form_input_extended['env_values']
                form_input_html = self.form_input_extended['env_html']
                
                answer = form_input_html.find_element(By.ID, form_input_answer)
                if answer:
                    answer.click()
                    return
                elif answer is None:
                    answer = self.browser.find_element(By.TEXT, form_input_answer)
                    if answer:
                        answer.click()
                    elif answer is None:
                        print("Ummmm I have no clue about this [checkbox] call the police maybe??")
                        
            if self.form_input_extended['button'] is True:
                form_input_answer = self.form_input_extended['env_values']
                form_input_html = self.form_input_extended['env_html']
                
                answer = form_input_html.find_element(By.ID, form_input_answer)
                if answer:
                    answer.click()
                    return
                elif answer is None:
                    answer = self.browser.find_element(By.TEXT, form_input_answer)
                    if answer:
                        answer.click()
                    elif answer is None:
                        print("Ummmm I have no clue about this [checkbox] call the police maybe??")
                        
            elif self.form_input_extended['file'] is True:
                form_input_answer = self.form_input_extended['env_values']
                form_input_html = self.form_input_extended['env_html']
                
                answer = form_input_html.find_element(By.ID, form_input_answer)
                if answer:
                    answer.click()
                    return
                elif answer is None:
                    answer = self.browser.find_element(By.TEXT, form_input_answer)
                    if answer:
                        answer.click()
                    elif answer is None:
                        print("Ummmm I have no clue about this [file] call the police maybe??")
                        
        if self.form_input_extended['mandatory'] is True and not self.form_input_extended['env_values']:
            if self.max_similarity < .25:
                print("prompt user to answer!!!")
            else:
                #Skips the form
                raise BreakLoopException

    def print_form_input_extended(self):
        print("\n\n\ndouble_check_before_fill_in_form()")
        print('--------------------------------------------')
        print("Form Input Extended: ")
        for key, value in self.form_input_extended.items():
            print(f"{key}: {value}")
        print('--------------------------------------------')
        print("\n")
    
    def extract_css(self, input_data_html):
        soup = BeautifulSoup(input_data_html, 'lxml')
        print("soup = ", soup)
        body_children = soup.body.contents
        for child in body_children:
            print('element = ', child)
            if child.get('id'):
                identifier = child.get('id')
                css_selector = f'#{identifier}'
            elif child.get('class'):
                identifier = child.get('class')[0]
                css_selector = f'.{identifier}'
            else:
                raise ValueError('The element does not have an id or a class')
            elemental = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        return elemental

    def scroll_to_question(self, input_data_html):
        print("\nscroll_to_question()")
        soup = BeautifulSoup(input_data_html, 'lxml')
        print("soup = ", soup)

        body_children = soup.body.contents
        for child in body_children:
            print('element = ', child)

            if child.get('id'):
                identifier = child.get('id')
                css_selector = f'#{identifier}'
            elif child.get('class'):
                identifier = child.get('class')[0]
                css_selector = f'.{identifier}'
            else:
                raise ValueError('The element does not have an id or a class')

            elemental = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

            self.browser.execute_script("arguments[0].scrollIntoView();", elemental)

    def troubleshoot_form_filling(self, element, value):
        try:
            # Check if the value is not None or empty
            if not value:
                print("Error: Value is None or empty")
                return False

            # Check if the element is present
            if element is None:
                print("Error: Element is None")
                return False

            # Check if the element is an input field
            if element.tag_name.lower() != 'input':
                print(f"Error: Element is not an input field, it's a {element.tag_name}")
                return False

            # Check if the element has the correct attributes
            if element.get_attribute('name') != 'job_application[phone]':
                print("Error: Element has incorrect name attribute")
                return False

            # Check if the element is displayed (visible to the user)
            if not element.is_displayed():
                print("Error: Element is not displayed")
                return False

            # Check if the element is enabled (interactable)
            if not element.is_enabled():
                print("Error: Element is not enabled")
                return False

            # Try to fill in the form
            element.clear()
            element.send_keys(value)
            print(f"Success: Filled in the form with {value}")

            return True
        except Exception as e:
            print(f"Error: An exception occurred: {e}")
            return False

    def init_form_input_extended(self):
        self.form_input_extended = {
            "mandatory": False,
            "text": False,
            "select": False,
            "radio": False,
            "checkbox": False,
            "button": False,
            "file": False,
            "select all": False,
            "select one": False,
            "dynamic": False,
            "env_key": None,
            "env_values": [],
            "env_html": None
        }

    def process_text(self, text):
        print("process_text()")
        if "*" in text or "✱" in text:
            self.form_input_extended['mandatory'] = True
        if 'select one' in text.lower():
            self.form_input_extended['select one'] = True
        if 'select all' in text.lower() or 'mark all' in text.lower():
            self.form_input_extended['select all'] = True
        return text.lower().strip().replace("(", "").replace(")", "").replace(".", "").replace("?", "").replace("*", "").replace("✱", "").strip()

    def generate_response(self, context):
        print("\ngenerate_response()")
        print("context = ", context)
        input_ids = self.tokenizer.encode(context, return_tensors='pt').to("cuda" if torch.cuda.is_available() else "cpu")
        max_length = len(input_ids[0]) + 100
        output = self.model.generate(input_ids, max_length=max_length, temperature=0.7)
        response = self.tokenizer.decode(output[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        print("response = ", response)
        return response

    #*Checklist/Radio just transitions Yes-True && No-False
    def bool_to_str(self, value):
        print("\nbool_to_str()")
        return "Yes" if value.lower() == "true" else "No"

    def process_form_inputs(self, form_input_details):
        print("\nprocess_form_inputs()")
        self.init_form_input_extended()

        # self.nlp_load()
        # print("nlp loaded... ")

        #print("self.form_input_details: ", end="")
        #print(self.form_input_details)
        #print("form_input_details: ", form_input_details)
        submit_button = None
        remove_attachment = None
        resume_attachment = None
        for i, input_data in enumerate(form_input_details):
            try:
                print("\n\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")

                time.sleep(2)
                self.init_form_input_extended()
                self.is_special_case(input_data)

                #++++++++++++++++++++++++++++++ MAYBE treat like edge cases +++++++++++++++++++++++++++++++++++++++
                print(f"Input {str(i)}:")
                print("  form_input_details = ", input_data)
                if input_data['is_hidden']:
                    continue



                #|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
                #       iMac Computer needed this for testing!!!
                # if i == [1, 2, 3, 4, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]:
                #     self.form_input_extended['bc_nick_said'] == True
                #|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|




                # print("This is -> is None")         |       print("This is -> == None")         =>       print("This is -> None or empty")
                # if input_data['label'] is None:     |       if input_data['label'] == None:     =>       if not input_data['label']:
                #     print("Dang so -> is None")     |           print("Dang so -> == None")     =>           print("Dang so -> is None or empty")
                #     continue                        |           continue                        =>           continue


                #! THIS HAS TO BE 1st!!!!!!!!!  b/c if it's None or 'empty'(null) then all the other tests give erros when comparring!!
                print("This is -> None or empty")
                #Basically checks for None and empty!!
                if not input_data['label'] or input_data['label'] is None:
                    print("Dang so -> is None or empty")
                    continue

                print("This is -> dynamic")
                # or input_data['label'] is None:
                if 'dynamic' in input_data['label']:
                    print("Dang so -> dynamic")
                    continue

                print("This is -> == None       ...straight-up")
                if input_data['label'] is None:
                    print("Dang so -> == None       ...straight-up")
                    continue

                print("This is -> == None       IT'S A STRING")
                if input_data['label'] == 'None':
                    print("Dang so -> == None       IT'S A STRING")
                    continue



                if 'Remove attachment' in input_data['label']:
                    print("Remove attachment: (a file of sorts)")
                    print("input_data: ", input_data)
                    remove_attachment = input_data
                    print("remove_attachment: ", remove_attachment)
                    continue


                if 'Resume/CV' in input_data['label']:
                    print("Resume/CV: (a file)")
                    print("input_data: ", input_data)
                    resume_attachment = input_data
                    print("resume_attachment: ", resume_attachment)
                    continue


                if 'Submit Application' in input_data['label']:
                    print("Submit Application")
                    print("input_data: ", input_data)
                    submit_button = input_data
                    print("submit_button: ", submit_button)
                    continue
                #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


                self.scroll_to_question(input_data['html'])
                #self.scroll_to_element(input_data)
                print("  Scrolled here I guess...\n")
                print("self.form_input_extended = ", self.form_input_extended)
                time.sleep(3)

                label = input_data['label']
                print("unprocessed label: ", label)
                label = self.process_text(label)
                print("processed label: ", label)
                input_type = input_data['type']
                predefined_options = input_data.get('values', None)
                print("predefined_options = ", predefined_options)

                # If the input type in select, radio, or checkbox, handle it as a !special case!
                print("\n_____________________________________________________________________________________")
                print("TIME FOR COMPARISONS! DO YOU HEAR THAT BUTT-HEAD!!! WE ARE GONNA BE COMPARING BUTTS!!")
                if input_type in ['select', 'radio', 'checkbox']:
                    print("Ahhhhhhh yes it is either one of these: 'select', 'radio', 'checkbox'")
                    matching_keys = self.get_matching_keys(label)               #! .get_matching_keys() does all the comaparing to get the right answer!!!!! ssooo there do   special case check -> .env chack -> long q>a ... a>a check!!!
                    if matching_keys:
                        #!HERE HERE HERE HERE HERE HERE HERE HERE HERE HERE HERE HERE
                        print("self.form_input_extended = ", self.form_input_extended)
                        for key in matching_keys:

                            answer = self.users_information[{key}]
                            print("answer = ", answer)
                            if answer in predefined_options:
                                # Input the answer into the form
                                print(f"Entering '{answer}' for '{label}'")
                            else:
                                print(f"Stored answer '{answer}' is not a valid option for '{label}'")
                    else:
                        print(f"No stored answers found for '{label}'")

                else:
                    print("This one ain't special... this one ain't even intelligent... dumb ol' question any how")
                    matching_keys = self.try_finding_match(label)
                    print("matching_keys = ", matching_keys)
                    #! MAYBE HERE MAYBE HERE MAYBE MAYBE HERE MAYBE HERE MAYBE HERE
                    #self.form_input_extended['env_key'] = key
                    #self.form_input_extended['env_values'].append(self.users_information[key])
                    print("if matching_keys: ", end="")
                    print("True" if matching_keys else "False")
                    # if matching_keys:
                    #     for key in matching_keys:
                    if matching_keys:
                        print("self.form_input_extended['env_values'] = ", self.form_input_extended['env_values'])
                        for key in self.form_input_extended['env_values']:
                            print("key = ", key)
                            answer = self.users_information.get(key)
                            print("answer = ", answer)
                            # Input the answer into the form
                            print(f"Entering '{answer}' for '{label}'")
                            #self.fill_form(label, answer)
                    else:
                        context = self.q_and_a['summary'] + " " + label
                        answer = self.generate_response(context)
                        if answer:
                            # Input the answer into the form
                            print(f"Entering '{answer}' for '{label}'")
                            #self.fill_form(label, answer)
                        else:
                            print(f"No stored answers found for '{label}'")
                self.form_input_extended['env_html'] = self.extract_css(input_data['html'])

                self.print_form_input_extended()     ############################### HERE VON!!!

                self.fill_that_form()


            except BreakLoopException:
                print("You know what eff that job anyways! They probably suck and would've over worked you.")
                return


        self.submit_job_application(submit_button)
        print("ALL DONE!!! The job application has been completed Counselor Mackie...")
        print("Normally Counselor Mackie would recommend pushing the 'Submit Application' button right now!")
        time.sleep(2)

    def try_finding_match(self, label):
        print("\n1)try_finding_match()")
        words_in_label = label.split()
        jacc_key = None
        if len(words_in_label) <= 2:
            print("This question has 2 words or less.")
            print(words_in_label)
        
        else:
            print("This question has more than 2 words.")
            #! => doc = self.nlp(label)
            named_entities, headword, dependants = self.spacy_extract_key_info(self.nlp(label))
            print(f"named_entities = {named_entities}")
            print(f"headword = {headword}")
            print(f"dependants = {dependants}")
            key = self.generate_key(named_entities, headword, dependants)
            jacc_key = key.lower().replace("_", " ")
            print("jacc_key = ", jacc_key)
        
        #self.JobSearchWorkflow_instance.load_custom_rules()
        print("words_in_label = ", words_in_label)
        print("label = ", label)
        #NOTE: Remember Q_AND_A is only for the summary! So we only traverse CUSTOM_RULES!!
        print("self.custom_rules = ", self.custom_rules)
        #? These might work in case that one doesn't
        #for rule in self.custom_rules.keys():
        #for rule, value in self.custom_rules.items():
        #for rule, value in self.custom_rules:
        for rule in self.custom_rules:
            if label == rule:
                print("MATCH: [ try_finding_match() ]")
                print("\tCUSTOM_RULES = ", rule)
                print("\tlabel = ", label)
                #print("\t... value = ", value)
                print("\t... value = ", self.custom_rules[rule])
                return rule
            
        found_best_match = self.find_best_match(label)
        print("found_best_match = ", found_best_match)
        
        #TODO: REPLACE THIS    v!!!!!!!!!!
        # if label == config.py[key]:
        #     return config.py[key]
        if found_best_match:
            return found_best_match
        #! RECENT CHANGE RECENT CHANGE RECENT CHANGE
        # elif self.jaccard_similarity(jacc_key, label):
        #     return jacc_key
        # else:
        #     #Since `rule` was previously defined you use it as above but since `summary` wasn't {something about Python treats} so just use () with '' inside it and the variable name within the ''
        #     return self.generate_response(self.q_and_a('summary'))
       
        
        #! HERE HERE HERE HERE
               
                   
        else:
            jacc_key

    #*SpaCy runs SpaCy methods
    def spacy_extract_key_info(self, doc):
        print("\nspacy_extract_key_info()")
        print("\n\n--------------------------------------------------------")
        print("My Way")
        print("spacy_extract_headword_and_dependants()")
        headword = ""
        dependants = []
        for token in doc:
            print(f"""
                  TOKEN: {token.text}
                  ====
                  {token.tag_ = }
                  {token.head.text = }
                  {token.dep_ = }
                  """)
            
            
            print(token.head)
            if token.dep_ == "ROOT":
                headword = token.head.text
            elif token.dep_ in {"compound", "amod", "attr"}:
                dependants.append(token.lemma_)
                #dependants.append(token.text)
        print(f"headword = {headword}")
        print(f"dependants = {dependants}")
        #return headword, dependants
        print("--------------------------------------------------------")
        
        print("\n\n--------------------------------------------------------")
        print("Their Dumb Way")
        named_entities = [ent.text for ent in doc.ents]
        headword = ""
        dependants = []
        for token in doc:
            if token.dep_ == "ROOT":
                headword = token.lemma_
            elif token.dep_ in {"compound", "amod", "attr"}:
                dependants.append(token.lemma_)
        print(f"named_entities = {named_entities}")
        print(f"headword = {headword}")
        print(f"dependants = {dependants}")
        #return named_entities, headword, dependants
        print("--------------------------------------------------------")
        return named_entities, headword, dependants
    
    #*If SpaCy special case needs to be made... ensure it!! and if still yes then do so here
    def generate_key(self, named_entities, headword, dependants):
        print("\ngenerate_key()")
        
        # Using set automatically eliminates duplicates for us!!
        tokens = set(named_entities + [headword] + dependants)
        key = "_".join(tokens).upper()
        print(f"key = {key}")
        return key
    
    #TODO: ADD NEW key-value PAIR TO FILE  &&  THE custom_rules or users_information
    #*Add !UNIQUE! key-value pair to EITHER config.py || .env
    def store_new_answer(self, question, answer):
        print("\nstore_new_answer()")
        #nlp = spacy.load("en_core_web_md")
        doc = self.nlp(question.lower())
        named_entities, headword, dependants = self.spacy_extract_key_info(doc)
        key = self.generate_key(named_entities, headword, dependants)
        #key = self.verify_key(key, question)
        
        # If key is unique, add it to the .env file
        if key not in self.users_information:
            self.users_information[key] = answer
            with open(self.env_path, "a") as file:
                file.write(f"\n{key}='{answer}")
    
    #TODO:------------------------------------------------------------------------------
    #TODO: redid the synonym method
    def handle_match(self, key, label):
        print("MATCH: [ 2.1)find_best_match() -> .similarity(question{*label*} | self.users_information.key)]")
        print("\tusers_information = ", key)
        print("\tlabel = ", label)
        print("\t... value = ", self.users_information[key])
        self.form_input_extended['env_key'] = key
        self.form_input_extended['env_values'].append(self.users_information[key])
        return key

    #*Uses label to try and find a matching key from the users' .env
    def find_best_match(self, label):
        print("\n2)find_best_match()")
        
        doc1 = self.nlp(label.lower())
        print("-doc1 = ", doc1)
        max_similarity = -1
        best_match = None
        synonyms = self.get_synonyms(label)
        
        print("users_information + 1")
        for key in self.users_information.keys():
            doc2 = self.nlp(key.lower().replace("_", " "))
            print("-doc2(self.users_information.key) = ", doc2)
            similarity = doc1.similarity(doc2)
            print("similarity = ", similarity)
            print("key = ", key)
            if similarity > max_similarity:
                max_similarity = similarity
                best_match = key    #leave as = to key so it's just easier for later!!
                print("max_similarity = ", max_similarity)
                print("best_match = ", best_match)
                
                if max_similarity == 1.0:
                    print("Before assignment:", self.form_input_extended)
                    print("Before assignment(key):", key)
                    self.form_input_extended['env_key'] = key
                    print("After assignment:", self.form_input_extended)
                    print("After assignment(key):", key)
                    
                    self.form_input_extended['env_values'].append(self.users_information[key])
                    print("MATCH: [ 2.1)find_best_match() -> .similarity(question{*label*} | self.users_information.key)]")
                    print("\tusers_information = ", key)
                    print("\tlabel = ", label)
                    print("\t... value = ", self.users_information[key])
                    #print("\t... value = ", self.users_information['{key}'])
                    return key
                elif len(synonyms) > 0:
                    for synonym in synonyms:
                        doc2_syn = self.nlp(synonym.lower().replace("_", " "))
                        similarity_syn = doc2_syn.similarity(doc2)
                        if similarity_syn > max_similarity:
                            max_similarity = similarity_syn
                            best_match = key
                            
                            if max_similarity == 1.0:
                                print("Before assignment:", self.form_input_extended)
                                print("Before assignment(key):", key)
                                self.form_input_extended['env_key'] = key
                                print("After assignment:", self.form_input_extended)
                                print("After assignment(key):", key)
                                
                                self.form_input_extended['env_values'].append(self.users_information[key])
                                print("MATCH: [ 2.1)find_best_match() -> .similarity(question{*label*} | self.users_information.key)]")
                                print("\tusers_information = ", key)
                                print("\tlabel = ", label)
                                print("\t... value = ", self.users_information[key])
                                #print("\t... value = ", self.users_information['{key}'])
                                return key
                
                
            # Check for synonyms
            #! WRONG ! sometimes I have 2 so get the root or something!!!
            #synonyms = self.get_synonyms(key)
            #synonyms = self.get_synonyms(label)
            
            
            #!-------------------------------------------------------------------------------------------------------------------------
            # for synonym in synonyms:
            #     doc2 = self.nlp(synonym.lower().replace("_", " "))
            #     print("-doc2(synonyms.index) = ", doc2)
            #     #similarity = doc1.similarity(doc2)
            #     similarity = doc2.similarity(doc1)
            #     print("similarity = ", similarity)
            #     print("key = ", key)
            #     print("synonyms = ", synonyms)
            #     if similarity > max_similarity:
            #         max_similarity = similarity
            #         best_match = key
            #         print("max_similarity = ", max_similarity)
            #         print("best_match = ", best_match)
                    
            #         if max_similarity == 1.0:
            #             self.form_input_extended['env_key'] = key
            #             self.form_input_extended['env_values'].append(self.users_information[key])
            #             print("MATCH: [ 2.2)find_best_match() -> .similarity(question{*label*} | synonyms.index)]")
            #             print("\tusers_information = ", key)
            #             print("\tlabel = ", label)
            #             print("\t... synonym = ", synonym)
            #             print("\t... value = ", self.users_information[key])
            #             #print("\t... value = ", self.users_information['{key}'])
            #             return key
            #!-------------------------------------------------------------------------------------------------------------------------
            
            
            print("\nusers_information + 1")
            
        print("max_similarity = ", max_similarity)
        print("best_match = ", best_match)
        print(best_match if max_similarity > 0.90 else None)
        return best_match if max_similarity > 0.90 else None
    
    def check_similarity(self, doc1, doc2, key, label, max_similarity):
        similarity = doc1.similarity(doc2)
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = key
            if max_similarity == 1.0:
                return self.handle_match(key, label), max_similarity
        return best_match, max_similarity

    def find_the_bestest_match(self, label):       #aka - "find_best_match"
        print("\n2)find_best_match()")
        doc1 = self.nlp(label.lower())
        max_similarity = -1
        best_match = None
        synonyms = self.get_synonyms(label)

        for key in self.users_information.keys():
            doc2 = self.nlp(key.lower().replace("_", " "))
            best_match, max_similarity = self.check_similarity(doc1, doc2, key, label, max_similarity)

            if len(synonyms) > 0:
                for synonym in synonyms:
                    doc2_syn = self.nlp(synonym.lower().replace("_", " "))
                    best_match, max_similarity = self.check_similarity(doc1, doc2_syn, key, label, max_similarity)

        print("max_similarity = ", max_similarity)
        print("best_match = ", best_match)
        return best_match if max_similarity > 0.90 else None
    #TODO:------------------------------------------------------------------------------
    
    #*This is the DOUBLE CHECK
    def get_synonyms(self, word):
        print("\n3)get_synonyms()")
        print(f"word = {word}")
        #TODO: Ensure this resets the list of synonyms each time
        synonyms = []

        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())
        #TODO: DOUBLE CHECK THIS!!!!! Your asking for the synonyms of `phone number`?!?!?!?! Do we really want the synonyms for the key and not the label?!?!?!
        if word.lower() in self.custom_synonyms:
            #for custom_syn in self.custom_synonyms[word]:
            for custom_syn in self.custom_synonyms[self.process_text(word)]:
                #synonyms.extend(custom_syn)
                print("filtered_custom_syn = ", end="")
                filtered_custom_syn = self.process_text(custom_syn)
                filtered_custom_syn = filtered_custom_syn.replace("_", " ")
                print(filtered_custom_syn)
                synonyms.append(filtered_custom_syn)

        print("self.custom_synonyms = ", end="")
        print(self.custom_synonyms)
        
        
        print("synonyms = ", end="")
        print(synonyms)
        print("\n--------------------")
        
        time.sleep(2)
        
        return synonyms
    
    #*Just for me to see what it does!!
    def jaccard_similarity(self, sentence1, sentence2):
        print("\njaccard_similarity()")
        set1 = set(sentence1.lower().split())
        set2 = set(sentence2.lower().split())
        intersection = set1.intersection(set2)
        print(f"intersection = {intersection}")
        union = set1.union(set2)
        print(f"union = {union}")
        jaccard_similarity = (len(intersection) / len(union))
        print(f"jaccard_similarity = {jaccard_similarity}")
        if jaccard_similarity > 90:
            return True
        else:
            return False
    
    def submit_job_application(self, submit_button):
        
        print("We are about to click the submit button")
        time.sleep(3)
        submit_button = self.extract_css(submit_button['HTML'])
        print("submit_button = ", submit_button)
        time.sleep(1)
        submit_element_idk = self.browser.find_element(By.CSS_SELECTOR, submit_button)
        print("submit_element_idk = ", submit_element_idk)
        time.sleep(1)
        self.keep_jobs_applied_to_info()
        #self.sessions_applied_to_info
        return
        
        
        
        
        
        #submit_button_index = self.form_input_details.get('KEY-NAME')
        #submit_button = self.extract_css(submit_button_index['HTML'])
        
        '''
        submit_button = self.extract_css(submit_button['HTML'])
        
        self.browser.find_element(By.CSS_SELECTOR, submit_button).click()
        
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".response-message")))
        
        response_message = self.browser.find_element(By.CSS_SELECTOR, ".response-message").text
        if "success" in response_message.lower():
            self.keep_jobs_applied_to_info()
            print("Form submission was successful!")
        else:
            print("Form submission failed!")
            
        error_messages = self.driver.find_elements(By.CSS_SELECTOR, ".error-message")
        for error_message in error_messages:
            print(f"Error: {error_message.text}")
        '''
            
        #TODO: Add call to oxylabs captcha!!!!! 
            
        #TODO: I believe I just return all the way to go to the next job application!!!!
        #return

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!                                                                               !
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    #TODO: Check the wording in the question
    #*special_case() method 2
    def is_special_case(self, input_data):
        label = input_data['type']
        if label in ['select', 'radio', 'checkbox', 'file']:  #NOT 'button' b/c that's just the Submit
            if label == 'select':
                select_element = self.browser.find_element(label)
                is_multiple_choice = select_element.get_attribute('multiple') is not None
                if is_multiple_choice is True:
                    self.form_input_extended['text'] = 'is_multiple_choice'
                elif is_multiple_choice is False:
                    pass
            elif label == 'checkbox':
                self.form_input_extended['checkbox'] = True
                self.form_input_extended = 'is_multiple_choice'
            elif label == 'radio':
                self.form_input_extended['radio'] = True
            elif label == 'file':
                self.form_input_extended['file'] = True
        else:
            if label == 'text' or label == 'textarea':
                self.form_input_extended['text'] = True
            elif label == 'button':
                self.form_input_extended['text'] = True
            
            else:
                print("There has been an error father...")
                print("label = ", label)
        return

    #TODO: Once we submit the application confirm that here and then save everything!!!
        #? For the user or my google_sheet_stats i don't know???
    #* My vote is we leave it as it is so b/c this is the correct format for Google Sheet's!!!
    #* Then JobsThatUserHasAppliedTo.csv has the same format and we can just add the session time at the end easily!!
    #! REMEMBER: if the program crashes it has to hold/preserve values!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def keep_jobs_applied_to_info(self):
        self.sessions_applied_to_info.append({
            'Job_URL': self.current_url,
            'Company_Name': self.current_jobs_details["company_name"],
            'Job_Title': self.current_jobs_details["job_title"],
            'Company_Job_Location': self.current_jobs_details["job_location"],
            'Company_Department': self.company_job_department,
            'Job_ID_Number': self.job_id_number,
        })
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    def keep_jobs_applied_to_info(self):
        self.jobs_applied_to_this_session.append(self.current_jobs_details)

