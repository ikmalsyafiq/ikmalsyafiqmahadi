import pandas as pd

allStudents = pd.read_csv(r'C:\Users\khair\ILMIA\6_student_output.csv')
allVacancies = pd.read_csv(r'C:\Users\khair\ILMIA\2_job_vacancy.csv')
                    
final = [] 
jobToStudentRatios = {}
laborDemand = {}
laborSupply = {}
salaries = {}
top5 = {} # by industry

### EXCLUDE UNUSED COLUMNS AND VALUES ###
allVacancies = allVacancies.drop(columns=['skills', 'job_types', 'job_level', 'masco1d_name', 'msic1d_name', 'msic5d_name'])
allVacancies = allVacancies[(allVacancies.edu_group != 'SPM/SPMV/MCE/O-Level') & (allVacancies.nec_desc != 'Not Specified Or Unable To Classify')]
allStudents = allStudents[(allStudents.certification_level != 'Matriculation / Foundation') & (allStudents.certification_level != 'Pra-Diploma') & (allStudents.nec3_desc != 'Not Specified Or Unable To Classify')]

### CLEAN AND IMPUTE MISSING VALUES ###

# convert all salary types to monthly
# assumes 8hr/day, 5day/week (or 40hr/week) and 52 week/year

allVacancies.loc[allVacancies.salary_type == 'Annually', 'max_salary'] = allVacancies[allVacancies.salary_type == 'Annually']['max_salary'].map(lambda a: round(a / 12))
allVacancies.loc[allVacancies.salary_type == 'Annually', 'max_salary'] = allVacancies[allVacancies.salary_type == 'Annually']['min_salary'].map(lambda a: round(a / 12))

allVacancies.loc[allVacancies.salary_type == 'Weekly', 'max_salary'] = allVacancies[allVacancies.salary_type == 'Weekly']['max_salary'].map(lambda a: round(a * 52 / 12))
allVacancies.loc[allVacancies.salary_type =='Weekly', 'max_salary'] = allVacancies[allVacancies.salary_type == 'Weekly']['min_salary'].map(lambda a: round(a * 52 / 12))

allVacancies.loc[allVacancies.salary_type  == 'Daily', 'max_salary'] = allVacancies[allVacancies.salary_type == 'Daily']['max_salary'].map(lambda a: round(a * 5 * 52 / 12))
allVacancies.loc[allVacancies.salary_type  == 'Daily', 'max_salary'] = allVacancies[allVacancies.salary_type == 'Daily']['min_salary'].map(lambda a: round(a * 5 * 52 / 12))

allVacancies.loc[allVacancies.salary_type  == 'Hourly', 'max_salary'] = allVacancies[allVacancies.salary_type == 'Hourly']['max_salary'].map(lambda a: round(a * 40 * 52 / 12))
allVacancies.loc[allVacancies.salary_type  == 'Hourly', 'max_salary'] = allVacancies[allVacancies.salary_type == 'Hourly']['min_salary'].map(lambda a: round(a * 40 * 52 / 12))

# refactor education group
allVacancies.loc[(allVacancies.edu_group == 'PMR/LCE/SRP') | (allVacancies.edu_group == 'SPM/SPMV/MCE/O-Level') | (allVacancies.edu_group == 'No Formal Education') | (allVacancies.edu_group == 'Primary Education'), 'edu_group']= 1
allVacancies.loc[(allVacancies.edu_group == 'Matriculation / Foundation') | (allVacancies.edu_group == 'STPM/STAM/HSC/A-Level'), 'edu_group']= 2
allVacancies.loc[(allVacancies.edu_group == 'Diploma') | (allVacancies.edu_group == 'Advanced Diploma'), 'edu_group']= 3
allVacancies.loc[(allVacancies.edu_group == 'Bachelor') | (allVacancies.edu_group == 'Graduate Diploma'), 'edu_group']= 4
allVacancies.loc[(allVacancies.edu_group == 'Master'), 'edu_group']= 5
allVacancies.loc[(allVacancies.edu_group == 'Ph.D'), 'edu_group']= 6
allVacancies.loc[(allVacancies.edu_group == 'Certificate') | (allVacancies.edu_group == 'Skills Certificate'), 'edu_group']= 0
allVacancies['edu_group'] = allVacancies['edu_group'].fillna(-1) # include in all job:student ratio regardless of degree level

# refactor cert levels
allStudents.loc[(allStudents.certification_level == 'Matriculation / Foundation') | (allStudents.certification_level == 'Pra-Diploma'),'certification_level']= 2
allStudents.loc[(allStudents.certification_level == 'Advanced Diploma') | (allStudents.certification_level == 'Diploma'),'certification_level']= 3
allStudents.loc[(allStudents.certification_level == 'Bachelor') | (allStudents.certification_level == 'Postgraduate Diploma') | (allStudents.certification_level == 'Professional'),'certification_level']= 4
allStudents.loc[(allStudents.certification_level == 'Master'),'certification_level']= 5
allStudents.loc[(allStudents.certification_level == 'Ph.D') | (allStudents.certification_level == 'Others'),'certification_level']= 6
allStudents.loc[(allStudents.certification_level == 'Certificate'),'certification_level']= 0

### MATCH STUDENTS TO JOB VACANCIES ###

# get unique list of jobs from both datasets based on nec_desc (merging factor)
jobVacancies = allVacancies.nec_desc.unique()
studentOutput = allStudents.nec3_desc.unique()

matches = set(jobVacancies) & set(studentOutput)