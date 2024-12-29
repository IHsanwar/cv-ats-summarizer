import spacy
import PyPDF2
import re
from pathlib import Path
from typing import Dict, List, Optional

class CVSummarizer:
    def __init__(self):
        # Load English language model
        self.nlp = spacy.load("en_core_web_sm")
        
    def read_pdf(self, file_path: str) -> str:
        """
        Read text content from a PDF file
        """
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"Error reading PDF: {str(e)}")
            return ""
        return text

    def extract_contact_info(self, text: str) -> Dict[str, str]:
        """
        Extract contact information using regex patterns
        """
        contact_info = {
            'email': '',
            'phone': '',
            'linkedin': ''
        }
        
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact_info['email'] = email_match.group()
            
        # Phone pattern
        phone_pattern = r'\b(?:\+\d{1,3}[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}\b'
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            contact_info['phone'] = phone_match.group()
            
        # LinkedIn pattern
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_match = re.search(linkedin_pattern, text)
        if linkedin_match:
            contact_info['linkedin'] = linkedin_match.group()
            
        return contact_info

    def extract_skills(self, text: str) -> List[str]:
        """
        Extract skills from the text using NLP
        """
        doc = self.nlp(text)
        skills = []
        
        # Common skill-related keywords
        skill_sections = ['skills', 'technical skills', 'expertise', 'competencies','kemampuan','skill','SKILL']
        
        # Find skills section
        lines = text.lower().split('\n')
        start_index = -1
        
        for i, line in enumerate(lines):
            if any(section in line.lower() for section in skill_sections):
                start_index = i
                break
                
        if start_index != -1:
            # Extract skills from the skills section
            skill_text = ' '.join(lines[start_index:start_index + 10])
            # Extract noun phrases as potential skills
            for chunk in self.nlp(skill_text).noun_chunks:
                if len(chunk.text.split()) <= 3:  # Limit to phrases of 3 words or less
                    skills.append(chunk.text.strip())
                    
        return list(set(skills))  # Remove duplicates

    def extract_experience(self, text: str) -> List[Dict[str, str]]:
        """
        Extract work experience information
        """
        experience = []
        
        # Look for experience section
        experience_headers = ['experience', 'work experience', 'employment history','PENGALAMAN DAN PELATIHAN']
        lines = text.split('\n')
        start_index = -1
        
        for i, line in enumerate(lines):
            if any(header in line.lower() for header in experience_headers):
                start_index = i
                break
                
        if start_index != -1:
            # Process next several lines for experience entries
            current_entry = {}
            for line in lines[start_index + 1:start_index + 15]:  # Look at next 15 lines
                if line.strip():
                    # Try to identify company and position
                    if not current_entry:
                        current_entry['title'] = line.strip()
                    elif 'company' not in current_entry:
                        current_entry['company'] = line.strip()
                    elif 'description' not in current_entry:
                        current_entry['description'] = line.strip()
                        experience.append(current_entry)
                        current_entry = {}
                        
        return experience

    def summarize_cv(self, file_path: str) -> Dict:
        """
        Main function to summarize a CV
        """
        # Read the CV file
        text = self.read_pdf(file_path)
        if not text:
            return {"error": "Could not read CV file"}
            
        # Extract information
        contact_info = self.extract_contact_info(text)
        skills = self.extract_skills(text)
        experience = self.extract_experience(text)
        
        # Create summary
        summary = {
            "contact_information": contact_info,
            "skills": skills,
            "experience": experience,
            "original_length": len(text.split()),
        }
        
        return summary
    
def summarizer(cv_path):
    summarizer = CVSummarizer()
    
    try:
        summary = summarizer.summarize_cv(cv_path)
        
        # Create a summary string with the contact information, skills, and experience
        summary_text = "\n=== CV Summary ===\n"
        
        summary_text += "\nContact Information:\n"
        for key, value in summary["contact_information"].items():
            if value:
                summary_text += f"{key.capitalize()}: {value}\n"
        
        summary_text += "\nSkills:\n"
        for skill in summary["skills"]:
            summary_text += f"- {skill}\n"
        
        summary_text += "\nExperience Highlights:\n"
        for exp in summary["experience"]:
            summary_text += f"\nTitle: {exp.get('title', 'N/A')}\n"
            summary_text += f"Company: {exp.get('company', 'N/A')}\n"
            summary_text += f"Description: {exp.get('description', 'N/A')}\n"
        
        summary_text += f"\nOriginal CV length: {summary['original_length']} words"
        
        return summary_text  # Return the summary text
    
    except Exception as e:
        print(f"Error processing CV: {str(e)}")
        return "Error processing CV"

if __name__ == "__main__":
    main()