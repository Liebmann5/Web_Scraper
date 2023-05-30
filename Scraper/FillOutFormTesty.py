def process_form_inputs(self, form_inputs):
    """Process the form inputs."""
    processed_inputs = []

    for input_data in form_inputs:
        processed_input = self.process_input(input_data)
        if processed_input is not None:
            processed_inputs.append(processed_input)

    return processed_inputs

def process_input(self, input_data):
    """Process a single input."""
    label = input_data['label']
    input_type = self.get_input_type(input_data)

    if input_type is None:
        best_match = self.find_best_match(label)
        if best_match is not None:
            return { 'label': label, 'value': self.users_information[best_match] }
    elif input_type == 'is_multiple_choice':
        # Handle multiple choice input
        pass  # TODO: Implement this
    elif input_type == 'is_file':
        # Handle file input
        pass  # TODO: Implement this

    return None

def fill_form(self, form_inputs):
    """Fill the form with the processed inputs."""
    for input_data in form_inputs:
        label = input_data['label']
        value = input_data['value']
        self.fill_input(label, value)

def fill_input(self, label, value):
    """Fill a single input."""
    # TODO: Implement this
    # This will depend on the specific web scraping library you're using

def find_best_match(self, label):
        """Find the best match for a given label in the user's information."""
        doc1 = self.nlp(label.lower())
        max_similarity = -1
        best_match = None
        synonyms = self.get_synonyms(label)

        for key in self.users_information.keys():
            doc2 = self.nlp(key.lower().replace("_", " "))
            similarity = doc1.similarity(doc2)

            if similarity > max_similarity:
                max_similarity = similarity
                best_match = key

            if max_similarity == 1.0:
                return key

        for synonym in synonyms:
            doc2 = self.nlp(synonym.lower().replace("_", " "))
            similarity = doc2.similarity(doc1)

            if similarity > max_similarity:
                max_similarity = similarity
                best_match = key

            if max_similarity == 1.0:
                return key

        return best_match if max_similarity > 0.75 else None

def get_synonyms(self, word):
    """Get synonyms for a given word."""
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return synonyms

def get_input_type(self, input_data):
    """Get the type of input for a given data."""
    input_type_map = {
        'select': 'is_multiple_choice',
        'checkbox': 'is_multiple_choice',
        'file': 'is_file',
    }
    return input_type_map.get(input_data['type'], None)

def jaccard_similarity(self, sentence1, sentence2):
    """Calculate the Jaccard similarity between two sentences."""
    set1 = set(sentence1.lower().split())
    set2 = set(sentence2.lower().split())
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)

def is_special_case(self, input_data):
    """Check if a given data is a special case."""
    special_case_map = {
        'select': 'is_multiple_choice',
        'checkbox': 'is_multiple_choice',
        'file': 'is_file',
    }
    return special_case_map.get(input_data['type'], None)




def handle_multiple_choice_question(question, env_key, is_required):
    # Get the value from the .env file
    env_value = self.users_information(env_key)

    # If the value is empty and the question is required, skip the form
    if is_required and not env_value:
        skip_form()

    # If the value is not in the predefined values, find the closest match
    if env_value not in get_predefined_values(question):
        env_value = find_closest_match(env_value, get_predefined_values(question))

    # Fill the form with the value
    fill_form(question, env_value)

def handle_text_box_question(question, env_key, is_required):
    # Get the value from the .env file
    env_value = self.users_information(env_key)

    # If the value is empty and the question is required, skip the form
    if is_required and not env_value:
        skip_form()

    # Generate a response using GPT-Neo if the value is a summary
    if is_summary(env_value):
        env_value = generate_response_with_gpt_neo(env_value, question)

    # Fill the form with the value
    fill_form(question, env_value)

def handle_multiple_choice_question(question, env_key, is_required):
    # Get the value from the .env file
    env_value = self.users_information(env_key)

    # If the value is empty and the question is required, skip the form
    if is_required and not env_value:
        skip_form()

    predefined_values = get_predefined_values(question)

    # If the value is not in the predefined values, find the closest match
    if env_value not in predefined_values:
        closest_match = find_closest_match(env_value, predefined_values)
        
        # If there is no close match, prompt the user for input or skip the form
        if closest_match is None:
            # Prompt the user for input or skip the form
            pass
        else:
            env_value = closest_match

    # Fill the form with the value
    fill_form(question, env_value)









def init_form_input_extended(self):
    self.form_input_extended = form_input_extended = {
                                    "mandatory": "True",            #bool: T | F if * is present        #!default value => False
                                    "select": "options",            #options: selectOne/selectAll
                                    "radio": "selectOne",           #options: selectOne
                                    "checkbox": "options",          #options: selectOne/selectAll
                                    "button": ".click()",
                                    "file": ".send_keys()",
                                    
                                    "select all": "False",
                                    "select one": "False",
                                    "mark all": "False",
                                    
                                    "env_key": "matching_env_key",
                                    "env_values": "answer1, answer2, answer3",        #null, blank, incorrect, 
                                }



