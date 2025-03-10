import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class AkinatorRL:
    def __init__(self, questions_file="questions.pkl", entities_file="entities.pkl"):
        self.questions_path = Path(questions_file)
        self.entities_path = Path(entities_file)
        
        # Load or initialize questions and their weights
        if self.questions_path.exists():
            with open(self.questions_path, 'rb') as f:
                self.questions, self.question_weights = pickle.load(f)
        else:
            # Initial questions
            self.questions = [
                # Basic classification
                "Is it an animal?",
                "Is it a person?",
                "Is it a fictional character?",
                "Is it an object?",
                "Is it a place?",
                "Is it a food or drink?",
                "Is it a plant?",
                "Is it a vehicle?",
                "Is it technology-related?",
                
                # Animal questions
                "Does it live in water?",
                "Is it a mammal?",
                "Is it a bird?",
                "Is it a reptile?",
                "Is it an insect?",
                "Is it a fish?",
                "Can it fly?",
                "Is it a predator?",
                "Is it a pet?",
                "Is it a farm animal?",
                "Is it wild?",
                "Does it have fur?",
                "Does it have scales?",
                "Does it have feathers?",
                "Is it larger than a human?",
                "Is it smaller than a cat?",
                "Is it dangerous to humans?",
                "Is it nocturnal?",
                "Does it live in a group/herd?",
                "Is it endangered?",
                
                # Person questions
                "Is this person alive?",
                "Is this person male?",
                "Is this person famous?",
                "Is this person an actor/actress?",
                "Is this person a musician?",
                "Is this person a politician?",
                "Is this person an athlete?",
                "Is this person a scientist?",
                "Is this person a writer?",
                "Is this person a historical figure?",
                "Is this person American?",
                "Is this person European?",
                "Is this person Asian?",
                "Is this person older than 50?",
                "Is this person younger than 30?",
                
                # Object questions
                "Is it electronic?",
                "Is it used in the kitchen?",
                "Is it used for transportation?",
                "Is it furniture?",
                "Is it a tool?",
                "Is it a toy?",
                "Is it clothing?",
                "Is it made of metal?",
                "Is it made of wood?",
                "Is it made of plastic?",
                "Can you hold it in your hand?",
                "Is it expensive?",
                "Is it used daily?",
                "Is it found in most homes?",
                
                # Food/drink questions
                "Is it a fruit?",
                "Is it a vegetable?",
                "Is it a dessert?",
                "Is it a beverage?",
                "Is it alcoholic?",
                "Is it spicy?",
                "Is it sweet?",
                "Is it sour?",
                "Is it eaten raw?",
                "Is it cooked?",
                "Is it a main dish?",
                "Is it a snack?",
                
                # Place questions
                "Is it a country?",
                "Is it a city?",
                "Is it a natural landmark?",
                "Is it a building?",
                "Is it a tourist destination?",
                "Is it in Europe?",
                "Is it in Asia?",
                "Is it in North America?",
                "Is it in the Southern Hemisphere?",
                "Is it near water?",
                "Is it in a desert?",
                "Is it in a forest?",
                "Is it mountainous?",
                
                # Technology questions
                "Is it a computer?",
                "Is it a mobile device?",
                "Is it software?",
                "Is it used for communication?",
                "Is it used for entertainment?",
                "Was it invented in the last 20 years?",
                "Is it connected to the internet?",
                
                # Fictional character questions
                "Is this character from a movie?",
                "Is this character from a TV show?",
                "Is this character from a book?",
                "Is this character from a video game?",
                "Is this character from a comic/manga?",
                "Is this character human?",
                "Is this character a superhero?",
                "Is this character a villain?",
                "Is this character animated?",
                "Is this character from Disney?",
                "Is this character from Marvel or DC?",
                "Is this character magical or has superpowers?",
                
                # Vehicle questions
                "Does it travel on land?",
                "Does it travel on water?",
                "Does it travel in air?",
                "Does it have wheels?",
                "Does it have an engine?",
                "Is it powered by humans?",
                "Can it carry multiple people?",
                "Is it used for public transportation?",
                "Is it used for transporting goods?",
                "Is it faster than a car?",
                
                # General questions
                "Is it colorful?",
                "Is it larger than a microwave?",
                "Is it smaller than a shoe?",
                "Is it heavy?",
                "Is it valuable?",
                "Is it older than 100 years?",
                "Is it modern (created in the last 50 years)?",
                "Is it used for entertainment?",
                "Is it used for work?",
                "Is it rare?",
                "Is it common in households?",
                "Is it seasonal?",
                "Is it associated with a specific culture?",
                "Is it associated with a specific holiday?",
                "Is it used outdoors?",
                "Is it used indoors?",
            ]
            # Initialize weights (higher = more informative)
            self.question_weights = {q: 1.0 for q in self.questions}
        
        # Load or initialize entities
        if self.entities_path.exists():
            with open(self.entities_path, 'rb') as f:
                self.entities = pickle.load(f)
        else:
            # Initial entities with their attributes
            self.entities = {
                "dog": {
                    "Is it an animal?": 1, 
                    "Does it live in water?": 0, 
                    "Is it a mammal?": 1, 
                    "Can it fly?": 0, 
                    "Is it a pet?": 1,
                    "Is it a predator?": 0,
                    "Does it have fur?": 1,
                    "Is it larger than a microwave?": 0,
                    "Is it smaller than a shoe?": 0,
                    "Is it dangerous to humans?": 0,
                    "Is it a farm animal?": 0,
                    "Is it wild?": 0,
                    "Is it colorful?": 0,
                    "Is it rare?": 0,
                    "Is it common in households?": 1
                },
                "cat": {
                    "Is it an animal?": 1, 
                    "Does it live in water?": 0, 
                    "Is it a mammal?": 1, 
                    "Can it fly?": 0, 
                    "Is it a pet?": 1, 
                    "Is it a predator?": 1,
                    "Does it have fur?": 1,
                    "Is it larger than a microwave?": 0,
                    "Is it smaller than a shoe?": 0,
                    "Is it dangerous to humans?": 0,
                    "Is it a farm animal?": 0,
                    "Is it wild?": 0,
                    "Is it colorful?": 0,
                    "Is it rare?": 0,
                    "Is it common in households?": 1
                },
                "fish": {"Is it an animal?": 1, "Does it live in water?": 1, "Is it a mammal?": 0},
                "bird": {"Is it an animal?": 1, "Does it live in water?": 0, "Can it fly?": 1},
                "elephant": {"Is it an animal?": 1, "Does it live in water?": 0, "Is it a mammal?": 1, "Can it fly?": 0, "Is it larger than a human?": 1},
            }
    
    def save(self):
        """Save the current state of questions and entities"""
        with open(self.questions_path, 'wb') as f:
            pickle.dump((self.questions, self.question_weights), f)
        
        with open(self.entities_path, 'wb') as f:
            pickle.dump(self.entities, f)
    
    def calculate_information_gain(self, question: str, current_entities: List[str]) -> float:
        """
        Calculate information gain for a question based on current possible entities
        Higher gain = better question to ask
        """
        if not current_entities or question not in self.question_weights:
            return 0.0
        
        # Count yes/no answers for this question among current entities
        yes_count = 0
        no_count = 0
        unknown_count = 0
        
        for entity in current_entities:
            if entity in self.entities and question in self.entities[entity]:
                if self.entities[entity][question] == 1:
                    yes_count += 1
                else:
                    no_count += 1
            else:
                unknown_count += 1
        
        total = yes_count + no_count + unknown_count
        
        # Perfect split would be 50/50
        # The closer to 50/50, the higher the information gain
        if total == 0:
            return 0.0
        
        yes_ratio = yes_count / total
        no_ratio = no_count / total
        
        # Calculate how close the split is to 50/50
        # 0.5 is perfect, 0 or 1 is worst
        balance = 1.0 - abs(0.5 - yes_ratio) * 2
        
        # Penalize questions with many unknowns
        known_ratio = (yes_count + no_count) / total
        
        # Combine balance and known_ratio with the question's weight
        return balance * known_ratio * self.question_weights[question]
    
    def get_next_question(self, answers: Dict[str, int]) -> Optional[str]:
        """
        Get the next most informative question to ask
        """
        # Filter questions not yet answered
        unanswered = [q for q in self.questions if q not in answers]
        if not unanswered:
            return None
        
        # If we have no answers yet, start with a basic classification question
        if not answers:
            basic_questions = [
                "Is it an animal?",
                "Is it a person?",
                "Is it a fictional character?",
                "Is it an object?",
                "Is it a place?",
                "Is it a food or drink?",
            ]
            available_basics = [q for q in basic_questions if q in unanswered]
            if available_basics:
                return available_basics[0]
        
        # Filter entities that match our current answers
        matching_entities = []
        for entity, attributes in self.entities.items():
            matches = True
            for question, answer in answers.items():
                if question in attributes and attributes[question] != answer:
                    matches = False
                    break
            if matches:
                matching_entities.append(entity)
        
        # If no matching entities, just return a random unanswered question
        if not matching_entities:
            # Sort by weight (most informative first) and return the top one
            return sorted(unanswered, key=lambda q: self.question_weights.get(q, 0), reverse=True)[0]
        
        # Calculate information gain for each unanswered question
        question_gains = {}
        for question in unanswered:
            # Skip questions that are irrelevant based on previous answers
            if self._is_question_irrelevant(question, answers):
                continue
            
            # Calculate how well this question divides the remaining entities
            yes_count = 0
            no_count = 0
            unknown_count = 0
            
            for entity in matching_entities:
                if question in self.entities[entity]:
                    if self.entities[entity][question] == 1:
                        yes_count += 1
                    else:
                        no_count += 1
                else:
                    unknown_count += 1
            
            # Perfect question divides the set in half
            total = yes_count + no_count + unknown_count
            if total > 0:
                # Calculate how balanced the split is (closer to 0.5 is better)
                balance = min(yes_count / total, no_count / total)
                # Adjust by the question weight
                question_gains[question] = balance * self.question_weights.get(question, 1.0)
        
        # If we have gains, return the question with highest gain
        if question_gains:
            return max(question_gains, key=question_gains.get)
        
        # Fallback to a random question sorted by weight
        return sorted(unanswered, key=lambda q: self.question_weights.get(q, 0), reverse=True)[0]
    
    def _is_question_irrelevant(self, question: str, answers: Dict[str, int]) -> bool:
        """
        Determine if a question is irrelevant based on previous answers
        """
        # If user said it's not an animal, don't ask animal-specific questions
        if "Is it an animal?" in answers and answers["Is it an animal?"] == 0:
            animal_questions = [
                "Does it live in water?", "Is it a mammal?", "Is it a bird?",
                "Is it a reptile?", "Is it an insect?", "Is it a fish?",
                "Can it fly?", "Is it a predator?", "Is it a pet?",
                "Is it a farm animal?", "Is it wild?", "Does it have fur?",
                "Does it have scales?", "Does it have feathers?",
                "Is it smaller than a cat?", "Is it dangerous to humans?",
                "Is it nocturnal?", "Does it live in a group/herd?",
                "Is it endangered?"
            ]
            if question in animal_questions:
                return True
        
        # If user said it's not a person, don't ask person-specific questions
        if "Is it a person?" in answers and answers["Is it a person?"] == 0:
            person_questions = [
                "Is this person alive?", "Is this person male?",
                "Is this person famous?", "Is this person an actor/actress?",
                "Is this person a musician?", "Is this person a politician?",
                "Is this person an athlete?", "Is this person a scientist?",
                "Is this person a writer?", "Is this person a historical figure?",
                "Is this person American?", "Is this person European?",
                "Is this person Asian?", "Is this person older than 50?",
                "Is this person younger than 30?"
            ]
            if question in person_questions:
                return True
        
        # Add similar logic for other categories
        
        return False
    
    def predict(self, answers: Dict[str, int]) -> Tuple[Optional[str], float]:
        """
        Make a prediction based on the answers provided so far
        Returns (entity, confidence) or (None, confidence) if no confident prediction
        """
        if not answers:
            return None, 0.0
        
        # Calculate match scores for each entity
        scores = {}
        for entity, attributes in self.entities.items():
            match_count = 0
            total_questions = 0
            
            for question, answer in answers.items():
                if question in attributes:
                    total_questions += 1
                    if attributes[question] == answer:
                        match_count += 1
            
            if total_questions > 0:
                scores[entity] = match_count / total_questions
        
        if not scores:
            return None, 0.0
        
        # Find the best match
        best_entity = max(scores, key=scores.get)
        confidence = scores[best_entity]
        
        # Only return a prediction if we're confident enough AND have asked enough questions
        # Increase the minimum questions threshold from 3 to 8
        # Increase the confidence threshold from 0.7 to 0.8
        if confidence > 0.8 and len(answers) >= 8:
            return best_entity, confidence
        return None, confidence
    
    def update_from_feedback(self, entity: str, answers: Dict[str, int], correct: bool):
        """
        Update the model based on user feedback
        """
        if correct:
            # Add or update entity
            self.entities[entity] = answers
            
            # Slightly increase weights of questions that were asked
            for question in answers:
                if question in self.question_weights:
                    self.question_weights[question] *= 1.05  # 5% increase
        else:
            # If prediction was wrong, slightly decrease weights of questions that were asked
            for question in answers:
                if question in self.question_weights:
                    self.question_weights[question] *= 0.95  # 5% decrease
        
        # Normalize weights to prevent extreme values
        max_weight = max(self.question_weights.values())
        if max_weight > 10.0:
            for q in self.question_weights:
                self.question_weights[q] /= max_weight / 5.0
        
        # Save updated model
        self.save()
    
    def add_question(self, question: str):
        """Add a new question to the system"""
        if question not in self.questions:
            self.questions.append(question)
            self.question_weights[question] = 1.0
            self.save() 