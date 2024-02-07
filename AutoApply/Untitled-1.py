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
                safe_print(f"  form_input_details = {input_data}")
                if input_data['is_hidden']:
                    continue



                #|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
                #       iMac Computer needed this for testing!!!
                # if i == [1, 2, 3, 4, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]:
                #     self.form_input_extended['bc_nick_said'] == True
                #|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|




 
                #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


                self.scroll_to_question(input_data['html'])
                #self.scroll_to_element(input_data)
                print("  Scrolled here I guess...\n")
                safe_print(f"self.form_input_extended = {self.form_input_extended}")
                time.sleep(3)

                label = input_data['label']
                safe_print(f"unprocessed label: {label}")
                label = self.process_text(label)
                safe_print(f"processed label: {label}")
                input_type = input_data['type']
                predefined_options = input_data.get('values', None)
                safe_print(f"predefined_options = {predefined_options}")

                # If the input type in select, radio, or checkbox, handle it as a !special case!
                print("\n_____________________________________________________________________________________")
                print("TIME FOR COMPARISONS! DO YOU HEAR THAT BUTT-HEAD!!! WE ARE GONNA BE COMPARING!!")
                if input_type in ['select', 'radio', 'checkbox']:
                    print("Ahhhhhhh yes it is either one of these: 'select', 'radio', 'checkbox'")
                    matching_keys = self.get_matching_keys(label)               #! .get_matching_keys() does all the comaparing to get the right answer!!!!! ssooo there do   special case check -> .env chack -> long q>a ... a>a check!!!
                    if matching_keys:
                        #!HERE HERE HERE HERE HERE HERE HERE HERE HERE HERE HERE HERE
                        safe_print(f"self.form_input_extended = {self.form_input_extended}")
                        for key in matching_keys:

                            answer = self.users_information[{key}]
                            safe_print(f"answer = {answer}")
                            if answer in predefined_options:
                                # Input the answer into the form
                                safe_print(f"Entering '{answer}' for '{label}'")
                            else:
                                safe_print(f"Stored answer '{answer}' is not a valid option for '{label}'")
                    else:
                        safe_print(f"No stored answers found for '{label}'")

                else:
                    print("This one ain't special... this one ain't even intelligent... dumb ol' question any how")
                    matching_keys = self.try_finding_match(label)
                    safe_print(f"matching_keys = {matching_keys}")
                    #! MAYBE HERE MAYBE HERE MAYBE MAYBE HERE MAYBE HERE MAYBE HERE
                    #self.form_input_extended['env_key'] = key
                    #self.form_input_extended['env_values'].append(self.users_information[key])
                    print("if matching_keys: ", end="")
                    print("True" if matching_keys else "False")
                    # if matching_keys:
                    #     for key in matching_keys:
                    if matching_keys:
                        
                        
                        
                        
                        if not self.form_input_extended['env_values']:
                            #self.form_input_extended['env_values'] is originally ASSIGNED a list type... so a lsit type it MUST remain!
                            self.form_input_extended['env_values'].append(matching_keys)
                        
                        
                        
                        
                        print("self.form_input_extended['env_values'] = ", self.form_input_extended['env_values'])
                        for key in self.form_input_extended['env_values']:
                            safe_print(f"key = {key}")
                            answer = self.users_information.get(key)
                            safe_print(f"answer = {answer}")
                            # Input the answer into the form
                            safe_print(f"Entering '{answer}' for '{label}'")
                            #self.fill_form(label, answer)
                    else:
                        context = self.q_and_a['summary'] + " " + label
                        answer = self.generate_response(context)
                        if answer:
                            # Input the answer into the form
                            safe_print(f"Entering '{answer}' for '{label}'")
                            #self.fill_form(label, answer)
                        else:
                            safe_print(f"No stored answers found for '{label}'")
                self.form_input_extended['env_html'] = self.extract_css(input_data['html'])

                self.print_form_input_extended()     ############################### HERE VON!!!

                self.fill_that_form()


            except BreakLoopException:
                print("You know what forget that job anyways! They probably suck and would've over worked you.")
                return


        self.submit_job_application(submit_button)
        print("ALL DONE!!! The job application has been completed Counselor Mackie...")
        print("Normally Counselor Mackie would recommend pushing the 'Submit Application' button right now!")
        time.sleep(2)

