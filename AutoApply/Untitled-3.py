    def apply_to_job(self):
        print("\napply_to_job()")
        time.sleep(3)
        current_url = self.browser.current_url
        if self.application_company_name == "lever":
            self.reset_webpages_soup_elements()
        self.soup_elements['soup'] = self.apply_beautifulsoup(current_url, "html")
        self.form_input_details = self.get_form_input_details(current_url)
        self.insert_resume()
        # self.process_form_inputs(self.form_input_details)
        self.fillout_job_application(self.form_input_details)
        return 3
    def fillout_job_application(self):
        print(f"\nfillout_job_application()")
        self.process_form_inputs(self.form_input_details)
        self.print_form_input_extended()
        self.fill_that_form()
        self.submit_job_application(submit_button)
        return
    def submit_job_application(self, submit_button):
        print(f"\nsubmit_job_application()")
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
    def print_form_input_extended(self):
        print("\n\n\ndouble_check_before_fill_in_form()")
        
        print('--------------------------------------------')
        print("Form Input Extended: ")
        for key, value in self.form_input_extended.items():
            print(f"{key}: {value}")
        print('--------------------------------------------')
        print("\n")
    def extract_question_text_and_strip_excess(self, filthy_question):
        print("extract_question_text_and_strip_excess()")
        #if "*" in filthy_question or "✱" in filthy_question:
        asterisk_list = ["*", "✲", "✱", "＊", "﹡", "⁎", "✻", "∗", "⃰", "✲", "✳", "꙳", "﹡", "※", "⁂", "✢", "✣", "✤", "✥", "✦", "✧", "✶", "✷", "✸", "✹", "✺", "✼", "✽", "❃", "❊", "❋"]

        if any(asterisk in filthy_question for asterisk in asterisk_list):
            self.form_input_extended['mandatory'] = True
        if 'select one' in filthy_question.lower():
            self.form_input_extended['select one'] = True
        if 'select all' in filthy_question.lower() or 'mark all' in filthy_question.lower():
            self.form_input_extended['select all'] = True
        return filthy_question.lower().strip().replace("(", "").replace(")", "").replace(".", "").replace("?", "").replace("*", "").replace("✱", "").strip()
    #MAYBE have -prepare- as a method name!!!
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
                safe_print(f"unprocessed label: {label}")
                label = self.process_text(label)
                safe_print(f"processed label: {label}")
                predefined_answers = input_data.get('values', None)
                safe_print(f"predefined_answers = {predefined_answers}")
                


                #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
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
                #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                
                #self.answer_by_label_type(input_data)
                self.process_to_answer_questions(input_data)
            except BreakLoopException:
                print("You know what forget that job anyways! They probably suck and would've over worked you.")
                return
            return
#process_form_inputs()  =>  prep-work
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
    def check_for_falsiness(self, input_data):
        print(f"\ncheck_for_falsiness()")
        if not input_data['label']:
            print("Dang so -> input_data['label'] is falsy")
            return True
        return False
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
                
            #NEW
            elif child.has_attr('name'):
                name_value = child['name']
                css_selector = f'input[name="{name_value}"]'
                
            else:
                raise ValueError('The element does not have an id or a class')

            elemental = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemental)
    def analyze_and_flag_question_requirements(self, text):
        print("process_text()")
#process_form_inputs()  =>  prep-work
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
                        self.handle_multi_ans_questions()
                    else:
                        self.workflow_to_find_anwser(input_data)
                
            except SomeException:
                raise BreakLoopException("Unable to answer!")
        else:
            self.analyze_and_classify_question_text()
        self.print_form_input_extended()
        return 
#process_to_answer_questions()  =>  1/2
    #TODO TODO TODO !!!!!!!!!!!
    def analyze_and_classify_question_specifics(self, input_data):
        #TODO
        self.handle_logic(input_data)
        max_ans_allowed = self.num_of_answers_accepted(input_data)
        #dynamic questions - related to a previous Q, only appear if specific answer picked from
        # previous Q, Q's that have dynamic answer list,...
        dynamic_reason = self.reasons_for_dynamic_flag(input_data)
        #NOTE: perhaps use a while loop and make dynamic_reason a list of all the reasons!!!!
        if dynamic_reason == dyanmic_causes[0]:
            return
        if dynamic_reason == dyanmic_causes[0]:
            return
        return max_ans_allowed
    def handle_logic(self, input_data):
        self.bool_to_str(input_data)
        return
    def bool_to_str(self, value):
        print("\nbool_to_str()")
        return "Yes" if value.lower() == "true" else "No"
    def num_of_answers_accepted(self, input_data):
    def reasons_for_dynamic_flag(self, input_data):
