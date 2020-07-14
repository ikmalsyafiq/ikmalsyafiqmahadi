import pandas as pd
import json
import job
import ilmia

i = 0
for k in sorted(list(ilmia.matches)):
        vacanciesForThisJob = ilmia.allVacancies[ilmia.allVacancies.nec_desc == k]
        studentsForThisJob = ilmia.allStudents[ilmia.allStudents.nec3_desc == k]
        j = job.Job(k, vacanciesForThisJob, studentsForThisJob)
        
        temp = {}
        courses = {}
        temp['id'] = i
        temp['name'] = k
        temp['linkedin'] = j.getLinkedIn()
        temp['jobstreet'] = j.getJobStreet()
        temp['courses'] = []

        for c in j.courses:
                course = {}
                course['name'] = c
                for year in ilmia.allVacancies.year.unique():
                        course[str(year)] = {
                                'numOfJobs': j.jobsForYear(year, c),
                                'numOfStudents': j.studentsForYear(year, c),
                                'maleCount': j.genderCount(year, c, True),
                                'femaleCount': j.genderCount(year, c),
                                'aveMinSalary': j.averageSalary(year),
                                'aveMaxSalary': j.averageSalary(year,False)
                        }
                temp['courses'].append(course)
        
        # compute industry-wide stats
        ratio = j.jobToStudentRatio(2018)
        if ratio != -1: ilmia.jobToStudentRatios[k] = ratio
        
        demand = j.jobsForYear(2018)
        if demand != -1: ilmia.laborDemand[k] = demand

        supply = j.studentsForYear(2018)
        if supply != -1: ilmia.laborSupply[k] = supply   

        maxSalary = j.averageSalary(2018, False) 
        if maxSalary != -1: ilmia.salaries[k] = maxSalary

        ilmia.final.append(temp)
        i = i + 1

# extract data for top5 stats
r = sorted(ilmia.jobToStudentRatios.items(), key=lambda x: x[1], reverse=True)  
ilmia.top5['jobToStudent'] = [i[0] for i in r[:5]]

d = sorted(ilmia.laborDemand.items(), key=lambda x: x[1], reverse=True)  
ilmia.top5['laborDemand'] = [i[0] for i in d[:5]]

s = sorted(ilmia.laborSupply.items(), key=lambda x: x[1], reverse=True)  
ilmia.top5['laborSupply'] = [i[0] for i in s[:5]]

salary = {}
slry = sorted(ilmia.salaries.items(), key=lambda x: x[1], reverse=True)  
for i in slry[:5]:
        salary[i[0]] = i[1]
ilmia.top5['salary'] = salary

with open('data.json', 'w') as f:
        json.dump(ilmia.final, f)

with open('top5.json', 'w') as t:
        json.dump(ilmia.top5, t)