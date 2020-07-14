### INITIALIZE JOB CLASS OBJECT ###
class Job:
        def __init__(self, name, companies, students):
                self.name = name
                self.companies = companies
                self.students = students
                self.courses = self.getCourses()
                        
        def getCourses(self):
            # categorize courses together based on degree level
            courses = {}
            levels = self.students.groupby(['certification_level'])

            for l in levels.groups.keys():
                if l == 0: courses['Certificate'] = l
                elif l == 2: courses['Matriculation/Foundation/Pre-Diploma'] = l
                elif l == 3: courses['Diploma/Advanced Diploma'] = l
                elif l == 4: courses['Bachelor/Postgraduate Diploma/Professional'] = l
                elif l == 5: courses['Master'] = l
                elif l == 6: courses['PhD/Doctorate'] = l
            
            return courses

        def getDegreeLevel(self, c):
                return self.courses[c]

        def checkYearExists(self, year, students=False):
                if students:
                        years = [i for i in self.students.year.unique()]
                else:
                        years = [i for i in self.companies.year.unique()]

                if year in years:
                        return True
                return False
       
        def jobsForYear(self, year, c=None):
                if self.checkYearExists(year):
                        if c is not None:
                                # find course degree level
                                level = self.getDegreeLevel(c)
                                
                                # only count jobs that require at least degree level
                                return int(self.companies[(self.companies.year == year) & (self.companies.edu_group <= level)]['job_count'].sum())
                        else:
                                return int(self.companies[self.companies.year == year]['job_count'].sum()) # count all jobs in the industry for the year
                else: return 0

        def studentsForYear(self, year, c=None):
                if self.checkYearExists(year, True):
                        if c is not None:
                                level = self.getDegreeLevel(c)

                                # only count students with the same, or higher, degree level
                                return len(self.students[(self.students.year == year) & (self.students.certification_level >= level)])
                        else:
                                return len(self.students[self.students.year == year]) # count all students in the industry for the year
                else: return 0
        
        def jobToStudentRatio(self, year):
                jobs = self.jobsForYear(year)
                students = self.studentsForYear(year)

                if jobs == -1 or students == -1:
                        return -1
                else:
                        return round(jobs / students, 4)                

        def genderCount(self, year, c, male=False):
                if self.checkYearExists(year, True):
                        # only count students with similar degree qualification
                        level = self.getDegreeLevel(c)
                        subStudents = self.students[(self.students.year == year) & (self.students.certification_level == level)]
                        if male:
                                return len(subStudents[subStudents.gender == 'Male'])
                        else:
                                return len(subStudents[subStudents.gender == 'Female']) 
                else: return 0      

        def averageSalary(self, year, min=True):
                # exclude jobs with no salary declared from calculations
                if self.checkYearExists(year):
                        if min:
                                return int(self.companies[(self.companies.year == year) & (self.companies.min_salary.notnull())]['min_salary'].mean())
                        else:
                                return int(self.companies[(self.companies.year == year) & (self.companies.max_salary.notnull())]['max_salary'].mean())
                else: return -1

        def getLinkedIn(self):
            split = self.name.split(" ")
            path = '%20'.join(split)
            return 'https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22my%3A0%22%5D&keywords=' + path + '&origin=GLOBAL_SEARCH_HEADER'

        def getJobStreet(self):
            split = self.name.split(" ")
            path = '+'.join(split)
            return 'https://www.jobstreet.com.my/en/job-search/job-vacancy.php?ojs=10&key=' + path