#process_to_answer_questions()  =>  1/2
    
#process_to_answer_questions()  =>  2/2
    def handle_multi_ans_questions(self, input_data, max_ans_allowed):
        i = 0
        while i <= max_ans_allowed:
            answer = self.workflow_to_find_answer(input_data)
            #NOTE: IMPORTANT since that workflow is so long having it inside another if I believe is bad?!?
            if not answer:
                break
            i =+ 1
        # i = represents the number of answers found... ssooo 0 means none 
        return i
    def workflow_to_find_anwser(self, input_data):
        #Check form_input_details['values'] if Yes, No, True, or False and if so self.bool_to_str() && save all answers!!
        # if self.form_input_details['values'] == 'True' or self.form_input_details['values'] == 'Yes':
        #     alternate_possible_values = ['True', 'Yes', 1]
        
        
        
        #            self.compare_label_to_config_keys()
        if answer := self.check_custom_rules(input_data, self.custom_rules):
            return answer
        #This applies synonyms I believe!!
        elif answer := self.check_env_file():
            return answer
        # elif answer := self.check_custom_synonyms():
        #     return answer
        elif not self.form_input_details['values']:
            if answer := self.compare_restricted_values_to_env():
                return answer
        elif answer := self.can_summary_answer():
            return answer
        else:
            return None
        self.handle_match(input_data, answer)
        return answer
#process_to_answer_questions()  =>  2/2

