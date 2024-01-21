# import re
# import json
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# ###### Import Libraries ######
# import nltk
# nltk.download('stopwords')
# import streamlit as st
# import pandas as pd
# import base64,io,random 
# import time,datetime
# from streamlit_tags import st_tags

# ###### Libraries for pdf tools ######

# from pyresparser import ResumeParser
# from pdfminer3.layout import LAParams
# from pdfminer3.pdfpage import PDFPage
# from pdfminer3.pdfinterp import PDFResourceManager
# from pdfminer3.pdfinterp import PDFPageInterpreter
# from pdfminer3.converter import TextConverter

# ###### Import Courses and  Database File ######

# from Courses import*
# from database import CreateTable,insert_data


# ###### Machine Learning Algortihm ######

# from sklearn.naive_bayes import MultinomialNB
# from sklearn.feature_extraction.text import CountVectorizer


# def convert_pdf_to_txt(pdf_file):
#     resource_manager = PDFResourceManager()
#     fake_file_handle = io.StringIO()
#     converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
#     page_interpreter = PDFPageInterpreter(resource_manager, converter)
#     for page in PDFPage.get_pages(pdf_file):
#         page_interpreter.process_page(page)
#     text = fake_file_handle.getvalue()
#     converter.close()
#     fake_file_handle.close()
#     return text

# def course_recommender(course_list):
#     st.subheader("**Courses & Certificates Recommendations 👨‍🎓**")
#     c = 0
#     rec_course = []
#     ## slider to choose from range 1-10
#     no_of_reco =5
#     random.shuffle(course_list)
#     for c_name, c_link in course_list:
#         c += 1
#         st.markdown(f"({c}) [{c_name}]({c_link})")
#         rec_course.append(c_name)
#         if c == no_of_reco:
#             break
#     return rec_course


# def NormalUser():
#     internship_pattern = re.compile(r'\binternship(s)?\b', flags=re.IGNORECASE)
#     experience_pattern = re.compile(r'\bexperience\b', flags=re.IGNORECASE)
#     pdf_file = st.file_uploader("Choose your Resume", type=['pdf'])
#     if pdf_file is not None:
#         with st.spinner('Hang On While We Cook Magic For You...'):
#             time.sleep(3)
#         file_bytes = base64.b64encode(pdf_file.read()).decode()
#         #st.write(f'<iframe src="data:application/pdf;base64,{file_bytes}" width="600" height="900"></iframe>', unsafe_allow_html=True)
#         resume_text = convert_pdf_to_txt(pdf_file)
#         resume_data = ResumeParser(pdf_file).get_extracted_data()
#         if resume_data:
#             st.header("**Resume Analysis 🤘**")
#             st.success("Hello "+ resume_data['name'])
#             st.subheader("**Your Basic info 👀**")
        
#             try:
#                 st.text('Name: '+resume_data['name'])
#                 st.text('Email: ' + resume_data['email'])
#                 st.text('Contact: ' + resume_data['mobile_number'])
#                 st.text('Skills: '+resume_data['skills'])
#            #     print(resume_data['skills'])
#             except:
#                 pass
                
#             try:
#                 st.text('Degree: ' + resume_data['degree'])
#             except:
#                 pass
                
#             try:
#                 st.text('College_Name: ' + resume_data['college_name'])
#             except:
#                 pass
                
#             try:
#                 st.text('Year of Experience: ' + str(resume_data['total_experience']))
#                 st.text("Designition" + str(resume_data["designition"]))
#             except:
#                 pass
                    
                  
#                 ## Predicting Candidate Experience Level 
                
#             cand_level = ''
#             if resume_data['no_of_pages'] < 1:                
#                 cand_level = "NA"
#                 st.markdown( '''<h4 style='text-align: left; color: #d73b5c;'>You are at Fresher level!</h4>''',unsafe_allow_html=True)
                
#                 #### if internship then intermediate level
                    
#             # Check for internship using regular expression
            
