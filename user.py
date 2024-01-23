import re
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from docx import Document

import pymongo

###### Import Libraries ######
import nltk
nltk.download('stopwords')
import streamlit as st
import pandas as pd
import base64,io,random 
import time,datetime
from streamlit_tags import st_tags

###### Libraries for pdf tools ######

from pyresparser import ResumeParser
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import textwrap 

###### Import Courses and  Database File ######

from Courses import*
from database import CreateTable,insert_data


###### Machine Learning Algortihm ######

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer



def store_resumedata_in_mongodb(name, email, mobile_number, job_title,score, experience,timestamp, mongodb_connection_string):
    # Connect to MongoDB
    client = pymongo.MongoClient(mongodb_connection_string)

    # Choose the database
    db_name = 'Users'
    db = client[db_name]

    # Choose the collection
    collection_name = 'Resume_Data'
    collection = db[collection_name]

    # Prepare the document to be inserted
    resume_data = {
        'Name': name,
        'Email': email,
        'Mobile Number': mobile_number,
        'Job Title': job_title,
        'Experience': experience,
        'Resume Score': score,
        'Timestamp':timestamp
    }

    # Insert the document into the collection
    result = collection.insert_one(resume_data)

    # Check if the insertion was successful
    if result.inserted_id:
        st.success('\nUser data successfully stored in MongoDB !')
    else:
        st.error('Failed to store resume data in MongoDB.')


def convert_docx_to_txt(docx_file):
    doc = Document(docx_file)
    text = [paragraph.text for paragraph in doc.paragraphs]
    return '\n'.join(text)


def convert_pdf_to_txt(pdf_file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    for page in PDFPage.get_pages(pdf_file):
        page_interpreter.process_page(page)
    text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()
    return text

def course_recommender(course_list):
    st.markdown('''<h4 style='text-align:center;margin-bottom:20px;font-family:Bungee;font-style:underline; margin-top:30px; font-size:50px; color: #080506; background-color:#a99a86;letter-spacing:5px'>Courses & Certificates Recommendations ''',unsafe_allow_html=True)
    c = 0
    rec_course = []
    ## slider to choose from range 1-10
    no_of_reco =5
    random.shuffle(course_list)
    for c_name, c_link in course_list:
        c += 1
        st.markdown(f"({c}) [{c_name}]({c_link})")
        rec_course.append(c_name)
        if c == no_of_reco:
            break
    return rec_course


# def NormalUser():
#     pdf_file = st.file_uploader("Choose your Resume", type=['pdf'])
#     if pdf_file is not None:
#         with st.spinner('Hang On While We Cook Magic For You...'):
#             time.sleep(3)
#         file_bytes = base64.b64encode(pdf_file.read()).decode()
#         #st.write(f'<iframe src="data:application/pdf;base64,{file_bytes}" width="600" height="900"></iframe>', unsafe_allow_html=True)
#         resume_text = convert_pdf_to_txt(pdf_file)
#         resume_data = ResumeParser(pdf_file).get_extracted_data()
#         if resume_data:
#             st.header("**Resume Analysis ✉️**")
#             st.success("Hello "+ resume_data['name'])
#             st.subheader("**Your Basic info 📋**")


def generate_pdf_report(resume_data, resume_score, cand_level, clf, current_skills, recommended_skills, recommended_courses, resume_tips):
    buffer = io.BytesIO()

    # Create PDF
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, "Resume Report")
    p.drawString(100, 730, "Name: " + resume_data['name'])
    p.drawString(100, 710, "Email: " + resume_data['email'])
    p.drawString(100, 690, "Contact: " + resume_data['mobile_number'])
    p.drawString(100, 670, "Resume Score: " + str(resume_score))
    p.drawString(100, 650, "Experience Level: " + cand_level)
    p.drawString(100, 630, "Predicted Job Title: " + clf)

    # Convert current_skills list to a string
    current_skills_str = ', '.join(current_skills)
    # p.drawString(100, 610, "Current Skills: " + current_skills_str)
    # p.drawString(100, 590, "Recommended Skills: " + ', '.join(recommended_skills))
    # p.drawString(100, 570, "Recommended Courses: " + ", ".join(recommended_courses))
    p.drawString(100, 550, "Tips and Ideas:")

    # Add Tips and Ideas from the provided dictionary
    y_position = 530  # Starting y-position for tips
    for tip_category, tip_content in resume_tips.items():
        # Adjust x-position and line wrapping
        lines = textwrap.wrap(f"{tip_category}: {tip_content}", width=80)
        for line in lines:
            p.drawString(120, y_position, line)
            y_position -= 15  # Adjust this value as needed to space out the lines

    # Add more information to the PDF as needed

    p.save()

    buffer.seek(0)
    return buffer