#----------------------------------------------------------------------------------------------------------
#**********************************************************************************************************
#----------------------------------------------------------------------------------------------------------
#**********************************************************************************************************
#----------------------------------------------------------------------------------------------------------
#**********************************************************************************************************
#----------------------------------------------------------------------------------------------------------

    def process_form_inputs(self, form_input_details):
        print("\nprocess_form_inputs()")
        # self.init_form_input_extended()
        self.nlp_load()
        print("nlp loaded... ")

        #print("self.form_input_details: ", end="")
        #print(self.form_input_details)
        #print("form_input_details: ", form_input_details)

        for i, input_data in enumerate(form_input_details):
            time.sleep(2)
            try:
                print("\n\n\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")

                #self.init_form_input_extended()

                print(f"Input {str(i)}:")
                safe_print(f"  form_input_details = {input_data}")
                
                self.identify_input_type_value(input_data)
                
                if input_data['is_hidden']:
                    #This could be captcha, dynamic question, or just has a dynamic list that opens
                    self.handle_hidden_elements(i, input_data)
                    #TODO
                    
                #is_special_case()
                if self.handle_special_input_labels(input_data):
                    continue
                
                self.scroll_to_question(input_data['html'])
                #self.scroll_to_element(input_data)
                print("  Scrolled here I guess...\n")
                safe_print(f"self.form_input_extended = {self.form_input_extended}")
                time.sleep(1)

                label = input_data['label']
                safe_print(f"un-analyzed label: {label}")
                #process_text()
                #MAYBE => classify/identify_mandatory_question_requirements()
                label = self.analyze_and_flag_question_requirements(label)
                safe_print(f"analyzed label: {label}")
                #MAYBE move this to identify_input_type_value()
                input_type = input_data['type']
                predefined_options = input_data.get('values', None)
                safe_print(f"predefined_options = {predefined_options}")
        
                
                #self.answer_by_label_type(input_data)
                self.process_to_answer_questions(input_data)
            except BreakLoopException:
                print("You know what forget that job anyways! They probably suck and would've over worked you.")
                return
            return
        
    def answer_by_label_type(self, input_data):
        print("\n_____________________________________________________________________________________")
        print("TIME FOR COMPARISONS! DO YOU HEAR THAT BUTT-HEAD!!! WE ARE GONNA BE COMPARING!!")
        # If the input type in select, radio, or checkbox, handle it as a !special case!
        if input_type in ['select', 'radio', 'checkbox']:
            print("Ahhhhhhh yes it is either one of these: 'select', 'radio', 'checkbox'")
            matching_keys = self.get_matching_keys(label)               #! .get_matching_keys() does all the comaparing to get the right answer!!!!! ssooo there do   special case check -> .env chack -> long q>a ... a>a check!!!
            if matching_keys:
                #!HERE HERE HERE HERE HERE HERE HERE HERE HERE HERE HERE HERE
                safe_print(f"self.form_input_extended = {self.form_input_extended}")
                for key in matching_keys:

                    answer = self.users_information[{key}]
                    safe_print(f"answer = {answer}")
                    if answer in predefined_options:
                        # Input the answer into the form
                        safe_print(f"Entering '{answer}' for '{label}'")
                    else:
                        safe_print(f"Stored answer '{answer}' is not a valid option for '{label}'")
            else:
                safe_print(f"No stored answers found for '{label}'")

        else:
            print("This one ain't special... this one ain't even intelligent... dumb ol' question any how")
            matching_keys = self.try_finding_match(label)
            safe_print(f"matching_keys = {matching_keys}")
            #! MAYBE HERE MAYBE HERE MAYBE MAYBE HERE MAYBE HERE MAYBE HERE
            #self.form_input_extended['env_key'] = key
            #self.form_input_extended['env_values'].append(self.users_information[key])
            print("if matching_keys: ", end="")
            print("True" if matching_keys else "False")
            # if matching_keys:
            #     for key in matching_keys:
            if matching_keys:
                
                
                
                
                if not self.form_input_extended['env_values']:
                    #self.form_input_extended['env_values'] is originally ASSIGNED a list type... so a lsit type it MUST remain!
                    self.form_input_extended['env_values'].append(matching_keys)
                
                
                
                
                print("self.form_input_extended['env_values'] = ", self.form_input_extended['env_values'])
                for key in self.form_input_extended['env_values']:
                    safe_print(f"key = {key}")
                    answer = self.users_information.get(key)
                    safe_print(f"answer = {answer}")
                    # Input the answer into the form
                    safe_print(f"Entering '{answer}' for '{label}'")
                    #self.fill_form(label, answer)
            else:
                context = self.q_and_a['summary'] + " " + label
                answer = self.generate_response(context)
                if answer:
                    # Input the answer into the form
                    safe_print(f"Entering '{answer}' for '{label}'")
                    #self.fill_form(label, answer)
                else:
                    safe_print(f"No stored answers found for '{label}'")
        self.form_input_extended['env_html'] = self.extract_css(input_data['html'])

        self.print_form_input_extended()     ############################### HERE VON!!!

        self.fill_that_form()
        return

    def init_form_input_label(self):
        self.form_input_label = {
            "mandatory": False,
            "text": False,
            "select": False,
            "radio": False,
            "checkbox": False,
            "button": False,
            "file": False,
            "answer_min": 0,
            "answer_max": 0,
            "dynamic": False,
            "not_applicable": False,
            "left_blank": False,
            "unanswerable": False
        }   

    #Finds just 1 answer!!!!
    def process_to_answer_questions(input_data):
        if self.form_input_extended['mandatory'] == True:
            try:
                #TODO
                #NOTE:For 'mandatory' questions 1 answer is REQUIRED and 0 SHOULD result in a thrown exception!!
                self.analyze_and_classify_question_specifics()
                    self.num_of_answers_accepted()
                    self.question_relationship()
                self.search_for_answers()
                    if self.analyze_and_classify_question_specifics() == True or self.has_special_label_type() == True:
                        self.handle_special_question()
                    else:
                        self.workflow_to_find_anwser(input_data)
                
            except SomeException:
                raise BreakLoopException("Unable to answer!")
        else:
            self.analyze_and_classify_question_text()
            
    def workflow_to_find_anwser(self, input_data):
        #Check form_input_details['values'] if Yes, No, True, or False and if so self.bool_to_str() && save all answers!!
        if self.form_input_details['values'] == 'True' or self.form_input_details['values'] == 'Yes':
            alternate_possible_values = ['True', 'Yes', 1]
        
        #            self.compare_label_to_config_keys()
        if answer := self.check_custom_rules(input_data, self.custom_rules):
            return answer
        #This applies synonyms I believe!!
        elif answer := self.check_env_file():
            return answer
        elif answer := self.check_custom_synonyms():
            return answer
        elif not self.form_input_details['values']:
            if answer := self.compare_restricted_values_to_env():
                return answer
        elif answer := self.can_summary_answer():
            return answer
        else:
            return None
    
    #removes the
    def check_custom_rules(self, input_data, custom_rules):
        print(f"\ncheck_custom_rules()")
        #print("self.custom_rules = ", self.custom_rules)
        print(f"self.custom_rules = {custom_rules}")
        if custom_rules_key := self.compare_label_to_config_keys(input_data, custom_rules):
            custom_rules_key_value = self.convert_custom_rules(input_data['label'], custom_rules_key)
        else:
            return
        
    #! label needed!!!!!
    def check_custom_synonyms(self, label):
        words_in_label = label.split()
        jacc_key = None
        print("words_in_label = ", words_in_label)
        
        named_entities, headword, dependants = self.spacy_extract_key_info(self.nlp(label))
        print(f"named_entities = {named_entities}")
        print(f"headword = {headword}")
        print(f"dependants = {dependants}")
        key = self.generate_key(named_entities, headword, dependants)
        jacc_key = key.lower().replace("_", " ")
        print("jacc_key = ", jacc_key)

        found_best_match = self.find_best_match(label)
        print("found_best_match = ", found_best_match)
        
        if found_best_match:
            return found_best_match
        else:
            jacc_key
        
    def compare_label_to_config_keys(self, input_data, config_dict_var):
        for config_key_capitalized in config_dict_var:
            config_key = config_key_capitalized.lower()
            if input_data['label'] == config_key:
                print(f"MATCH: [ {input_data['label']} = {config_key} ]")

    def handle_special_input_labels(self, input_data):
        print("handle_special_input_labels()")
        submit_button = None
        remove_attachment = None
        resume_attachment = None
        #?MAYBE?
        # if input_data['is_hidden']:
        #     self.handle_hidden_elements(input_data)
        
        if self.check_for_falsiness(input_data):
            return True
        
        print("This is -> dynamic")
        # or input_data['label'] is None:
        if 'dynamic' in input_data['label']:
            print("This is -> dynamic")
            return True
        
        if input_data['label'] == 'None':
            print("input_data['label'] == None       IT'S A STRING")
            return True

        if 'Remove attachment' in input_data['label']:
            print("Remove attachment: (a file of sorts)")
            safe_print(f"input_data: {input_data}")
            remove_attachment = input_data
            safe_print(f"remove_attachment: {remove_attachment}")
            return True

        if 'Resume/CV' in input_data['label']:
            print("Resume/CV: (a file)")
            safe_print(f"input_data: {input_data}")
            resume_attachment = input_data
            safe_print(f"resume_attachment: {resume_attachment}")
            return True

        if 'Submit Application' in input_data['label']:
            print("Submit Application")
            safe_print(f"input_data: {input_data}")
            submit_button = input_data
            safe_print(f"submit_button: {submit_button}")
            return True
        return False
        
    #Checks for "falsiness" in input_data['label']
    #In Python, several things are considered "falsy", including an empty string (''), an empty list ([]),
    #an empty dictionary ({}), the number zero (0), None, and False. So, this part of the condition will be
    #True if input_data['label'] is any of these falsy values, including an empty string.
    #NOTE:
        #Nullness-In Python, the term "null" is not used as frequently as in some other languages. Instead,
        #Python uses None to represent the absence of a value. Checking for None is checking for this
        #specific absence.
        #Emptiness-Refers to a variable that is initialized but holds no content, like an empty string ('')
        #or an empty list ([]). In your case, you are checking for the emptiness of input_data['label'].
    def check_for_falsiness(self, input_data):
        print(f"\ncheck_for_falsiness()")
        if not input_data['label']:
            print("Dang so -> input_data['label'] is falsy")
            return True
        return False
    
    #is_special_case()
    def identify_input_type_value(self, input_data):
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
    
    #process_text()
    def analyze_and_flag_question_requirements(self, text):
        print("process_text()")
        #if "*" in text or "✱" in text:
        asterisk_list = ["*", "✲", "✱", "＊", "﹡", "⁎", "✻", "∗", "⃰", "✲", "✳", "꙳", "﹡", "※", "⁂", "✢", "✣", "✤", "✥", "✦", "✧", "✶", "✷", "✸", "✹", "✺", "✼", "✽", "❃", "❊", "❋"]

        if any(asterisk in text for asterisk in asterisk_list):
            self.form_input_extended['mandatory'] = True
        if 'select one' in text.lower():
            self.form_input_extended['select one'] = True
        if 'select all' in text.lower() or 'mark all' in text.lower():
            self.form_input_extended['select all'] = True
        return text.lower().strip().replace("(", "").replace(")", "").replace(".", "").replace("?", "").replace("*", "").replace("✱", "").strip()
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        

        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
                
        
        
        
    def fill_that_form(self):                                                                            #v For `select` when there's too many answers!!
        #if self.form_input_extended['mandatory'] is True and (self.form_input_extended['env_values'] or self.form_input_extended['env_html']):
        # ^ the purpose of the if is b/c...  if we don't need(['mandatory']) to do the question then we don't!!!!
        print("fill_that_form()")
        if self.form_input_extended['env_key'] and self.form_input_extended['env_values']:
            #print("fill_that_form()")
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
            #-------------------------------------------------------------------------------------------
            #This  v  checks if the "value" is 'empty' or 'None'
            #if self.form_input_extended['bc_nick_said']:
            if 'bc_nick_said' in self.form_input_extended:
                if self.form_input_extended['bc_nick_said'] == True:
                    pass
                elif self.form_input_extended['bc_nick_said'] == False:
                    print("Release the hounds Mr. Smithers...")
                    #self.form_input_extended['bc_nick_said'] == False
                    return
            
            
            
            
            
            
            
            
            # if self.form_input_extended['env_key'] == 'PHONE_NUMBER':
            #     print("Ok at least I made it in here!")
            #     element = self.form_input_extended['env_html']
            #     value = self.form_input_extended['env_values'][0]
            #     print("element = ", element)
            #     print("value = ", value)
                
            #     success = self.troubleshoot_form_filling(element, value)
                
            #     if not success:
            #         print("Failed to fill in the form. See the error messages above for details.")
            #     else:
            #         print("Successfully filled in the form.")
            
            
            
            
            
            
            
            
            
            
            
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

#----------------------------------------------------------------------------------------------------------          
#**********************************************************************************************************
#----------------------------------------------------------------------------------------------------------
#**********************************************************************************************************
#----------------------------------------------------------------------------------------------------------
#**********************************************************************************************************
#----------------------------------------------------------------------------------------------------------