#             elif internship_pattern.search(resume_text):
#                 cand_level = "Intermediate"
#                 st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''', unsafe_allow_html=True)

#             # Check for work experience using regular expression
            
#             elif experience_pattern.search(resume_text):
#                 cand_level = "Experienced"
#                 st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!</h4>''', unsafe_allow_html=True)
            
#             else:
#                 cand_level = "Fresher"
#                 st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at Fresher level!!''',unsafe_allow_html=True)
                
         
#                  ## Skills Analyzing and Recommendation
#             st.subheader("**Skills Recommendation 💡**")

#             keywords = st_tags(label='### Your Current Skills',
#             text='See our skills recommendation below',value=resume_data['skills'],key='1')
#                                         ###### Job Role Predication ######

#                # Load the job role and skills dataset
#        #     df = pd.read_csv('data.csv')

#                # Create a CountVectorizer object to convert job skills to a matrix of token counts
#         #    vectorizer = CountVectorizer(stop_words='english')

#                # Fit the vectorizer on the job skills data
#        #     X = vectorizer.fit_transform(df['skills'])

#                # Train the Naive Bayes model
#          #   clf = MultinomialNB().fit(X, df['job_role'])
            
            
            
            
            
#             with open('data.json', 'r') as file:
#               data = json.load(file)

#             # Flatten the data into a list of strings for each job title
#             job_titles = list(data.keys())
#             job_skills = [' '.join(data[title]) for title in job_titles]
            
            
#             vectorizer = CountVectorizer()
#             job_skills_matrix = vectorizer.fit_transform(job_skills)
            
#             def predict_job_title(input_skills):
#                 # Transform the input skills using the same vectorizer
#                 input_skills_matrix = vectorizer.transform([' '.join(input_skills)])
            
#                 # Calculate cosine similarity 
#                 similarity = cosine_similarity(input_skills_matrix, job_skills_matrix)
            
#                 # Get the index of the job title with the highest similarity
#                 predicted_index = similarity.argmax()
            
#                 return job_titles[predicted_index]
            
#             def get_missing_skills(predicted_job_title, input_skills):
#                 # Get the skills associated with the predicted job title
#                 predicted_job_skills = data[predicted_job_title]
            
#                 # Find the skills that are present in predicted_job_skills but not in input_skills
#                 missing_skills = list(set(predicted_job_skills) - set(input_skills))
            
#                 return missing_skills
            
          
#             my_Skills = resume_data['skills']
            
#             print(my_Skills)
            
#             clf= predict_job_title(my_Skills)
            
#             print(f"The predicted job title based on input skills is: {clf}")
            
#             remaining_skills = get_missing_skills(clf,resume_data['skills'])
            
#             print(f"Remaining skills for {clf}: {remaining_skills}")
        
    
#             st.success("** Our analysis says you are looking for Jobs in {} **".format(clf))
            
            
#             recommended_skills = remaining_skills
           

#             # Display recommended skills 
#             recommended_keywords = st_tags(label='### Recommended skills for you.',
#                                text='Recommended skills generated from System',
#                                value=recommended_skills,
#                                key='2')
            
#             if clf=="Web Developer":
#                  rec_course = course_recommender(web_developer_courses)
                 
#             elif clf == "Software Developer":
#                 rec_course = course_recommender(software_developer_courses)
               