def NormalUser():
    internship_pattern = re.compile(r'\binternship(s)?\b', flags=re.IGNORECASE)
    experience_pattern = re.compile(r'\bexperience\b', flags=re.IGNORECASE)    
    file_type = st.radio("Choose File Type", ["PDF", "DOCX"])

    if file_type == "PDF":
        pdf_file = st.file_uploader("Choose your Resume (PDF)", type=['pdf'])
    
        if pdf_file is not None:
                # Display the selected resume as an iframe
                file_bytes = base64.b64encode(pdf_file.read()).decode()
                iframe_code = f'<br><iframe src="data:application/pdf;base64,{file_bytes}" width="680" height="950"></iframe>'
                st.markdown(iframe_code, unsafe_allow_html=True)

    

                with st.spinner('Hang On While We Cook Magic For You...'):
                    time.sleep(3)
        
                # Rest of your code for resume analysis
                resume_text = convert_pdf_to_txt(pdf_file)
                resume_data = ResumeParser(pdf_file).get_extracted_data()
                try:
                    st.header("\n\n")
                #    st.title("\n\n** -------  Resume Analysis  -------✉️**\n")
                    st.markdown('''<h4 style='padding:10px;text-align:center;margin-bottom:20px;font-family:Fantasy;font-style:underline; margin-top:30px; font-size:50px; color: #771414; background-color:#d5d3d3;letter-spacing:5px'>-------  Resume Analysis ✉️  ------- ''',unsafe_allow_html=True)

                    st.text("\n")
                    st.success("\nDear "+" "+resume_data['name']+" !! Welcome to WSH Resume Analyzer 🙂"+"\n")
                    # st.header("**Your Basic info 📋**")
                    
                    # st.text('Name: '+resume_data['name'])
                    # st.text('Email: ' + resume_data['email'])
                    # st.text('Contact: ' + resume_data['mobile_number'])
                    # st.text('Skills: '+resume_data['skills'])
                    
                    st.header("**Your Basic info 📋**")

                    # Assuming resume_data is a dictionary with keys 'name', 'email', 'mobile_number', 'total_experience'
                    table_data = {
                        'Attributes': ['Name', 'Email', 'Contact', 'Experience'],
                        'Details': [resume_data['name'], resume_data['email'], resume_data['mobile_number'], resume_data['total_experience']]
                    }
                    
                    # Create a Markdown table
                    markdown_table = "| Attributes | Details |\n| --- | --- |\n"
                    for attribute, detail in zip(table_data['Attributes'], table_data['Details']):
                        markdown_table += f"| {attribute} | {detail} |\n"
                    
                    # Display the Markdown table using st.write
                    st.write(markdown_table, unsafe_allow_html=True)
                            #     print(resume_data['skills'])
            
                #   st.text('Skills: '+resume_data['skills'])
                except:
                    pass
                    
                try:
                    st.text('Degree: ' + resume_data['degree'])
                except:
                    pass
                    
                try:
                    st.text('College_Name: ' + resume_data['college_name'])
                except:
                    pass
                    
                try:
                
                #  st.table(table_data, columns=column_names)
                #  st.text('Year of Experience: ' + str(resume_data['total_experience']))
                # st.text("Designition" + str(resume_data["designition"]))
                
                    st.success(f"\n\nDesignition: {resume_data['designition']}")
                # st.markdown(f"Designition: {resume_data['designition']}")

                except:
                    pass
                        
                    
                    ## Predicting Candidate Experience Level 
                    
                cand_level = ''
                if resume_data['no_of_pages'] < 1:                
                    cand_level = "NA"
                    st.markdown( '''<h4 style='text-align:center; margin-top:20px; color: #080506; background-color:#e1dddf;letter-spacing:3px'>You are at Fresher level!</h4>''',unsafe_allow_html=True)
                    
                    #### if internship then intermediate level
                        
                elif internship_pattern.search(resume_text):
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align:center; margin-top:20px; color: #080506; background-color:#e1dddf;letter-spacing:3px'>You are at intermediate level!</h4>''', unsafe_allow_html=True)

                # Check for work experience using regular expression
                
                elif experience_pattern.search(resume_text):
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align:center; margin-top:20px; color: #080506; background-color:#e1dddf;letter-spacing:3px'>You are at experience level!</h4>''', unsafe_allow_html=True)
                
                else:
                    cand_level = "Fresher"
                    st.markdown('''<h4 style='text-align:center; margin-top:20px; color: #080506; background-color:#e1dddf;letter-spacing:3px'>You are at Fresher level!!''',unsafe_allow_html=True)
                    
            
                    ## Skills Analyzing and Recommendation
            
                st.markdown('''<h4 style='text-align:center;margin-bottom:20px;font-family:Bungee;font-style:underline; margin-top:30px; font-size:50px; color: #080506; background-color:#a99a86;letter-spacing:5px'>Skills Evaluation ''',unsafe_allow_html=True)     
            

                keywords = st_tags(label='### Your Current Skills',
                text='See our skills recommendation below',value=resume_data['skills'],key='1')
                                            ###### Job Role Predication ######

                # Load the job role and skills dataset
        #     df = pd.read_csv('data.csv')

                # Create a CountVectorizer object to convert job skills to a matrix of token counts
            #    vectorizer = CountVectorizer(stop_words='english')

                # Fit the vectorizer on the job skills data
        #     X = vectorizer.fit_transform(df['skills'])

                # Train the Naive Bayes model
            #   clf = MultinomialNB().fit(X, df['job_role'])
                
                
                
                
                
                with open('data.json', 'r') as file:
                    data = json.load(file)

                # Flatten the data into a list of strings for each job title
                job_titles = list(data.keys())
                job_skills = [' '.join(data[title]) for title in job_titles]
                
                
                vectorizer = CountVectorizer()
                job_skills_matrix = vectorizer.fit_transform(job_skills)
                
                def predict_job_title(input_skills):
                    # Transform the input skills using the same vectorizer
                    input_skills_matrix = vectorizer.transform([' '.join(input_skills)])
                
                    # Calculate cosine similarity 
                    similarity = cosine_similarity(input_skills_matrix, job_skills_matrix)
                
                    # Get the index of the job title with the highest similarity
                    predicted_index = similarity.argmax()
                
                    return job_titles[predicted_index]
                
                def get_missing_skills(predicted_job_title, input_skills):
                    # Get the skills associated with the predicted job title
                    predicted_job_skills = data[predicted_job_title]
                
                    # Find the skills that are present in predicted_job_skills but not in input_skills
                    missing_skills = list(set(predicted_job_skills) - set(input_skills))
                
                    return missing_skills
                
            
                my_Skills = resume_data['skills']
                
                print(my_Skills)
                
                clf= predict_job_title(my_Skills)
                
                print(f"The predicted job title based on input skills is: {clf}")
                
                remaining_skills = get_missing_skills(clf,resume_data['skills'])
                
                print(f"Remaining skills for {clf}: {remaining_skills}")
            
        
                st.success("** Our analysis says you are looking for Jobs in {} **".format(clf))
                
                
                recommended_skills = remaining_skills
            

                # Display recommended skills 
                recommended_keywords = st_tags(label='### Recommended skills for you.',
                                text='Recommended skills generated from System',
                                value=recommended_skills,
                                key='2')
                
                if clf=="Web Developer":
                    rec_course = course_recommender(web_developer_courses)
                    
                elif clf == "Software Developer":
                    rec_course = course_recommender(software_developer_courses)
                
                    pass
                elif clf == "Mobile App Developer":
                    rec_course = course_recommender(mobile_app_developer_courses)
                    pass
                elif clf == "Data Analyst":
                    rec_course = course_recommender(data_analyst_courses)
                    pass
                elif clf == "Systems Analyst":
                    rec_course = course_recommender(systems_analyst_courses)
                    pass
                elif clf == "Quality Assurance Engineer":
                    rec_course = course_recommender(qa_engineer_courses)
                    pass
                elif clf == "DevOps Engineer":
                    rec_course = course_recommender(devops_engineer_courses)
                    pass
                elif clf == "Network Administrator":
                    rec_course = course_recommender(network_administrator_courses)
                    pass
                elif clf == "Cybersecurity Analyst":
                    rec_course = course_recommender(cyber_security_analyst_courses)
                    pass
                elif clf == "Game Developer":
                    rec_course = course_recommender(game_developer_courses)
                    pass
                elif clf == "UIUX Designer":
                    rec_course = course_recommender(uiux_designer_courses)
                    pass
                elif clf == "Database Administrator":
                    rec_course = course_recommender(database_administrator_courses)
                    pass
                elif clf == "Cloud Solutions Architect":
                    rec_course = course_recommender(cloud_solutions_architect_courses)
                    pass
                elif clf == "Machine Learning Engineer":
                    rec_course = course_recommender(machine_learning_engineer_courses)
                    pass
                elif clf == "Full Stack Developer":
                    rec_course = course_recommender(full_stack_developer_courses)
                    pass
                elif clf == "MERN Stack Developer":
                    rec_course = course_recommender(mern_stack_developer_courses)
                    pass
                elif clf == "MEAN Stack Developer":
                    rec_course = course_recommender(mean_stack_developer_courses)
                    pass  
                
                elif clf == "Graphic Designer":
                    rec_course = course_recommender(graphic_designer_courses)
                    pass  
                
                elif clf == "Content Creator":
                    rec_course = course_recommender(content_creator_courses)
                    pass    
                
                elif clf == "Media Planner":
                    rec_course = course_recommender(media_planner_courses)
                    pass    
            
                elif clf == "Digital Marketing Specialist":
                    rec_course = course_recommender(digital_marketing_specialist_courses)
                    pass 
                
                elif clf == "Video Producer":
                    rec_course = course_recommender(video_producer_courses)
                    pass   
                
                
                elif clf == "Public Relations Officer":
                    rec_course = course_recommender(public_relations_officer_courses)
                    pass     
                
                elif clf == "Social Media Manager":
                    rec_course = course_recommender(social_media_manager_courses)
                    pass    
                
                elif clf == "Journalist":
                    rec_course = course_recommender(journalist_courses)
                    pass    
                
                elif clf == "Broadcast Producer":
                    rec_course = course_recommender(broadcast_producer_courses)
                    pass    
                
                elif clf == "Event Coordinator":
                    rec_course = course_recommender(event_coordinator_courses)
                    pass   
                    
                elif clf == "Photographer":
                    rec_course = course_recommender(photographer_courses)
                    pass
                
                elif clf == "Media Research Analyst":
                    rec_course = course_recommender(media_research_analyst_courses)
                    pass       
                
                
                elif clf == "Audio Engineer":
                    rec_course = course_recommender(audio_engineer_courses)
                    pass   
                
                elif clf == "Media Educator":
                    rec_course = course_recommender(media_educator_courses)
                    pass   
                
                elif clf == "Virtual Events Specialist":
                    rec_course = course_recommender(virtual_events_specialist_courses)
                    pass   
            
                
                elif clf == "Business Analyst":
                    rec_course = course_recommender(business_analyst_courses)
                
                    pass
                
                elif clf == "Financial Analyst":
                    rec_course = course_recommender(financial_analyst_courses)
                
                    pass
                elif clf == "Marketing Manager":
                    rec_course = course_recommender(marketing_manager_courses)
                    pass
                elif clf == "Human Resources Specialist":
                    rec_course = course_recommender(human_resources_specialist_courses)
                
                    pass
                elif clf == "Supply Chain Analyst":
                    rec_course = course_recommender(supply_chain_analyst_courses)
                    
                    
                    pass
                elif clf == "Operations Manager":
                    rec_course = course_recommender(operations_manager_courses)
                    
                    pass
                elif clf == "Management Consultant":
                    rec_course = course_recommender(management_consultant_courses)
                
                    pass
                elif clf == "Entrepreneur":
                    rec_course = course_recommender(entrepreneur_courses)
            
                    pass
                elif clf == "Sales Manager":
                    rec_course = course_recommender(sales_manager_courses)
                    
                    pass
                elif clf == "Retail Manager":
                    rec_course = course_recommender(retail_manager_courses)
            
                    pass
                elif clf == "Event Planner":
                    rec_course = course_recommender(event_planner_courses)
                
                    pass
                elif clf == "Public Relations Specialist":
                    rec_course = course_recommender(public_relations_specialist_courses)
                
                    pass
                elif clf == "Healthcare Administrator":
                    rec_course = course_recommender(healthcare_administrator_courses)
                    
                    pass
                elif clf == "International Business Specialist":
                    rec_course = course_recommender(international_business_specialist_courses)
                
                    pass
                elif clf == "E-commerce Manager":
                    rec_course = course_recommender(e_commerce_manager_courses)
                
                if clf == "General Practitioner":
                    rec_course = course_recommender(general_practitioner_courses)
                elif clf == "Surgeon":
                    rec_course = course_recommender(surgeon_courses)
                elif clf == "Cardiologist":
                    rec_course = course_recommender(cardiologist_courses)
                elif clf == "Pediatrician":
                    rec_course = course_recommender(pediatrician_courses)
                elif clf == "Orthopedic Surgeon":
                    rec_course = course_recommender(orthopedic_surgeon_courses)
                elif clf == "Neurologist":
                    rec_course = course_recommender(neurologist_courses)
                elif clf == "Psychiatrist":
                    rec_course = course_recommender(psychiatrist_courses)
                elif clf == "Ophthalmologist":
                    rec_course = course_recommender(ophthalmologist_courses)
                elif clf == "Gynecologist":
                    rec_course = course_recommender(gynecologist_courses)
                elif clf == "Dermatologist":
                    rec_course = course_recommender(dermatologist_courses)
                elif clf == "Anesthesiologist":
                    rec_course = course_recommender(anesthesiologist_courses)
                elif clf == "Radiologist":
                    rec_course = course_recommender(radiologist_courses)
                elif clf == "Emergency Medicine Physician":
                    rec_course = course_recommender(emergency_medicine_physician_courses)
                elif clf == "Pathologist":
                    rec_course = course_recommender(pathologist_courses)
                elif clf == "Medical Researcher":
                    rec_course = course_recommender(medical_researcher_courses)
                else:
                    
                    print("Nor Available")


                    # Randomly select 2 links from each array
                    random_resume_links = random.sample(resume_videos, 2)
                    random_interview_links = random.sample(interview_videos, 2)
                    
                    # st.text("\n\n")
                    # st.subheader("Resume Betterment Videos ▶")
                    # for video_id in random_resume_links:
                    #     video_url = f'{video_id}'
                    #     st.video(video_url, width=500, height=400)
                    
                    # st.text("\n\n")
                    # st.subheader("Interview Videos ▶")
                    # for video_id in random_resume_links:
                    #     video_url = f'{video_id}'
                    #     st.video(video_url, width=500, height=400)
                        

                    st.markdown('''<h4 style='text-align:center;margin-bottom:20px;font-family:Bungee;font-style:underline; margin-top:30px; font-size:50px; color: #080506; background-color:#a99a86;letter-spacing:5px'>Resume Betterment Videos Links ▶''',unsafe_allow_html=True)
                    
                    for link in random_resume_links:
                        st.markdown(f'<br><iframe width="560" height="315" src="{link}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
                    
                    
                
                    st.markdown('''<h4 style='text-align:center;margin-bottom:20px;font-family:Bungee;font-style:underline; margin-top:30px; font-size:50px; color: #080506; background-color:#a99a86;letter-spacing:5px'>Interview Perperation Videos Links  ▶''',unsafe_allow_html=True)
                    for link in random_interview_links:
                        st.markdown(f'<iframe width="560" height="315" src="{link}" frameborder="0" allowfullscreen style="margin-top:20px"></iframe>', unsafe_allow_html=True)
                    
                    # st.subheader("Resume Betterment Videos   ▶ ")
                    # for linkss in random_resume_links:
                    #     st.markdown(f"[{linkss}]({linkss})")
                        
                    # st.subheader("Interview Videos Links   ▶")
                    # for links in random_interview_links:
                    #     st.markdown(f"[{links}]({links})")    
                    
                    # st.subheader("Resume Betterment Videos ▶")
                    # for linkss in random_resume_links:
                    #     st.markdown(f'<iframe width="560" height="315" src="https://www.youtube.com/watch?v={linkss}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
                    
                    # st.subheader("Interview Videos Links ▶")
                    # for links in random_interview_links:
                    #     st.markdown(f'<iframe width="560" height="315" src="https://www.youtube.com/watch?v={links}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
                    
                    
                        
                    
                # Resume Scorer & Resume Writing Tips
                st.subheader("\n\n")
                st.markdown('''<h4 style='text-align:center;padding:5px; margin-bottom:20px;font-family:Bungee;font-style:underline; margin-top:30px; font-size:50px; color: #080506; background-color:#a99a86;letter-spacing:5px'>Resume Modifications Techniques (Tips & Ideas)  📝''',unsafe_allow_html=True)
            
                resume_score = 0
                    
                    ### Predicting Whether these key points are added to the resume
                education_pattern = re.compile(r'\b(education|school|college)\b', flags=re.IGNORECASE)
                if education_pattern.search(resume_text):
                    resume_score = resume_score + 15
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Education Details</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Education. It will give Your Qualification level to the recruiter</h4>''',unsafe_allow_html=True)
                
                experience_pattern = re.compile(r'\bexperience\b', flags=re.IGNORECASE)
                if experience_pattern.search(resume_text):
                    resume_score = resume_score + 15
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Experience</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Experience. It will help you to stand out from crowd</h4>''',unsafe_allow_html=True)
                internship_pattern = re.compile(r'\b(internship|internships|intern)\b', flags=re.IGNORECASE)
                if internship_pattern.search(resume_text):
                    resume_score = resume_score + 9
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Internships</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Internships. It will help you to stand out from crowd</h4>''',unsafe_allow_html=True)
                skills_pattern = re.compile(r'\bskill(?:s)?\b', flags=re.IGNORECASE)
                if skills_pattern.search(resume_text) :
                    resume_score = resume_score + 6
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Skills</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Skills. It will help you a lot</h4>''',unsafe_allow_html=True)
                projects_pattern = re.compile(r'\bproject(?:s)?\b', flags=re.IGNORECASE)        
                if projects_pattern.search(resume_text):
                    resume_score = resume_score + 15
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Projects. It will show that you have done work related the required position or not.</h4>''',unsafe_allow_html=True)

                hobbies_pattern = re.compile(r'\bhobbies\b|\binterests\b|\bsoft\b|\bgoal\b', flags=re.IGNORECASE)
                if hobbies_pattern.search(resume_text):
                    resume_score = resume_score + 6
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies/Interests</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Hobbies/Intrests. It will show your personality to the Recruiters and give the assurance that you are fit for this role or not.</h4>''',unsafe_allow_html=True)
                    
                achievements_pattern = re.compile(r'\bachievements\b|\bachievement\b|\bawards\b', flags=re.IGNORECASE)
                if achievements_pattern.search(resume_text) :
                    resume_score = resume_score + 9
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements </h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Achievements. It will show that you are capable for the required position.</h4>''',unsafe_allow_html=True)
                certifications_pattern = re.compile(r'\bcertifications\b|\bcertification\b|\bcertificates\b', flags=re.IGNORECASE)
                if certifications_pattern.search(resume_text) :
                    resume_score = resume_score + 9
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Certifications </h4>''',unsafe_allow_html=True)
    
                else:
                    st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Certifications. It will show that you have done some specialization for the required position.</h4>''',unsafe_allow_html=True)

                languages_pattern = re.compile(r'\blanguages\b|\blanguage\b', flags=re.IGNORECASE)    
                if languages_pattern.search(resume_text):
                    resume_score = resume_score + 6
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Languages </h4>''',unsafe_allow_html=True)
    
                else:
                    st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please Menation Languages you know. It will show that you have diffrent communication skills.</h4>''',unsafe_allow_html=True)
                summary_objective_pattern = re.compile(r'\bSUMMARY\b|\bSummary\b|\bOBJECTIVES\b|\bObjectives\b|\bObjective\b', flags=re.IGNORECASE)
                if summary_objective_pattern.search(resume_text):
                    resume_score = resume_score + 3
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Summary/Objective</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Summary/Objective. It will show your single word presentation to the comapny.</h4>''',unsafe_allow_html=True)
                leadership_volunteer_pattern = re.compile(r'\bLEADERSHIP\b|\bLeadership\b|\bVOLUNTEER\b|\bVolunteer\b|\bVolunteers\b', flags=re.IGNORECASE)
                if leadership_volunteer_pattern.search(resume_text):
                    resume_score = resume_score + 6
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Summary/Objective</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Leadership/Volunteer. It will show your Leadership & Managnement skiils to the comapny.</h4>''',unsafe_allow_html=True)
            
                
                st.markdown('''<h4 style='text-align:center;margin-bottom:20px;font-family:Bungee;font-style:underline; margin-top:30px; font-size:50px; color: #080506; background-color:#a99a86;letter-spacing:5px'>  Resume Score Evaluation 📝''',unsafe_allow_html=True)

                
                
                    
                st.markdown(
                        """
                        <style>
                            .stProgress > div > div > div > div {
                                background-color: #d73b5c;
                            }
                        </style>""",
                        unsafe_allow_html=True,
                    )

                    ### Score Bar
                my_bar = st.progress(0)
                score = 0
                for percent_complete in range(resume_score):
                    score +=1
                    time.sleep(0.03)
                    my_bar.progress(percent_complete + 1)

        
                st.success('** Your Resume Writing Score: ' + str(score)+'**')
                #st.warning("** Note: This score is calculated based on the content that you have added in your Resume. **")
                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = str(cur_date+'_'+cur_time)
                
                insert_data(resume_data['name'],resume_data['email'],resume_data['mobile_number'],str(resume_score),
                            str(cand_level),clf,str(resume_data['skills']),timestamp)
                
                resume_tips = {
                "Education": "[+] Awesome! You have added Education Details" if education_pattern.search(resume_text) else "[-] Please add Education. It will give Your Qualification level to the recruiter",
                "Experience": "[+] Awesome! You have added Experience" if experience_pattern.search(resume_text) else "[-] Please add Experience. It will help you to stand out from the crowd",
                "Internships": "[+] Awesome! You have added Internships" if internship_pattern.search(resume_text) else "[-] Please add Internships. It will help you to stand out from the crowd",
                "Skills": "[+] Awesome! You have added Skills" if skills_pattern.search(resume_text) else "[-] Please add Skills. It will help you a lot",
                "Projects": "[+] Awesome! You have added your Projects" if projects_pattern.search(resume_text) else "[-] Please add Projects. It will show that you have done work related to the required position or not.",
                "Hobbies/Interests": "[+] Awesome! You have added your Hobbies/Interests" if hobbies_pattern.search(resume_text) else "[-] Please add Hobbies/Interests. It will show your personality to the Recruiters and give the assurance that you are fit for this role or not.",
                "Achievements": "[+] Awesome! You have added your Achievements" if achievements_pattern.search(resume_text) else "[-] Please add Achievements. It will show that you are capable of the required position.",
                "Certifications": "[+] Awesome! You have added your Certifications" if certifications_pattern.search(resume_text) else "[-] Please add Certifications. It will show that you have done some specialization for the required position.",
                "Languages": "[+] Awesome! You have added your Languages" if languages_pattern.search(resume_text) else "[-] Please mention Languages you know. It will show that you have different communication skills.",
                "Summary/Objective": "[+] Awesome! You have added your Summary/Objective" if summary_objective_pattern.search(resume_text) else "[-] Please add Summary/Objective. It will show your single-word presentation to the company.",
                "Leadership/Volunteer": "[+] Awesome! You have added Leadership/Volunteer" if leadership_volunteer_pattern.search(resume_text) else "[-] Please add Leadership/Volunteer. It will show your Leadership & Management skills to the company.",
            }


                
                if st.button("Download Resume Report"):
                    pdf_report = generate_pdf_report(
                        resume_data,
                        resume_score,
                        cand_level,
                        clf,
                        resume_data['skills'],
                        recommended_skills,
                        rec_course,
                        resume_tips
                    )
                    b64 = base64.b64encode(pdf_report.read()).decode()
                    href = f'<a href="data:application/pdf;base64,{b64}" download="Resume_Report.pdf">Download Resume Report</a>'
                    st.markdown(href, unsafe_allow_html=True)
            
                
                st.text("\n\n\n")
                store_resumedata_in_mongodb(resume_data['name'],resume_data['email'],resume_data['mobile_number'] ,clf ,resume_score,resume_data['total_experience'],timestamp, 'mongodb://localhost:27017') 
            # st.balloons()
                st.snow()

    elif file_type == "DOCX":
        docx_file = st.file_uploader("Choose your Resume (DOCX)", type=['docx'])
    
        if docx_file is not None:
                # Display the selected resume as an iframe
                file_bytes = base64.b64encode(docx_file.read()).decode()
                iframe_code = f'<br><iframe src="data:application/docx;base64,{file_bytes}" width="680" height="950"></iframe>'
                st.markdown(iframe_code, unsafe_allow_html=True)

    

                with st.spinner('Hang On While We Cook Magic For You...'):
                    time.sleep(3)
        
                # Rest of your code for resume analysis
                resume_text = convert_docx_to_txt(docx_file)
                resume_data = ResumeParser(docx_file).get_extracted_data()
                try:
                    st.header("\n\n")
                #    st.title("\n\n** -------  Resume Analysis  -------✉️**\n")
                    st.markdown('''<h4 style='padding:10px;text-align:center;margin-bottom:20px;font-family:Fantasy;font-style:underline; margin-top:30px; font-size:50px; color: #771414; background-color:#d5d3d3;letter-spacing:5px'>-------  Resume Analysis ✉️  ------- ''',unsafe_allow_html=True)

                    st.text("\n")
                    st.success("\nDear "+" "+resume_data['name']+" !! Welcome to WSH Resume Analyzer 🙂"+"\n")
                    # st.header("**Your Basic info 📋**")
                    
                    # st.text('Name: '+resume_data['name'])
                    # st.text('Email: ' + resume_data['email'])
                    # st.text('Contact: ' + resume_data['mobile_number'])
                    # st.text('Skills: '+resume_data['skills'])
                    
                    st.header("**Your Basic info 📋**")

                    # Assuming resume_data is a dictionary with keys 'name', 'email', 'mobile_number', 'total_experience'
                    table_data = {
                        'Attributes': ['Name', 'Email', 'Contact', 'Experience'],
                        'Details': [resume_data['name'], resume_data['email'], resume_data['mobile_number'], resume_data['total_experience']]
                    }
                    
                    # Create a Markdown table
                    markdown_table = "| Attributes | Details |\n| --- | --- |\n"
                    for attribute, detail in zip(table_data['Attributes'], table_data['Details']):
                        markdown_table += f"| {attribute} | {detail} |\n"
                    
                    # Display the Markdown table using st.write
                    st.write(markdown_table, unsafe_allow_html=True)
                            #     print(resume_data['skills'])
            
                #   st.text('Skills: '+resume_data['skills'])
                except:
                    pass
                    
                try:
                    st.text('Degree: ' + resume_data['degree'])
                except:
                    pass
                    
                try:
                    st.text('College_Name: ' + resume_data['college_name'])
                except:
                    pass
                    
                try:
                
                #  st.table(table_data, columns=column_names)
                #  st.text('Year of Experience: ' + str(resume_data['total_experience']))
                # st.text("Designition" + str(resume_data["designition"]))
                
                    st.success(f"\n\nDesignition: {resume_data['designition']}")
                # st.markdown(f"Designition: {resume_data['designition']}")

                except:
                    pass
                        
                    
                    ## Predicting Candidate Experience Level 
                    
                cand_level = ''
                if resume_data and resume_data.get('no_of_pages', 0) is not None and resume_data['no_of_pages'] < 1:                
                    cand_level = "NA"
                    st.markdown( '''<h4 style='text-align:center; margin-top:20px; color: #080506; background-color:#e1dddf;letter-spacing:3px'>You are at Fresher level!</h4>''',unsafe_allow_html=True)
                    
                    #### if internship then intermediate level
                        
                elif internship_pattern.search(resume_text):
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align:center; margin-top:20px; color: #080506; background-color:#e1dddf;letter-spacing:3px'>You are at intermediate level!</h4>''', unsafe_allow_html=True)

                # Check for work experience using regular expression
                
                elif experience_pattern.search(resume_text):
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align:center; margin-top:20px; color: #080506; background-color:#e1dddf;letter-spacing:3px'>You are at experience level!</h4>''', unsafe_allow_html=True)
                
                else:
                    cand_level = "Fresher"
                    st.markdown('''<h4 style='text-align:center; margin-top:20px; color: #080506; background-color:#e1dddf;letter-spacing:3px'>You are at Fresher level!!''',unsafe_allow_html=True)
                    
            
                    ## Skills Analyzing and Recommendation
            
                st.markdown('''<h4 style='text-align:center;margin-bottom:20px;font-family:Bungee;font-style:underline; margin-top:30px; font-size:50px; color: #080506; background-color:#a99a86;letter-spacing:5px'>Skills Evaluation ''',unsafe_allow_html=True)     
            

                keywords = st_tags(label='### Your Current Skills',
                text='See our skills recommendation below',value=resume_data['skills'],key='1')
                                            ###### Job Role Predication ######

                # Load the job role and skills dataset
        #     df = pd.read_csv('data.csv')

                # Create a CountVectorizer object to convert job skills to a matrix of token counts
            #    vectorizer = CountVectorizer(stop_words='english')

                # Fit the vectorizer on the job skills data
        #     X = vectorizer.fit_transform(df['skills'])

                # Train the Naive Bayes model
            #   clf = MultinomialNB().fit(X, df['job_role'])
                
                
                
                
                
                with open('data.json', 'r') as file:
                    data = json.load(file)

                # Flatten the data into a list of strings for each job title
                job_titles = list(data.keys())
                job_skills = [' '.join(data[title]) for title in job_titles]
                
                
                vectorizer = CountVectorizer()
                job_skills_matrix = vectorizer.fit_transform(job_skills)
                
                def predict_job_title(input_skills):
                    # Transform the input skills using the same vectorizer
                    input_skills_matrix = vectorizer.transform([' '.join(input_skills)])
                
                    # Calculate cosine similarity 
                    similarity = cosine_similarity(input_skills_matrix, job_skills_matrix)
                
                    # Get the index of the job title with the highest similarity
                    predicted_index = similarity.argmax()
                
                    return job_titles[predicted_index]
                
                def get_missing_skills(predicted_job_title, input_skills):
                    # Get the skills associated with the predicted job title
                    predicted_job_skills = data[predicted_job_title]
                
                    # Find the skills that are present in predicted_job_skills but not in input_skills
                    missing_skills = list(set(predicted_job_skills) - set(input_skills))
                
                    return missing_skills
                
            
                my_Skills = resume_data['skills']
                
                print(my_Skills)
                
                clf= predict_job_title(my_Skills)
                
                print(f"The predicted job title based on input skills is: {clf}")
                
                remaining_skills = get_missing_skills(clf,resume_data['skills'])
                
                print(f"Remaining skills for {clf}: {remaining_skills}")
            
        
                st.success("** Our analysis says you are looking for Jobs in {} **".format(clf))
                
                
                recommended_skills = remaining_skills
            

                # Display recommended skills 
                recommended_keywords = st_tags(label='### Recommended skills for you.',
                                text='Recommended skills generated from System',
                                value=recommended_skills,
                                key='2')
                
                if clf=="Web Developer":
                    rec_course = course_recommender(web_developer_courses)
                    
                elif clf == "Software Developer":
                    rec_course = course_recommender(software_developer_courses)
                
                    pass
                elif clf == "Mobile App Developer":
                    rec_course = course_recommender(mobile_app_developer_courses)
                    pass
                elif clf == "Data Analyst":
                    rec_course = course_recommender(data_analyst_courses)
                    pass
                elif clf == "Systems Analyst":
                    rec_course = course_recommender(systems_analyst_courses)
                    pass
                elif clf == "Quality Assurance Engineer":
                    rec_course = course_recommender(qa_engineer_courses)
                    pass
                elif clf == "DevOps Engineer":
                    rec_course = course_recommender(devops_engineer_courses)
                    pass
                elif clf == "Network Administrator":
                    rec_course = course_recommender(network_administrator_courses)
                    pass
                elif clf == "Cybersecurity Analyst":
                    rec_course = course_recommender(cyber_security_analyst_courses)
                    pass
                elif clf == "Game Developer":
                    rec_course = course_recommender(game_developer_courses)
                    pass
                elif clf == "UIUX Designer":
                    rec_course = course_recommender(uiux_designer_courses)
                    pass
                elif clf == "Database Administrator":
                    rec_course = course_recommender(database_administrator_courses)
                    pass
                elif clf == "Cloud Solutions Architect":
                    rec_course = course_recommender(cloud_solutions_architect_courses)
                    pass
                elif clf == "Machine Learning Engineer":
                    rec_course = course_recommender(machine_learning_engineer_courses)
                    pass
                elif clf == "Full Stack Developer":
                    rec_course = course_recommender(full_stack_developer_courses)
                    pass
                elif clf == "MERN Stack Developer":
                    rec_course = course_recommender(mern_stack_developer_courses)
                    pass
                elif clf == "MEAN Stack Developer":
                    rec_course = course_recommender(mean_stack_developer_courses)
                    pass  
                
                elif clf == "Graphic Designer":
                    rec_course = course_recommender(graphic_designer_courses)
                    pass  
                
                elif clf == "Content Creator":
                    rec_course = course_recommender(content_creator_courses)
                    pass    
                
                elif clf == "Media Planner":
                    rec_course = course_recommender(media_planner_courses)
                    pass    
            
                elif clf == "Digital Marketing Specialist":
                    rec_course = course_recommender(digital_marketing_specialist_courses)
                    pass 
                
                elif clf == "Video Producer":
                    rec_course = course_recommender(video_producer_courses)
                    pass   
                
                
                elif clf == "Public Relations Officer":
                    rec_course = course_recommender(public_relations_officer_courses)
                    pass     
                
                elif clf == "Social Media Manager":
                    rec_course = course_recommender(social_media_manager_courses)
                    pass    
                
                elif clf == "Journalist":
                    rec_course = course_recommender(journalist_courses)
                    pass    
                
                elif clf == "Broadcast Producer":
                    rec_course = course_recommender(broadcast_producer_courses)
                    pass    
                
                elif clf == "Event Coordinator":
                    rec_course = course_recommender(event_coordinator_courses)
                    pass   
                    
                elif clf == "Photographer":
                    rec_course = course_recommender(photographer_courses)
                    pass
                
                elif clf == "Media Research Analyst":
                    rec_course = course_recommender(media_research_analyst_courses)
                    pass       
                
                
                elif clf == "Audio Engineer":
                    rec_course = course_recommender(audio_engineer_courses)
                    pass   
                
                elif clf == "Media Educator":
                    rec_course = course_recommender(media_educator_courses)
                    pass   
                
                elif clf == "Virtual Events Specialist":
                    rec_course = course_recommender(virtual_events_specialist_courses)
                    pass   
            
                
                elif clf == "Business Analyst":
                    rec_course = course_recommender(business_analyst_courses)
                
                    pass
                
                elif clf == "Financial Analyst":
                    rec_course = course_recommender(financial_analyst_courses)
                
                    pass
                elif clf == "Marketing Manager":
                    rec_course = course_recommender(marketing_manager_courses)
                    pass
                elif clf == "Human Resources Specialist":
                    rec_course = course_recommender(human_resources_specialist_courses)
                
                    pass
                elif clf == "Supply Chain Analyst":
                    rec_course = course_recommender(supply_chain_analyst_courses)
                    
                    
                    pass
                elif clf == "Operations Manager":
                    rec_course = course_recommender(operations_manager_courses)
                    
                    pass
                elif clf == "Management Consultant":
                    rec_course = course_recommender(management_consultant_courses)
                
                    pass
                elif clf == "Entrepreneur":
                    rec_course = course_recommender(entrepreneur_courses)
            
                    pass
                elif clf == "Sales Manager":
                    rec_course = course_recommender(sales_manager_courses)
                    
                    pass
                elif clf == "Retail Manager":
                    rec_course = course_recommender(retail_manager_courses)
            
                    pass
                elif clf == "Event Planner":
                    rec_course = course_recommender(event_planner_courses)
                
                    pass
                elif clf == "Public Relations Specialist":
                    rec_course = course_recommender(public_relations_specialist_courses)
                
                    pass
                elif clf == "Healthcare Administrator":
                    rec_course = course_recommender(healthcare_administrator_courses)
                    
                    pass
                elif clf == "International Business Specialist":
                    rec_course = course_recommender(international_business_specialist_courses)
                
                    pass
                elif clf == "E-commerce Manager":
                    rec_course = course_recommender(e_commerce_manager_courses)
                
                if clf == "General Practitioner":
                    rec_course = course_recommender(general_practitioner_courses)
                elif clf == "Surgeon":
                    rec_course = course_recommender(surgeon_courses)
                elif clf == "Cardiologist":
                    rec_course = course_recommender(cardiologist_courses)
                elif clf == "Pediatrician":
                    rec_course = course_recommender(pediatrician_courses)
                elif clf == "Orthopedic Surgeon":
                    rec_course = course_recommender(orthopedic_surgeon_courses)
                elif clf == "Neurologist":
                    rec_course = course_recommender(neurologist_courses)
                elif clf == "Psychiatrist":
                    rec_course = course_recommender(psychiatrist_courses)
                elif clf == "Ophthalmologist":
                    rec_course = course_recommender(ophthalmologist_courses)
                elif clf == "Gynecologist":
                    rec_course = course_recommender(gynecologist_courses)
                elif clf == "Dermatologist":
                    rec_course = course_recommender(dermatologist_courses)
                elif clf == "Anesthesiologist":
                    rec_course = course_recommender(anesthesiologist_courses)
                elif clf == "Radiologist":
                    rec_course = course_recommender(radiologist_courses)
                elif clf == "Emergency Medicine Physician":
                    rec_course = course_recommender(emergency_medicine_physician_courses)
                elif clf == "Pathologist":
                    rec_course = course_recommender(pathologist_courses)
                elif clf == "Medical Researcher":
                    rec_course = course_recommender(medical_researcher_courses)
                else:
                    
                    print("Nor Available")


                    # Randomly select 2 links from each array
                    random_resume_links = random.sample(resume_videos, 2)
                    random_interview_links = random.sample(interview_videos, 2)
                    
                    # st.text("\n\n")
                    # st.subheader("Resume Betterment Videos ▶")
                    # for video_id in random_resume_links:
                    #     video_url = f'{video_id}'
                    #     st.video(video_url, width=500, height=400)
                    
                    # st.text("\n\n")
                    # st.subheader("Interview Videos ▶")
                    # for video_id in random_resume_links:
                    #     video_url = f'{video_id}'
                    #     st.video(video_url, width=500, height=400)
                        

                    st.markdown('''<h4 style='text-align:center;margin-bottom:20px;font-family:Bungee;font-style:underline; margin-top:30px; font-size:50px; color: #080506; background-color:#a99a86;letter-spacing:5px'>Resume Betterment Videos Links ▶''',unsafe_allow_html=True)
                    
                    for link in random_resume_links:
                        st.markdown(f'<br><iframe width="560" height="315" src="{link}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
                    
                    
                
                    st.markdown('''<h4 style='text-align:center;margin-bottom:20px;font-family:Bungee;font-style:underline; margin-top:30px; font-size:50px; color: #080506; background-color:#a99a86;letter-spacing:5px'>Interview Perperation Videos Links  ▶''',unsafe_allow_html=True)
                    for link in random_interview_links:
                        st.markdown(f'<iframe width="560" height="315" src="{link}" frameborder="0" allowfullscreen style="margin-top:20px"></iframe>', unsafe_allow_html=True)
                    
                    # st.subheader("Resume Betterment Videos   ▶ ")
                    # for linkss in random_resume_links:
                    #     st.markdown(f"[{linkss}]({linkss})")
                        
                    # st.subheader("Interview Videos Links   ▶")
                    # for links in random_interview_links:
                    #     st.markdown(f"[{links}]({links})")    
                    
                    # st.subheader("Resume Betterment Videos ▶")
                    # for linkss in random_resume_links:
                    #     st.markdown(f'<iframe width="560" height="315" src="https://www.youtube.com/watch?v={linkss}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
                    
                    # st.subheader("Interview Videos Links ▶")
                    # for links in random_interview_links:
                    #     st.markdown(f'<iframe width="560" height="315" src="https://www.youtube.com/watch?v={links}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
                    
                    
                        
                    
                # Resume Scorer & Resume Writing Tips
                st.subheader("\n\n")
                st.markdown('''<h4 style='text-align:center;padding:5px; margin-bottom:20px;font-family:Bungee;font-style:underline; margin-top:30px; font-size:50px; color: #080506; background-color:#a99a86;letter-spacing:5px'>Resume Modifications Techniques (Tips & Ideas)  📝''',unsafe_allow_html=True)
            
                resume_score = 0
                    
                    ### Predicting Whether these key points are added to the resume
                education_pattern = re.compile(r'\b(education|school|college)\b', flags=re.IGNORECASE)
                if education_pattern.search(resume_text):
                    resume_score = resume_score + 15
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Education Details</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Education. It will give Your Qualification level to the recruiter</h4>''',unsafe_allow_html=True)
                
                experience_pattern = re.compile(r'\bexperience\b', flags=re.IGNORECASE)
                if experience_pattern.search(resume_text):
                    resume_score = resume_score + 15
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Experience</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Experience. It will help you to stand out from crowd</h4>''',unsafe_allow_html=True)
                internship_pattern = re.compile(r'\b(internship|internships|intern)\b', flags=re.IGNORECASE)
                if internship_pattern.search(resume_text):
                    resume_score = resume_score + 9
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Internships</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Internships. It will help you to stand out from crowd</h4>''',unsafe_allow_html=True)
                skills_pattern = re.compile(r'\bskill(?:s)?\b', flags=re.IGNORECASE)
                if skills_pattern.search(resume_text) :
                    resume_score = resume_score + 6
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Skills</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Skills. It will help you a lot</h4>''',unsafe_allow_html=True)
                projects_pattern = re.compile(r'\bproject(?:s)?\b', flags=re.IGNORECASE)        
                if projects_pattern.search(resume_text):
                    resume_score = resume_score + 15
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Projects. It will show that you have done work related the required position or not.</h4>''',unsafe_allow_html=True)

                hobbies_pattern = re.compile(r'\bhobbies\b|\binterests\b|\bsoft\b|\bgoal\b', flags=re.IGNORECASE)
                if hobbies_pattern.search(resume_text):
                    resume_score = resume_score + 6
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies/Interests</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Hobbies/Intrests. It will show your personality to the Recruiters and give the assurance that you are fit for this role or not.</h4>''',unsafe_allow_html=True)
                    
                achievements_pattern = re.compile(r'\bachievements\b|\bachievement\b|\bawards\b', flags=re.IGNORECASE)
                if achievements_pattern.search(resume_text) :
                    resume_score = resume_score + 9
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements </h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Achievements. It will show that you are capable for the required position.</h4>''',unsafe_allow_html=True)
                certifications_pattern = re.compile(r'\bcertifications\b|\bcertification\b|\bcertificates\b', flags=re.IGNORECASE)
                if certifications_pattern.search(resume_text) :
                    resume_score = resume_score + 9
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Certifications </h4>''',unsafe_allow_html=True)
    
                else:
                    st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Certifications. It will show that you have done some specialization for the required position.</h4>''',unsafe_allow_html=True)

                languages_pattern = re.compile(r'\blanguages\b|\blanguage\b', flags=re.IGNORECASE)    
                if languages_pattern.search(resume_text):
                    resume_score = resume_score + 6
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Languages </h4>''',unsafe_allow_html=True)
    
                else:
                    st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please Menation Languages you know. It will show that you have diffrent communication skills.</h4>''',unsafe_allow_html=True)
                summary_objective_pattern = re.compile(r'\bSUMMARY\b|\bSummary\b|\bOBJECTIVES\b|\bObjectives\b|\bObjective\b', flags=re.IGNORECASE)
                if summary_objective_pattern.search(resume_text):
                    resume_score = resume_score + 3
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Summary/Objective</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Summary/Objective. It will show your single word presentation to the comapny.</h4>''',unsafe_allow_html=True)
                leadership_volunteer_pattern = re.compile(r'\bLEADERSHIP\b|\bLeadership\b|\bVOLUNTEER\b|\bVolunteer\b|\bVolunteers\b', flags=re.IGNORECASE)
                if leadership_volunteer_pattern.search(resume_text):
                    resume_score = resume_score + 6
                    st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Summary/Objective</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Leadership/Volunteer. It will show your Leadership & Managnement skiils to the comapny.</h4>''',unsafe_allow_html=True)
            
                
                st.markdown('''<h4 style='text-align:center;margin-bottom:20px;font-family:Bungee;font-style:underline; margin-top:30px; font-size:50px; color: #080506; background-color:#a99a86;letter-spacing:5px'>  Resume Score Evaluation 📝''',unsafe_allow_html=True)

                
                
                    
                st.markdown(
                        """
                        <style>
                            .stProgress > div > div > div > div {
                                background-color: #d73b5c;
                            }
                        </style>""",
                        unsafe_allow_html=True,
                    )

                    ### Score Bar
                my_bar = st.progress(0)
                score = 0
                for percent_complete in range(resume_score):
                    score +=1
                    time.sleep(0.03)
                    my_bar.progress(percent_complete + 1)

        
                st.success('** Your Resume Writing Score: ' + str(score)+'**')
                #st.warning("** Note: This score is calculated based on the content that you have added in your Resume. **")
                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = str(cur_date+'_'+cur_time)
                
                insert_data(resume_data['name'],resume_data['email'],resume_data['mobile_number'],str(resume_score),
                            str(cand_level),clf,str(resume_data['skills']),timestamp)
                
                resume_tips = {
                "Education": "[+] Awesome! You have added Education Details" if education_pattern.search(resume_text) else "[-] Please add Education. It will give Your Qualification level to the recruiter",
                "Experience": "[+] Awesome! You have added Experience" if experience_pattern.search(resume_text) else "[-] Please add Experience. It will help you to stand out from the crowd",
                "Internships": "[+] Awesome! You have added Internships" if internship_pattern.search(resume_text) else "[-] Please add Internships. It will help you to stand out from the crowd",
                "Skills": "[+] Awesome! You have added Skills" if skills_pattern.search(resume_text) else "[-] Please add Skills. It will help you a lot",
                "Projects": "[+] Awesome! You have added your Projects" if projects_pattern.search(resume_text) else "[-] Please add Projects. It will show that you have done work related to the required position or not.",
                "Hobbies/Interests": "[+] Awesome! You have added your Hobbies/Interests" if hobbies_pattern.search(resume_text) else "[-] Please add Hobbies/Interests. It will show your personality to the Recruiters and give the assurance that you are fit for this role or not.",
                "Achievements": "[+] Awesome! You have added your Achievements" if achievements_pattern.search(resume_text) else "[-] Please add Achievements. It will show that you are capable of the required position.",
                "Certifications": "[+] Awesome! You have added your Certifications" if certifications_pattern.search(resume_text) else "[-] Please add Certifications. It will show that you have done some specialization for the required position.",
                "Languages": "[+] Awesome! You have added your Languages" if languages_pattern.search(resume_text) else "[-] Please mention Languages you know. It will show that you have different communication skills.",
                "Summary/Objective": "[+] Awesome! You have added your Summary/Objective" if summary_objective_pattern.search(resume_text) else "[-] Please add Summary/Objective. It will show your single-word presentation to the company.",
                "Leadership/Volunteer": "[+] Awesome! You have added Leadership/Volunteer" if leadership_volunteer_pattern.search(resume_text) else "[-] Please add Leadership/Volunteer. It will show your Leadership & Management skills to the company.",
            }


                
                if st.button("Download Resume Report"):
                    pdf_report = generate_pdf_report(
                        resume_data,
                        resume_score,
                        cand_level,
                        clf,
                        resume_data['skills'],
                        recommended_skills,
                        rec_course,
                        resume_tips
                    )
                    b64 = base64.b64encode(pdf_report.read()).decode()
                    href = f'<a href="data:application/pdf;base64,{b64}" download="Resume_Report.pdf">Download Resume Report</a>'
                    st.markdown(href, unsafe_allow_html=True)
            
                
                st.text("\n\n\n")
                store_resumedata_in_mongodb(resume_data['name'],resume_data['email'],resume_data['mobile_number'] ,clf ,resume_score,resume_data['total_experience'],timestamp, 'mongodb://localhost:27017') 
            # st.balloons()
                st.snow()
            
            