#workflow_to_find_answer()
  #CUSTOM_RULES
    def check_custom_rules(self, input_data, custom_rules_dict):
        print(f"\ncheck_custom_rules()")
        #print("self.custom_rules = ", self.custom_rules)
        print(f"self.custom_rules = {custom_rules_dict}")
        if custom_rules_key := self.compare_label_to_config_keys(input_data, custom_rules_dict):
            return self.convert_custom_rules(input_data['label'], custom_rules_key)
        return
    def deconstruct_custom_rules_dict_smoothly(self, matching_key):
        # for key, value_list in self.custom_rules.items():
        #     if matching_key == key:
        #         return value_list
        # #No equal key found in CUSTOM_RULES
        # return None
        
        #When choosing the first item from an iterable that passes a condition, we can use the next built-in function instead of a for-loop to make our code and our intent clearer.
        # ^ [https://docs.sourcery.ai/Reference/Python/Default-Rules/use-next/#after]
        #https://www.geeksforgeeks.org/python-next-method/ (<- so next isn't faster than the for loop but it just makes our code more concise...  idk the dumb computer told me to)
        return next((value_list for key, value_list in self.custom_rules.items() if matching_key == key), None)
    # = =
    def convert_custom_rule_values(self, label, rule_capital):
        print(f"\nconvert_custom_rule_values()")
        final_string = ''
        final_ans_string = ''
        # v ??This part is basically just checking if key is present otherwise skip!?!?!?
        #! I believe  v  this is for synonyms!?!?!?!?
        #custom_key_value = self.check_if_label_in_customs(self.custom_rules, label)
        print(f"      label = {label}")
        custom_key_value = self.custom_rules[rule_capital]
        print(f"      rule_capital = {rule_capital}")
        print(f"      custom_key_value = {custom_key_value}")
        
        #! UNECESSARY
        if custom_key_value:
            #custom_rule_split = custom_key_value.split(',')
            #for custom_rule_value in custom_rule_split:
            for custom_rule_value in custom_key_value:
                print(f"      custom_rule_value = {custom_rule_value}")
                if custom_rule_value.strip():
                # custom_rule_value_trimmed_leading_and_trailing_spaces = custom_rule_value.strip()
                # value = self.determine_type_of_value(custom_rule_value_trimmed_leading_and_trailing_spaces)
                    value = self.determine_type_of_value(custom_rule_value.strip())
                else:
                    #Handles the space issue!
                    value = " "
                print(f"      value = {value}")
                final_ans_string += value
                print(f"      final_ans_string = {final_ans_string}\n")
                
                
                # env_value = self.extract_env_values(custom_rule_value_trimmed_leading_and_trailing_spaces)
                # final_ans_string += (env_value + ' ')
        else:
            #final_ans_string += (custom_rule_value_trimmed_leading_and_trailing_spaces + ' ')
            final_ans_string = custom_key_value
        #finalized_string = final_ans_string[:-1]
        # print(f"      finalized_string = {finalized_string}")
        # return finalized_string
        print(f"      final_ans_string = {final_ans_string}")
        return final_ans_string
    def determine_type_of_value(self, custom_rule_value):
        print(f"\ndetermine_type_of_value()")
        if value := self.extract_env_values(custom_rule_value):
            print("Found in the .env file")
        #TODO: Perhaps change this so that it checks if index 0=( and length-1=) signifying exec instead of running it the way you are!!!
        elif value := self.check_if_custom_rule_exec(custom_rule_value):
            print("Found out this is executable")
        else:
            #value = custom_rule_value
            print("Found out this is Normal  boooo")
        return value
    def extract_env_values(self, custom_values_key):
        print(f"\nextract_env_values()")
        print(f"      self.users_information = {self.users_information}")
        for env_key in self.users_information:
            print(f"      env_key = {env_key}")
            print(f"      custom_values_key = {custom_values_key}")
            if custom_values_key == env_key:
                env_value = self.users_information[env_key]
                print(f"      env_value = {env_value}")
                return env_value
        # v  This should never run
        return NameError
    def check_if_custom_rule_exec(self, custom_rule_value):
        print(f"\ncheck_if_custom_rule_exec()")
        try:
            exec("result = " + custom_rule_value)
            #final_value += str(result) + ' '
            final_value += str(result)
        except Exception as e:
            print(f"Error in executing code: {e}")
        return final_value
  #.env file
    def check_env_file(self, label):
        print(f"\ncheck_env_file()")
        words_in_label = label.split()
        jacc_key = None
        print("words_in_label = ", words_in_label)
        print("label = ", label)
        
        
        #NEW
        found_best_match = self.find_best_match(label)
        print("found_best_match = ", found_best_match)
        
        
        
        if len(words_in_label) <= 2:
            print("This question has 2 words or less.")
            print(words_in_label)
        
        else:
            print("This question has more than 2 words.")
            #! => doc = self.nlp(label)
            #! MOVE THIS SOMEWHERE ELSE -> LIKE TO A POINT AFTER WHEN WE ARE SURE AN ANSWER DOESNT EXIST!!
            named_entities, headword, dependants = self.spacy_extract_key_info(self.nlp(label))
            print(f"named_entities = {named_entities}")
            print(f"headword = {headword}")
            print(f"dependants = {dependants}")
            key = self.generate_key(named_entities, headword, dependants)
            jacc_key = key.lower().replace("_", " ")
            print(F"jacc_key = {jacc_key}")
            label = jacc_key
            #! MOVE THIS SOMEWHERE ELSE -> LIKE TO A POINT AFTER WHEN WE ARE SURE AN ANSWER DOESNT EXIST!!

        
        
        found_best_match = self.find_best_match(label)
        print("found_best_match = ", found_best_match)
        
        
        
        if found_best_match:
            return found_best_match
        #! RECENT CHANGE RECENT CHANGE RECENT CHANGE
        # elif self.jaccard_similarity(jacc_key, label):
        #     return jacc_key
        # else:
        #     #Since `rule` was previously defined you use it as above but since `summary` wasn't {something about Python treats} so just use () with '' inside it and the variable name within the ''
        #     return self.generate_response(self.q_and_a('summary'))
       
        
        #! HERE HERE HERE HERE        
        # else:
        #     jacc_key
        return
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
    
    def find_the_bestest_match(self, label):       #aka - "find_best_match"
        print("\n2)find_best_match()")
        doc1 = self.nlp(label.lower())
        max_similarity = -1
        best_match = None
        synonyms = self.get_synonyms(label)
        print_with_tab = '\t'   #Erase when ready
        print_with_2tabs = '\t\t'   #Erase when ready

        #This compares 
        for key in self.users_information.keys():
            env_key_doc = self.nlp(key.lower().replace("_", " "))
            best_match, max_similarity = self.check_similarity(doc1, env_key_doc, key, label, max_similarity, print_with_tab)

            if len(synonyms) > 0:
                for synonym in synonyms:
                    doc2_syn = self.nlp(synonym.lower().replace("_", " "))
                    best_match, max_similarity = self.check_similarity(doc1, doc2_syn, key, label, max_similarity, print_with_2tabs)

        print("max_similarity = ", max_similarity)
        print("best_match = ", best_match)
        return best_match if max_similarity > 0.90 else None
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
    def check_similarity(self, doc1, doc2, key, label, max_similarity, print_num_tabs):
        self.print_synonym_stuff(doc1, doc2, key, label, max_similarity, print_num_tabs)
        
        similarity = doc1.similarity(doc2)
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = key
            if max_similarity == 1.0:
                return self.handle_match(key, label), max_similarity
        return best_match, max_similarity
    def print_synonym_stuff(self, doc1, doc2, key, label, max_similarity, print_num_tabs):
        print(f"{print_num_tabs}Parameters for check_similarity:")
        print(f"{print_num_tabs}  doc1:            {doc1}")
        print(f"{print_num_tabs}  doc2:            {doc2}")
        print(f"{print_num_tabs}  key:             {key}")
        print(f"{print_num_tabs}  label:           {label}")
        print(f"{print_num_tabs}  max_similarity:  {max_similarity}")
    def handle_match(self, key, label):
        print(f"\nhandle_match()")
        print("MATCH: [ 2.1)find_best_match() -> .similarity(question{*label*} | self.users_information.key)]")
        print("\tusers_information = ", key)
        print("\tlabel = ", label)
        print("\t... value = ", self.users_information[key])
        self.form_input_extended['env_key'] = key
        self.form_input_extended['env_values'].append(self.users_information[key])
        return key
  #CUSTOM_SYNONYMS
    def check_custom_synonyms(self, label):
        print(f"\ncheck_custom_synonyms()")
  # -> config.py
    def compare_label_to_config_keys(self, input_data, config_dict_var):
        print(f"\ncompare_label_to_config_keys()")
        for config_key_capitalized in config_dict_var:
            config_key = config_key_capitalized.lower()
            if input_data['label'] == config_key:
                print(f"MATCH: [ {input_data['label']} = {config_key} ]")
  #Q_AND_A
    def can_summary_answer():
        context = self.q_and_a['summary'] + " " + label
        answer = self.generate_response(context)
        if answer:
            # Input the answer into the form
            safe_print(f"Entering '{answer}' for '{label}'")
            #self.fill_form(label, answer)
        else:
            safe_print(f"No stored answers found for '{label}'")
    def generate_response(self, context):
        print("\ngenerate_response()")
        print("context = ", context)
        input_ids = self.tokenizer.encode(context, return_tensors='pt').to("cuda" if torch.cuda.is_available() else "cpu")

        max_length = len(input_ids[0]) + 100
        output = self.model.generate(input_ids, max_length=max_length, temperature=0.7)
        response = self.tokenizer.decode(output[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        print("response = ", response)
        
        return response

  #store new answers

  
    def generate_key(self, named_entities, headword, dependants):
        print("\ngenerate_key()")
        
        # Using set automatically eliminates duplicates for us!!
        tokens = set(named_entities + [headword] + dependants)
        key = "_".join(tokens).upper()
        print(f"key = {key}")
        return key
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
#workflow_to_find_answer()

#
    def handle_match(self, key, label):
        print(f"\nhandle_match()")
        print("MATCH: [ 2.1)find_best_match() -> .similarity(question{*label*} | self.users_information.key)]")
        print("\tusers_information = ", key)
        print("\tlabel = ", label)
        print("\t... value = ", self.users_information[key])
        self.form_input_extended['env_key'] = key
        self.form_input_extended['env_values'].append(self.users_information[key])
        
        self.form_input_extended['env_html'] = self.extract_css(input_data['html'])
        # self.print_form_input_extended()
        
        return key
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
                
                
            #NEW
            elif child.has_attr('name'):
                name_value = child['name']
                css_selector = f'input[name="{name_value}"]'
                
                
            else:
                raise ValueError('The element does not have an id or a class')

            elemental = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

        return elemental
#







#-----------------------------------------------------



    def init_form_input_label(self):
        self.form_input_label = {
            "mandatory": False,
            "req_questions": [],
            "answers": [],
            "text": False,
            "select": False,
            "radio": False,
            "checkbox": False,
            "button": False,
            "file": False,
            "min_ans_required": 0,
            "max_ans_allowed": 0,
            "q_relationship": 0,
            "not_applicable": False,
            "left_blank": False,
            "out_of_scope": False
        }



#submit_application()
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
    def keep_jobs_applied_to_info(self):
        self.sessions_applied_to_info.append({
            'Job_URL': self.current_url,
            'Company_Name': self.current_jobs_details["company_name"],
            'Job_Title': self.current_jobs_details["job_title"],
            'Company_Job_Location': self.current_jobs_details["job_location"],
            'Company_Department': self.company_job_department,
            'Job_ID_Number': self.job_id_number,
        })
    def keep_jobs_applied_to_info(self):
        self.jobs_applied_to_this_session.append(self.current_jobs_details)
#submit_application()