#                 pass
#             elif clf == "Mobile App Developer":
#                 rec_course = course_recommender(mobile_app_developer_courses)
#                 pass
#             elif clf == "Data Analyst":
#                 rec_course = course_recommender(data_analyst_courses)
#                 pass
#             elif clf == "Systems Analyst":
#                 rec_course = course_recommender(systems_analyst_courses)
#                 pass
#             elif clf == "Quality Assurance Engineer":
#                 rec_course = course_recommender(qa_engineer_courses)
#                 pass
#             elif clf == "DevOps Engineer":
#                 rec_course = course_recommender(devops_engineer_courses)
#                 pass
#             elif clf == "Network Administrator":
#                 rec_course = course_recommender(network_administrator_courses)
#                 pass
#             elif clf == "Cybersecurity Analyst":
#                 rec_course = course_recommender(cyber_security_analyst_courses)
#                 pass
#             elif clf == "Game Developer":
#                 rec_course = course_recommender(game_developer_courses)
#                 pass
#             elif clf == "UIUX Designer":
#                 rec_course = course_recommender(uiux_designer_courses)
#                 pass
#             elif clf == "Database Administrator":
#                 rec_course = course_recommender(database_administrator_courses)
#                 pass
#             elif clf == "Cloud Solutions Architect":
#                 rec_course = course_recommender(cloud_solutions_architect_courses)
#                 pass
#             elif clf == "Machine Learning Engineer":
#                 rec_course = course_recommender(machine_learning_engineer_courses)
#                 pass
#             elif clf == "Full Stack Developer":
#                 rec_course = course_recommender(full_stack_developer_courses)
#                 pass
#             elif clf == "MERN Stack Developer":
#                 rec_course = course_recommender(mern_stack_developer_courses)
#                 pass
#             elif clf == "MEAN Stack Developer":
#                 rec_course = course_recommender(mean_stack_developer_courses)
#                 pass  
            
#             elif clf == "Graphic Designer":
#                 rec_course = course_recommender(graphic_designer_courses)
#                 pass  
            
#             elif clf == "Content Creator":
#                 rec_course = course_recommender(content_creator_courses)
#                 pass    
            
#             elif clf == "Media Planner":
#                 rec_course = course_recommender(media_planner_courses)
#                 pass    
           
#             elif clf == "Digital Marketing Specialist":
#                 rec_course = course_recommender(digital_marketing_specialist_courses)
#                 pass 
            
#             elif clf == "Video Producer":
#                 rec_course = course_recommender(video_producer_courses)
#                 pass   
            
            
#             elif clf == "Public Relations Officer":
#                 rec_course = course_recommender(public_relations_officer_courses)
#                 pass     
            
#             elif clf == "Social Media Manager":
#                 rec_course = course_recommender(social_media_manager_courses)
#                 pass    
            
#             elif clf == "Journalist":
#                 rec_course = course_recommender(journalist_courses)
#                 pass    
            
#             elif clf == "Broadcast Producer":
#                 rec_course = course_recommender(broadcast_producer_courses)
#                 pass    
            
#             elif clf == "Event Coordinator":
#                 rec_course = course_recommender(event_coordinator_courses)
#                 pass   
                
#             elif clf == "Photographer":
#                 rec_course = course_recommender(photographer_courses)
#                 pass
            
#             elif clf == "Media Research Analyst":
#                 rec_course = course_recommender(media_research_analyst_courses)
#                 pass       
              
            
#             elif clf == "Audio Engineer":
#                 rec_course = course_recommender(audio_engineer_courses)
#                 pass   
            
#             elif clf == "Media Educator":
#                 rec_course = course_recommender(media_educator_courses)
#                 pass   
            
#             elif clf == "Virtual Events Specialist":
#                 rec_course = course_recommender(virtual_events_specialist_courses)
#                 pass   
           
            
#             elif clf == "Business Analyst":
#                 rec_course = course_recommender(business_analyst_courses)
              
#                 pass
            
#             elif clf == "Financial Analyst":
#                 rec_course = course_recommender(financial_analyst_courses)
               
#                 pass
#             elif clf == "Marketing Manager":
#                 rec_course = course_recommender(marketing_manager_courses)
#                 pass
#             elif clf == "Human Resources Specialist":
#                 rec_course = course_recommender(human_resources_specialist_courses)
               
#                 pass
#             elif clf == "Supply Chain Analyst":
#                 rec_course = course_recommender(supply_chain_analyst_courses)
                
                
#                 pass
#             elif clf == "Operations Manager":
#                 rec_course = course_recommender(operations_manager_courses)
                
