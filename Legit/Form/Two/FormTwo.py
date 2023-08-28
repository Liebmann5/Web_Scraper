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
