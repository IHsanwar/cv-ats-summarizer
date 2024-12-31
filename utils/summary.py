import spacy
import PyPDF2
import re
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class CVSummarizer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        # Common skills dictionary for better recognition
        self.common_skills = {
                'languages': [
                    'python', 'java', 'javascript', 'typescript', 'c', 'c++', 'c#', 'ruby', 
                    'php', 'sql', 'html', 'css', 'swift', 'go', 'rust', 'perl', 'scala', 
                    'r', 'kotlin', 'dart', 'objective-c', 'bash', 'powershell', 'lua', 'haskell', 
                    'vba', 'matlab', 'groovy', 'elixir', 'f#', 'julia', 'sas', 'abap', 'fortran', 
                    'ada', 'cobol', 'solidity', 'assembly', 'flutter'
                ],
                'frameworks': [
                    'django', 'flask', 'fastapi', 'react', 'angular', 'vue', 'next.js', 'nuxt.js', 
                    'svelte', 'ember.js', 'spring', 'rails', 'laravel', 'express', 'symfony', 
                    'nestjs', 'adonisjs', 'meteor', 'struts', 'codeigniter', 'backbone.js', 'quarkus', 
                    'gin', 'bottle', 'pyramid', 'phoenix', 'play framework', 'grails', 'yii', 
                    'hapi.js', 'kivy'
                ],
                'databases': [
                    'mysql', 'postgresql', 'mongodb', 'oracle', 'sql server', 'redis', 'sqlite', 
                    'dynamodb', 'cassandra', 'elasticsearch', 'mariadb', 'firestore', 'arangodb', 
                    'couchdb', 'neo4j', 'hbase', 'ibm db2', 'teradata', 'cockroachdb', 'clickhouse'
                ],
                'tools': [
                    'git', 'docker', 'kubernetes', 'jenkins', 'aws', 'azure', 'gcp', 'terraform', 
                    'ansible', 'vagrant', 'gradle', 'maven', 'circleci', 'travisci', 'helm', 'grafana', 
                    'prometheus', 'splunk', 'sonarqube', 'logstash', 'chef', 'puppet', 'new relic', 
                    'sentry', 'datadog', 'elastic stack', 'tableau', 'power bi'
                ]
}

    def read_pdf(self, file_path: str) -> str:
        """
        Read and extract text from a PDF file with improved error handling and text processing.
        
        Args:
            file_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text from the PDF, or error message if extraction fails
            
        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            PermissionError: If there's no permission to access the file
            PyPDF2.PdfReadError: If the PDF is encrypted or corrupted
        """
        if not Path(file_path).exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")
            
        text_chunks = []
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                if pdf_reader.is_encrypted:
                    raise PyPDF2.PdfReadError("PDF is encrypted and cannot be processed")
                    
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    try:
                        chunk = page.extract_text()
                        if chunk:
                            # Clean up common PDF text extraction issues
                            chunk = re.sub(r'\s+', ' ', chunk)  # Replace multiple spaces
                            chunk = re.sub(r'([a-z])([A-Z])', r'\1 \2', chunk)  # Add space between camelCase
                            text_chunks.append(chunk.strip())
                        else:
                            print(f"Warning: No text extracted from page {page_num}")
                            
                    except Exception as e:
                        print(f"Warning: Failed to extract text from page {page_num}: {str(e)}")
                        continue
                        
        except PermissionError:
            raise PermissionError(f"Permission denied: Unable to access {file_path}")
        except PyPDF2.PdfReadError as e:
            raise PyPDF2.PdfReadError(f"Failed to read PDF: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error while reading PDF: {str(e)}")
            
        if not text_chunks:
            raise ValueError("No text could be extracted from the PDF")
            
        return '\n'.join(text_chunks)

    def extract_profile(self, text: str) -> Dict[str, str]:
        profile = {
            'name': '',
            'email': '',
            'phone': '',
            'linkedin': '',
            'location': '',
            'summary': ''
        }
        
        # Enhanced patterns
        email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        phone_pattern = r'(?:(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})'
        linkedin_pattern = r'(?:linkedin\.com/in/|linkedin:\s*)([^\s/]+)'
        location_pattern = r'(?:Address|Location):\s*([^,\n]+(?:,\s*[^,\n]+)*)'
        
        # Extract name (usually first line of CV)
        first_lines = text.split('\n')[:3]  # Check first 3 lines
        for line in first_lines:
            line = line.strip()
            if line and not any(keyword in line.lower() for keyword in ['resume', 'cv', 'curriculum']):
                profile['name'] = line
                break
        
        # Extract other profile information
        profile['email'] = next(iter(re.findall(email_pattern, text)), '')
        profile['phone'] = next(iter(re.findall(phone_pattern, text)), '')
        linkedin_match = re.search(linkedin_pattern, text, re.I)
        profile['linkedin'] = f"linkedin.com/in/{linkedin_match.group(1)}" if linkedin_match else ''
        
        # Extract location
        location_match = re.search(location_pattern, text, re.I)
        profile['location'] = location_match.group(1) if location_match else ''
        
        # Extract summary/objective
        summary_patterns = [
            r'(?:Professional\s+Summary|Summary|Profile|Objective):\s*([^\n]+(?:\n(?!\n)[^\n]+)*)',
            r'(?:SUMMARY OF QUALIFICATIONS|PROFESSIONAL PROFILE)[\s\n]*([^\n]+(?:\n(?!\n)[^\n]+)*)'
        ]
        
        for pattern in summary_patterns:
            summary_match = re.search(pattern, text, re.I)
            if summary_match:
                profile['summary'] = summary_match.group(1).strip()
                break
                
        return profile

    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        skills_section = {
            'technical_skills': [],
            'soft_skills': [],
            'languages': [],
            'tools': []
        }
        
        # Find skills section
        skill_section_pattern = r'(?:SKILLS|TECHNICAL SKILLS|EXPERTISE).*?\n(.*?)(?:\n\n|\Z)'
        skill_match = re.search(skill_section_pattern, text, re.I | re.DOTALL)
        
        if skill_match:
            skill_text = skill_match.group(1)
            
            # Process each line in the skills section
            for line in skill_text.split('\n'):
                line = line.strip().lower()
                if not line:
                    continue
                    
                # Categorize skills
                if any(lang in line for lang in self.common_skills['languages']):
                    skills_section['technical_skills'].extend(
                        [lang for lang in self.common_skills['languages'] if lang in line]
                    )
                if any(tool in line for tool in self.common_skills['tools']):
                    skills_section['tools'].extend(
                        [tool for tool in self.common_skills['tools'] if tool in line]
                    )
                
                # Extract soft skills
                soft_skills_keywords = ['communication', 'leadership', 'teamwork', 'problem solving',
                                     'analytical', 'organization', 'management']
                for skill in soft_skills_keywords:
                    if skill in line:
                        skills_section['soft_skills'].append(skill)
        
        # Remove duplicates and sort
        for category in skills_section:
            skills_section[category] = sorted(list(set(skills_section[category])))
            
        return skills_section

    def extract_experience(self, text: str) -> List[Dict[str, str]]:
        experience = []
        
        # Find experience section
        exp_section_pattern = r'(?:EXPERIENCE|WORK EXPERIENCE|EMPLOYMENT HISTORY).*?\n(.*?)(?:EDUCATION|SKILLS|\Z)'
        exp_match = re.search(exp_section_pattern, text, re.I | re.DOTALL)
        
        if exp_match:
            exp_text = exp_match.group(1)
            
            # Split into individual positions
            positions = re.split(r'\n\n+', exp_text.strip())
            
            for position in positions:
                if not position.strip():
                    continue
                    
                exp_entry = {
                    'title': '',
                    'company': '',
                    'period': '',
                    'responsibilities': []
                }
                
                lines = position.split('\n')
                
                # Extract title and company
                if lines:
                    first_line = lines[0].strip()
                    if '|' in first_line:
                        parts = first_line.split('|')
                        exp_entry['title'] = parts[0].strip()
                        exp_entry['company'] = parts[1].strip()
                    elif ',' in first_line:
                        parts = first_line.split(',')
                        exp_entry['title'] = parts[0].strip()
                        exp_entry['company'] = parts[1].strip()
                    else:
                        exp_entry['title'] = first_line
                
                # Extract period
                date_pattern = r'(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s.,-]+\d{4})'
                dates = re.findall(date_pattern, position, re.I)
                if len(dates) >= 2:
                    exp_entry['period'] = f"{dates[0]} - {dates[1]}"
                elif len(dates) == 1:
                    exp_entry['period'] = f"{dates[0]} - Present"
                
                # Extract responsibilities
                for line in lines[1:]:
                    line = line.strip()
                    if line and not any(date in line for date in dates):
                        if line.startswith('•') or line.startswith('-'):
                            exp_entry['responsibilities'].append(line[1:].strip())
                        else:
                            exp_entry['responsibilities'].append(line)
                
                if exp_entry['title'] or exp_entry['company']:
                    experience.append(exp_entry)
        
        return experience

    def format_output(self, profile: Dict, skills: Dict, experience: List) -> str:
        output = []
        
        # Format Profile Section
        output.append("PROFILE")
        output.append("=" * 50)
        for key, value in profile.items():
            if value:
                output.append(f"{key.title()}: {value}")
        output.append("")
        
        # Format Skills Section
        output.append("SKILLS")
        output.append("=" * 50)
        for category, skill_list in skills.items():
            if skill_list:
                output.append(f"{category.replace('_', ' ').title()}:")
                output.append("• " + "\n• ".join(skill_list))
                output.append("")
        
        # Format Experience Section
        output.append("EXPERIENCE")
        output.append("=" * 50)
        for exp in experience:
            if exp.get('title') or exp.get('company'):
                output.append(f"{exp.get('title')} | {exp.get('company')}")
                if exp.get('period'):
                    output.append(exp['period'])
                if exp.get('responsibilities'):
                    output.append("\nResponsibilities:")
                    for resp in exp['responsibilities']:
                        output.append(f"• {resp}")
                output.append("")
        
        return "\n".join(output)

    def summarize_cv_regex(self, text: str) -> str:
        if not text:
            return "Error: No text to process"
        
        # Extract information using existing methods
        profile = self.extract_profile(text)
        skills = self.extract_skills(text)
        experience = self.extract_experience(text)
        
        # Format output in desired pattern
        output = []
        
        # Profile paragraph
        profile_parts = []
        if profile.get('name'):
            profile_parts.append(profile['name'])
        if profile.get('email'):
            profile_parts.append(f"Email: {profile['email']}")
        if profile.get('phone'):
            profile_parts.append(f"Phone: {profile['phone']}")
        if profile.get('summary'):
            profile_parts.append(profile['summary'])
        output.append(" | ".join(profile_parts))
        output.append("")
        
        # Skills section with numbering
        output.append("Skills:")
        all_skills = []
        for skill_list in skills.values():
            all_skills.extend(skill_list)
        for i, skill in enumerate(sorted(set(all_skills)), 1):
            output.append(f"{i}. {skill}")
        output.append("")
        
        # Experience section with numbering
        output.append("Experience:")
        for i, exp in enumerate(experience, 1):
            if exp.get('title') and exp.get('company'):
                output.append(f"{i}. {exp['title']} | {exp['company']}")
        
        return "\n".join(output)
    
if __name__ == "__main__":
    summarizer = CVSummarizer()  # Correct instantiation
    cv_summary = summarizer.summarize_cv("path/to/cv.pdf")
    print(cv_summary)