#                 pass
#             elif clf == "Management Consultant":
#                 rec_course = course_recommender(management_consultant_courses)
               
#                 pass
#             elif clf == "Entrepreneur":
#                 rec_course = course_recommender(entrepreneur_courses)
          
#                 pass
#             elif clf == "Sales Manager":
#                 rec_course = course_recommender(sales_manager_courses)
                
#                 pass
#             elif clf == "Retail Manager":
#                 rec_course = course_recommender(retail_manager_courses)
           
#                 pass
#             elif clf == "Event Planner":
#                 rec_course = course_recommender(event_planner_courses)
               
#                 pass
#             elif clf == "Public Relations Specialist":
#                 rec_course = course_recommender(public_relations_specialist_courses)
              
#                 pass
#             elif clf == "Healthcare Administrator":
#                 rec_course = course_recommender(healthcare_administrator_courses)
                
#                 pass
#             elif clf == "International Business Specialist":
#                 rec_course = course_recommender(international_business_specialist_courses)
               
#                 pass
#             elif clf == "E-commerce Manager":
#                 rec_course = course_recommender(e_commerce_manager_courses)
               
#             if clf == "General Practitioner":
#                 rec_course = course_recommender(general_practitioner_courses)
#             elif clf == "Surgeon":
#                 rec_course = course_recommender(surgeon_courses)
#             elif clf == "Cardiologist":
#                 rec_course = course_recommender(cardiologist_courses)
#             elif clf == "Pediatrician":
#                 rec_course = course_recommender(pediatrician_courses)
#             elif clf == "Orthopedic Surgeon":
#                 rec_course = course_recommender(orthopedic_surgeon_courses)
#             elif clf == "Neurologist":
#                 rec_course = course_recommender(neurologist_courses)
#             elif clf == "Psychiatrist":
#                 rec_course = course_recommender(psychiatrist_courses)
#             elif clf == "Ophthalmologist":
#                 rec_course = course_recommender(ophthalmologist_courses)
#             elif clf == "Gynecologist":
#                 rec_course = course_recommender(gynecologist_courses)
#             elif clf == "Dermatologist":
#                 rec_course = course_recommender(dermatologist_courses)
#             elif clf == "Anesthesiologist":
#                 rec_course = course_recommender(anesthesiologist_courses)
#             elif clf == "Radiologist":
#                 rec_course = course_recommender(radiologist_courses)
#             elif clf == "Emergency Medicine Physician":
#                 rec_course = course_recommender(emergency_medicine_physician_courses)
#             elif clf == "Pathologist":
#                 rec_course = course_recommender(pathologist_courses)
#             elif clf == "Medical Researcher":
#                 rec_course = course_recommender(medical_researcher_courses)
#             else:
                
#                 print("Nor Available")








            
            
             

#             # Display recommended courses
#             # recommended_courses = st_tags(label='### Courses for you.',
#             #                   text='Recommended Courses generated from System',
#             #                   value=rec_course,  # Assuming rec_course is the correct variable here
#             #                   key='3')
            
#             # recommended_skills =remaining_skills
#             # recommended_keywords = st_tags(label='### Recommended skills for you.',
#             # text='Recommended skills generated from System',value=recommended_skills,key = '2') 
#             # rec_course = course_recommender(web_course)
#             # recommended_courses = st_tags(label='### Courses for you.',
#             # text='Recommended Courses generated from System',value=recommended_courses,key = '3')
            
            


#          #   reco_field=clf(vectorizer.transform(resume_data['skills']))[0]

#             # if reco_field=="Web Development":
#             #     recommended_skills =web_keyword
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '2')  
#             #     rec_course = course_recommender(web_course)
                
                
#             # elif reco_field=="Software Development":
#             #     recommended_skills = soft_keyword
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '3')
#             #     rec_course = course_recommender(soft_course)
                
#             # elif clf=="Java Developer":
#             #     recommended_skills =java_keyword
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '4')
#             #     rec_course = course_recommender(java_course)

