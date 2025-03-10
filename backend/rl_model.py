import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from typing import Dict, List, Tuple

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
                "Is it an animal?",
                "Does it live in water?",
                "Is it a mammal?",
                "Can it fly?",
                "Is it a pet?",
                "Is it larger than a human?",
                "Is it a predator?",
                "Does it have fur?",
                "Is it a farm animal?",
                "Is it a bird?",
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
                "dog": {"Is it an animal?": 1, "Does it live in water?": 0, "Is it a mammal?": 1, "Can it fly?": 0, "Is it a pet?": 1},
                "cat": {"Is it an animal?": 1, "Does it live in water?": 0, "Is it a mammal?": 1, "Can it fly?": 0, "Is it a pet?": 1, "Is it a predator?": 1},
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
    
    def get_next_question(self, answers: Dict[str, int]) -> str:
        """
        Get the most informative next question based on current answers
        """
        # Filter entities that match current answers
        possible_entities = []
        
        for entity, attributes in self.entities.items():
            matches = True
            for question, answer in answers.items():
                if question in attributes and attributes[question] != answer:
                    matches = False
                    break
            if matches:
                possible_entities.append(entity)
        
        # Find unanswered questions
        unanswered = [q for q in self.questions if q not in answers]
        
        if not unanswered or not possible_entities:
            return None
        
        # Calculate information gain for each unanswered question
        question_gains = {}
        for question in unanswered:
            gain = self.calculate_information_gain(question, possible_entities)
            question_gains[question] = gain
        
        # Return question with highest information gain
        return max(question_gains, key=question_gains.get)
    
    def predict(self, answers: Dict[str, int]) -> Tuple[str, float]:
        """
        Predict the entity based on current answers
        Returns (entity, confidence)
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
        
        # Only return a prediction if we're confident enough
        if confidence > 0.7 and len(answers) >= 3:
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