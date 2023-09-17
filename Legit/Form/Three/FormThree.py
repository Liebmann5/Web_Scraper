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
                    if matching_keys := self.get_matching_keys(label):
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
                        if answer := self.generate_response(context):
                            # Input the answer into the form
                            print(f"Entering '{answer}' for '{label}'")
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