#             # elif clf=="Python Developer":
#             #     recommended_skills =py_keyword
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '5')
#             #     rec_course = course_recommender(py_course)
                
#             # elif clf=="C ++ Developer":
#             #     recommended_skills =cpp_keyword
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '6')
#             #     rec_course = course_recommender(cpp_course)

#             # elif clf=="Data Science":
#             #     recommended_skills =ds_keyword
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '7')
#             #     rec_course = course_recommender(ds_course)
                
#             # elif clf=="Embedded  System":
#             #     recommended_skills =embd_keyword
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '8')
#             #     rec_course = course_recommender(embd_course)
                
#             # elif clf=="DotNet Developer":
#             #     recommended_skills =dnet_keyword
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '9')
#             #     rec_course = course_recommender(dnet_course)

#             # elif clf=="Software Testing":
#             #     recommended_skills =test_keyword
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '10')
#             #     rec_course = course_recommender(test_course)
                
                
#             # elif clf=="Administrative Assistant":
#             #     recommended_skills =administrative_assistant_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '11')
#             #     rec_course = course_recommender(Administrative_Assistant_course)   
                
             
#             # elif clf=="Financial Analyst":
#             #     recommended_skills =financial_analyst_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '12')
#             #     rec_course = course_recommender(Financial_Analyst_course) 
                   
#             # elif clf=="Human Resources Specialist":
#             #     recommended_skills =human_resources_specialist_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '13')
#             #     rec_course = course_recommender(Human_Resources_Specialist_course) 
                
#             # elif clf=="Marketing Coordinator":
#             #     recommended_skills =marketing_coordinator_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '14')
#             #     rec_course = course_recommender(Marketing_Coordinator_course) 
                
#             # elif clf=="Executive Assistant":
#             #     recommended_skills =executive_assistant_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '15')
#             #     rec_course = course_recommender(Executive_Assistant_course)     
                
#             # elif clf=="Business Development Manager":
#             #     recommended_skills =business_development_manager_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '16')
#             #     rec_course = course_recommender(Business_Development_Manager_course)  
             
#             # elif clf=="Office Manager":
#             #     recommended_skills =office_manager_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '17')
#             #     rec_course = course_recommender(Office_Manager_course)    
                
                
#             # elif clf=="Project Coordinator":
#             #     recommended_skills =project_coordinator_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '18')
#             #     rec_course = course_recommender(Project_Coordinator_course)    
                
                
#             # elif clf=="Customer Service Representative":
#             #     recommended_skills =customer_service_representative_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '19')
#             #     rec_course = course_recommender(Customer_Service_Representative_course)   
                
#             # elif clf=="Digital Marketing Specialist":
#             #     recommended_skills =digital_marketing_specialist_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '20')
#             #     rec_course = course_recommender(Digital_Marketing_Specialist_course)
                
                                          
#             # elif clf=="Content Marketing Manager":
#             #     recommended_skills =content_marketing_manager_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '21')
#             #     rec_course = course_recommender(Content_Marketing_Manager_course)     
            
#             # elif clf=="Social Media Coordinator":
#             #     recommended_skills =social_media_coordinator_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '22')
#             #     rec_course = course_recommender(Social_Media_Coordinator_course)   
                
#             # elif clf=="Brand Manager":
#             #     recommended_skills =brand_manager_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '23')
#             #     rec_course = course_recommender(Brand_Manager_course)  
            
            
#             # elif clf=="Email Marketing Specialist":
#             #     recommended_skills =email_marketing_specialist_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '24')
#             #     rec_course = course_recommender(Email_Marketing_Specialist_course)   
                
