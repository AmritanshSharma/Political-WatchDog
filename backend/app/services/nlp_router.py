import spacy

# Load a small English model (needs to be installed via `python -m spacy download en_core_web_sm`)
# Using a dummy fallback for now in case the model is missing
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None

class NLPRouter:
    def extract_entities(self, text: str):
        """
        Perform NER to extract Official Name, Case Allegation Type, and Case Status.
        """
        if nlp is None:
            # Fallback mock extraction
            return {
                "official_name": "Unknown",
                "allegation_type": "Unknown",
                "status": "Pending"
            }
            
        doc = nlp(text)
        
        persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        
        # Basic heuristic for case extraction (highly simplified)
        allegation_keywords = ["fraud", "corruption", "embezzlement", "assault"]
        allegations = [word for word in text.lower().split() if word in allegation_keywords]
        
        status_keywords = ["pending", "convicted", "acquitted", "dismissed"]
        status = "Unknown"
        for word in text.lower().split():
            if word in status_keywords:
                status = word.title()
                break
                
        return {
            "official_name": persons[0] if persons else "Unknown",
            "allegation_type": allegations[0].title() if allegations else "Unknown",
            "status": status
        }
