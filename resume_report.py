from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import warnings
warnings.filterwarnings("ignore")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    api_key="AIzaSyDQq69AxBRoHywVGL9cQ8bn7R4bbUbhVNE"
)

input_prompt = '''
As an ATS specialist, I meticulously evaluate resumes in tech, software, and data science for a fierce job market. Provide a percentage match, identify keywords, and offer top-tier guidance.

1. **Contact Information:**
   - Full name
   - Phone number (with country code)
   - Email address
   - LinkedIn profile
   - Location (City, State, ZIP code)

2. **Resume Format:**
   - Compatible formats (.docx, .pdf)
   - Proper naming convention

3. **Keywords and Phrases:**
   - Relevant to job description
   - Industry-specific terms
   - Synonyms and variations

4. **Formatting:**
   - Consistent and professional
   - Proper fonts, spacing, headers
   - Bulleted lists for clarity

5. **Work Experience:**
   - Job titles
   - Company names
   - Employment dates
   - Achievements, quantified

6. **Education:**
   - Degree earned
   - Institution name
   - Graduation date
   - Relevant coursework or honors

7. **Skills:**
   - Keywords from job description
   - Specific skills mentioned
   - Soft and hard skills

8. **Quantifiable Achievements:**
   - Measurable accomplishments
   - Metrics and data support

9. **Online Presence:**
   - LinkedIn and relevant profiles
   - Consistency with resume

10. **Customization:**
    - Tailored to job requirements
    - Avoid generic content
    - Address company's needs

11. **Gaps in Employment:**
    - Explain significant gaps
    - Provide context for career breaks

12. **Consistency:**
    - Consistent tense and formatting
    - Uniform language and style

13. **Length:**
    - Appropriate for experience level
    - Concise without omitting key details

14. **Language and Grammar:**
    - Correct grammar and spelling
    - Avoid jargon not understood by ATS
    - Use impactful action verbs

15. **File Naming:**
    - Professional and identifiable (e.g., FirstName_LastName_Resume.pdf)
    - Avoid special characters

16. **Applicant's Contact:**
    - Track interactions or applications
    - Mention referrals or connections

Check and mark all 16 points. Ignore irrelevant info. Consider industry-grade ATS like Oracle Taleo.

Make a table in which it will have 3 columns, first column will show keywords in job description, 2nd column will show keywords in your resume, and third column will show keywords missing. Make another table considering of all 16 points mentioned above, add tick and cross as required.

*Resume:*
{text}

*Job Description:*
{jd}
'''

def get_report(text,jd):
    prompt = PromptTemplate.from_template(input_prompt)
    formatteed_prompt = prompt.format(text = text, jd = jd)
    response = llm.invoke(formatteed_prompt)
    return response