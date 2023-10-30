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
                return self.handle_match(best_match, label), max_similarity
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
            synonyms.extend(lemma.name() for lemma in syn.lemmas())
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
        return jaccard_similarity > 90
    
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
                if is_multiple_choice:
                    self.form_input_extended['text'] = 'is_multiple_choice'
            elif label == 'checkbox':
                self.form_input_extended['checkbox'] = True
                self.form_input_extended = 'is_multiple_choice'
            elif label == 'radio':
                self.form_input_extended['radio'] = True
            elif label == 'file':
                self.form_input_extended['file'] = True
        elif label in ['text', 'textarea', 'button']:
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