#             # elif clf=="Marketing Analytics Manager":
#             #     recommended_skills =marketing_analytics_manager_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '25')
#             #     rec_course = course_recommender(Marketing_Analytics_Manager_course)   
            
            
#             # elif clf=="Product Marketing Manager":
#             #     recommended_skills =product_marketing_manager_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '26')
#             #     rec_course = course_recommender(Product_Marketing_Manager_course)    
                
                
#             # elif clf=="SEO Specialist":
#             #     recommended_skills =seo_specialist_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '27')
#             #     rec_course = course_recommender(SEO_Specialist_course)    
                
                
#             # elif clf=="Event Marketing Coordinator":
#             #     recommended_skills =event_marketing_coordinator_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '28')
#             #     rec_course = course_recommender(Event_Marketing_Coordinator_course) 
                
            
#             # elif clf=="Mechanical Engineer":
#             #     recommended_skills =mechanical_engineer_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '29')
#             #     rec_course = course_recommender(mechanical_engineer_courses) 
                
            
#             # elif clf=="Industrial Engineer":
#             #     recommended_skills =industrial_engineer_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '30')
#             #     rec_course = course_recommender(industrial_engineer_courses)  
                
                
#             # elif clf=="Electrical Engineer":
#             #     recommended_skills =electrical_engineer_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '31')
#             #     rec_course = course_recommender(electrical_engineer_courses) 
                
                
                
#             # elif clf=="Process Control Engineer":
#             #     recommended_skills =process_control_engineer_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '32')
#             #     rec_course = course_recommender(process_control_engineer_courses) 
            
#             # elif clf=="Manufacturing Engineer":
#             #     recommended_skills =manufacturing_engineer_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '33')
#             #     rec_course = course_recommender(manufacturing_engineer_courses) 
                
                
#             # elif clf=="Reliability Engineer":
#             #     recommended_skills =reliability_engineer_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '34')
#             #     rec_course = course_recommender(reliability_engineer_courses)                                   
                
                
                
#             # elif clf=="Mobile App Developer":
#             #     recommended_skills =mobile_app_development_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '35')
#             #     rec_course = course_recommender(mobile_app_development_courses)       
                  
                
#             # elif clf=="Android App Developer":
#             #     recommended_skills =android_app_development_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '36')
#             #     rec_course = course_recommender(android_app_development_courses)  
                
                
#             # elif clf=="IOS- App Developer":
#             #     recommended_skills =ios_app_development_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '37')
#             #     rec_course = course_recommender(ios_app_development_courses)  
                
                
#             # elif clf=="Native App Developer":
#             #     recommended_skills =native_app_development_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '38')
#             #     rec_course = course_recommender(native_app_development_courses)  
                
                
#             # elif clf=="Cross Platform App Developer":
#             #     recommended_skills =cross_platform_app_development_keywords
#             #     recommended_keywords = st_tags(label='### Recommended skills for you.',
#             #     text='Recommended skills generated from System',value=recommended_skills,key = '39')
#             #     rec_course = course_recommender(Customer_Service_Representative_course)  
                
                
#             # Resume Scorer & Resume Writing Tips
#             st.subheader("**Resume Tips & Ideas 🥂**")
#             resume_score = 0
                
#                 ### Predicting Whether these key points are added to the resume
#             education_pattern = re.compile(r'\b(education|school|college)\b', flags=re.IGNORECASE)
#             if education_pattern.search(resume_text):
#                 resume_score = resume_score + 15
#                 st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Education Details</h4>''',unsafe_allow_html=True)
#             else:
#                 st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Education. It will give Your Qualification level to the recruiter</h4>''',unsafe_allow_html=True)
            
#             experience_pattern = re.compile(r'\bexperience\b', flags=re.IGNORECASE)
#             if experience_pattern.search(resume_text):
#                 resume_score = resume_score + 15
#                 st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Experience</h4>''',unsafe_allow_html=True)
#             else:
#                 st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Experience. It will help you to stand out from crowd</h4>''',unsafe_allow_html=True)
#             internship_pattern = re.compile(r'\b(internship|internships|intern)\b', flags=re.IGNORECASE)
#             if internship_pattern.search(resume_text):
#                 resume_score = resume_score + 9
#                 st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Internships</h4>''',unsafe_allow_html=True)
#             else:
#                 st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Internships. It will help you to stand out from crowd</h4>''',unsafe_allow_html=True)
#             skills_pattern = re.compile(r'\bskill(?:s)?\b', flags=re.IGNORECASE)
#             if skills_pattern.search(resume_text) :
#                 resume_score = resume_score + 6
#                 st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Skills</h4>''',unsafe_allow_html=True)
#             else:
#                 st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Skills. It will help you a lot</h4>''',unsafe_allow_html=True)
#             projects_pattern = re.compile(r'\bproject(?:s)?\b', flags=re.IGNORECASE)        
#             if projects_pattern.search(resume_text):
#                 resume_score = resume_score + 15
#                 st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Projects</h4>''',unsafe_allow_html=True)
#             else:
#                 st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Projects. It will show that you have done work related the required position or not.</h4>''',unsafe_allow_html=True)

#             hobbies_pattern = re.compile(r'\bhobbies\b|\binterests\b|\bsoft\b|\bgoal\b', flags=re.IGNORECASE)
#             if hobbies_pattern.search(resume_text):
#                 resume_score = resume_score + 6
#                 st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Hobbies/Interests</h4>''',unsafe_allow_html=True)
#             else:
#                 st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Hobbies/Intrests. It will show your personality to the Recruiters and give the assurance that you are fit for this role or not.</h4>''',unsafe_allow_html=True)
                
#             achievements_pattern = re.compile(r'\bachievements\b|\bachievement\b|\bawards\b', flags=re.IGNORECASE)
#             if achievements_pattern.search(resume_text) :
#                 resume_score = resume_score + 9
#                 st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Achievements </h4>''',unsafe_allow_html=True)
#             else:
#                 st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Achievements. It will show that you are capable for the required position.</h4>''',unsafe_allow_html=True)
#             certifications_pattern = re.compile(r'\bcertifications\b|\bcertification\b|\bcertificates\b', flags=re.IGNORECASE)
#             if certifications_pattern.search(resume_text) :
#                 resume_score = resume_score + 9
#                 st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Certifications </h4>''',unsafe_allow_html=True)
 
#             else:
#                 st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Certifications. It will show that you have done some specialization for the required position.</h4>''',unsafe_allow_html=True)

#             languages_pattern = re.compile(r'\blanguages\b|\blanguage\b', flags=re.IGNORECASE)    
#             if languages_pattern.search(resume_text):
#                 resume_score = resume_score + 6
#                 st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Languages </h4>''',unsafe_allow_html=True)
 
#             else:
#                 st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please Menation Languages you know. It will show that you have diffrent communication skills.</h4>''',unsafe_allow_html=True)
#             summary_objective_pattern = re.compile(r'\bSUMMARY\b|\bSummary\b|\bOBJECTIVES\b|\bObjectives\b|\bObjective\b', flags=re.IGNORECASE)
#             if summary_objective_pattern.search(resume_text):
#                 resume_score = resume_score + 3
#                 st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Summary/Objective</h4>''',unsafe_allow_html=True)
#             else:
#                 st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Summary/Objective. It will show your single word presentation to the comapny.</h4>''',unsafe_allow_html=True)
#             leadership_volunteer_pattern = re.compile(r'\bLEADERSHIP\b|\bLeadership\b|\bVOLUNTEER\b|\bVolunteer\b|\bVolunteers\b', flags=re.IGNORECASE)
#             if leadership_volunteer_pattern.search(resume_text):
#                 resume_score = resume_score + 6
#                 st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added your Summary/Objective</h4>''',unsafe_allow_html=True)
#             else:
#                 st.markdown('''<h5 style='text-align: left; color: #fabc10;'>[-] Please add Leadership/Volunteer. It will show your Leadership & Managnement skiils to the comapny.</h4>''',unsafe_allow_html=True)
#             st.subheader("**Resume Score 📝**")
                
#             st.markdown(
#                     """
#                     <style>
#                         .stProgress > div > div > div > div {
#                             background-color: #d73b5c;
#                         }
#                     </style>""",
#                     unsafe_allow_html=True,
#                 )

#                 ### Score Bar
#             my_bar = st.progress(0)
#             score = 0
#             for percent_complete in range(resume_score):
#                 score +=1
#                 time.sleep(0.03)
#                 my_bar.progress(percent_complete + 1)

     
#             st.success('** Your Resume Writing Score: ' + str(score)+'**')
#             st.warning("** Note: This score is calculated based on the content that you have added in your Resume. **")
#             ts = time.time()
#             cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
#             cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
#             timestamp = str(cur_date+'_'+cur_time)
            
#             insert_data(resume_data['name'],resume_data['email'],resume_data['mobile_number'],str(resume_score),
#                         str(cand_level),clf,str(resume_data['skills']),timestamp)
           
            
#             st.balloons()
            
            




import re
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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

###### Import Courses and  Database File ######

from Courses import*
from database import CreateTable,insert_data


###### Machine Learning Algortihm ######

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer


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
    st.subheader("\n\n**Courses & Certificates Recommendations 👨‍🎓**")
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
def NormalUser():
    internship_pattern = re.compile(r'\binternship(s)?\b', flags=re.IGNORECASE)
    experience_pattern = re.compile(r'\bexperience\b', flags=re.IGNORECASE)    
    pdf_file = st.file_uploader("Choose your Resume", type=['pdf'])
    
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
                st.header("\n\n** ------------ Resume Analysis ------------✉️ **\n")
                st.text("\n")
                st.success("\nHello "+ resume_data['name']+"\n")
                st.subheader("**Your Basic info 📋**")
                
                st.text('Name: '+resume_data['name'])
                st.text('Email: ' + resume_data['email'])
                st.text('Contact: ' + resume_data['mobile_number'])
                st.text('Skills: '+resume_data['skills'])
           #     print(resume_data['skills'])
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
                st.text('Year of Experience: ' + str(resume_data['total_experience']))
                st.text("Designition" + str(resume_data["designition"]))
            except:
                pass
                    
                  
                ## Predicting Candidate Experience Level 
                
            cand_level = ''
            if resume_data['no_of_pages'] < 1:                
                cand_level = "NA"
                st.markdown( '''<h4 style='text-align: left; color: #d73b5c;'>You are at Fresher level!</h4>''',unsafe_allow_html=True)
                
                #### if internship then intermediate level
                    
            elif internship_pattern.search(resume_text):
                cand_level = "Intermediate"
                st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''', unsafe_allow_html=True)

            # Check for work experience using regular expression
            
            elif experience_pattern.search(resume_text):
                cand_level = "Experienced"
                st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!</h4>''', unsafe_allow_html=True)
            
            else:
                cand_level = "Fresher"
                st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at Fresher level!!''',unsafe_allow_html=True)
                
         
                 ## Skills Analyzing and Recommendation
            st.subheader("**Skills Recommendation 📓**")

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
                    
                st.subheader("\n\nResume Videos Links ▶")
                for link in random_resume_links:
                    st.markdown(f'<br><iframe width="560" height="315" src="{link}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
                
                
                st.subheader("\n\nInterview Videos Links ▶")
                for link in random_interview_links:
                    st.markdown(f'<iframe width="560" height="315" src="{link}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
                
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
            st.subheader("\n\nResume Tips & Ideas  📝")
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
            st.subheader("**Resume Score 📝**")
                
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
            st.warning("** Note: This score is calculated based on the content that you have added in your Resume. **")
            ts = time.time()
            cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            timestamp = str(cur_date+'_'+cur_time)
            
            insert_data(resume_data['name'],resume_data['email'],resume_data['mobile_number'],str(resume_score),
                        str(cand_level),clf,str(resume_data['skills']),timestamp)
           
            
           # st.balloons()
            st.snow()
            
            

