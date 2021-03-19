import csv 

#First, let's open up the CSV file and store it in a list.
with open('insurance.csv','r') as Insurance_file:
    csv_file = csv.reader(Insurance_file, delimiter = ",")
    person = []
    for row in csv_file:
        person.append(row)

#Then, let's remove the irrelevent title by slicing it out
neo_person = person[1:]

#Next, I want to start isolating different features that are similer between different people. If we can find two people that
#are identical in every way EXCEPT for one factor, we can use the difference between the two to figure out a formula for cost.

#The formula will be, at least based on what I've read online:
# Charges = (U * age) + (V * sex) + (W * bmi) + (X * children) + (Y * smoker) + (Z * region)
# Where age, children are values, sex and smoker are probably binary, and region is more complex but likely each region represents a value

#Since BMI is float, this seems like the obvious first choice to focus on solving. Let's simplify the loop it by combining all the raw data.

merged_ex_bmi = []

for indi in neo_person:
    merged_ex_bmi.append(str(indi[0]) + str(indi[1]) + str(indi[3]) + str(indi[4]) + str(indi[5]))

# print(len(merged_ex_bmi))

#Now that we've merged our data, let's find the index for two matching values. Since I'll use this feature multiple times, it makes
#sense to write it as a function.

def identify_matched_indexes(merged_data):
    #i will act as an index reference for the first matched pair.
    i = -1
    fudge_list = list(merged_data)

    while len(fudge_list) > 0:

        #The index reference for the 2nd value will be j + i
        j = 1
        #So for this iteration, i = 0, then 1, then 2...
        i += 1

        test_value = fudge_list.pop(0)

        for val in fudge_list:
            if test_value == val:
                #This following is to account for instances where two people are identical!
                # if neo_person[ref_val1][:-1] == neo_person[ref_val2][:-1]:
                #     pass
                # else:
                #     return [i, (j + i)]
                return [i, (j + i)]
            else:
                j += 1
    
    return "No duplicates found."

ref_val1, ref_val2 = identify_matched_indexes(merged_ex_bmi)

#Now we have our two identical values, we can finally isolate the the change in cost by accounting for change in BMI.
#The formula for that is: (CostA - CostB)/(bmiA - bmiB). We will write a formula for this that only works if only one metric
#needs analysed.

def metric_identifier(ref1, ref2, list_item):
    return (( float(neo_person[ref_val1][-1]) - float(neo_person[ref_val2][-1]) )/( float(neo_person[ref_val1][list_item]) - float(neo_person[ref_val2][list_item]) ))

W_bmi = metric_identifier(ref_val1, ref_val2, 2)

# Charges = (U * age) + (V * sex) + (490.39 * bmi) + (X * children) + (Y * smoker) + (Z * region)

#Now we just repeat this exercise, for age, children, sex, smoker, region

merged_ex_age = []

for indi in neo_person:
    merged_ex_age.append(str(indi[1]) + str(indi[2]) + str(indi[3]) + str(indi[4]) + str(indi[5]))

ref_val1, ref_val2 = identify_matched_indexes(merged_ex_age)

U_age = metric_identifier(ref_val1, ref_val2, 0)

# Charges = (285.855 * age) + (V * sex) + (490.39 * bmi) + (X * children) + (Y * smoker) + (Z * region)

merged_ex_children = []

for indi in neo_person:
    merged_ex_children.append(str(indi[0]) + str(indi[1]) + str(indi[2]) + str(indi[4]) + str(indi[5]))

ref_val1, ref_val2 = identify_matched_indexes(merged_ex_children)

#So this has hit us on a very unusual occurence! Apparently there are people who are identical in the metrics given
#But are charged different rates! Consider the following people:

# print(ref_val1, ref_val2)
# print(neo_person[ref_val1], neo_person[ref_val2])
# print(neo_person[102], neo_person[471])

#We can therefore conclude one of three things:
#1) The data is unclean. (i.e. cost is randomly generated...)
#2) The cost data is not related to the other metrics (absurd).
#3) There is a "hidden" metric that we aren't told.

#I suspect it's 1 but let's be charitable and say it's 3. Lets test our hypothesis by making a slightly altered version of the original formula:


def identify_multiple_matched_indexes(merged_data):
    i = -1
    fudge_list = list(merged_data)
    all_similer_people = []

    while len(fudge_list) > 0:

        j = 1
        i += 1

        test_value = fudge_list.pop(0)

        for val in fudge_list:
            if test_value == val:
                # This time, capture lots of information of matched people
                all_similer_people.append(i)
                all_similer_people.append(j + i)
            else:
                j += 1
    
    return all_similer_people

checker = identify_multiple_matched_indexes(merged_ex_bmi)

# print(( float(checker[0][-1]) - float(checker[1][-1]) )/( float(checker[0][2]) - float(checker[1][2]) ))
# print(checker[0], checker[1])
# print(( float(checker[5][-1]) - float(checker[4][-1]) )/( float(checker[5][2]) - float(checker[4][2]) ))
# print(checker[5], checker[6])

#This blows it right open, clearly there is some other metric that impacts the cost, because...
#1) There are people who are exactly the same, who are have the same cost. eg.
# print(neo_person[195], neo_person[581])
# But there are others who are the same but have different costs.
# print(neo_person[102], neo_person[471])
#2) Conversely, there are people who are the same in every way except one, but the multiplication factor is inconsistent between them.

# !!! CONCLUSION: There is either a hidden metric OR there is some discrimintory practise going on here OR there are mistakes. Either way, this
# is a serious issue that requires investigation outside the scope of this project.

#With that being the case, it will now be a good idea to do some more general analysis. Let's see what our sample size looks like and find some
#averages. Then, it might be worth seeing what attributes are correlated with higher costs.

age_metric = [] #0
sex_metric = [] #1
bmi_metric = [] #2
children_metric = [] #3
smoker_metric = [] #4
geo_metric = [] #5
cost_metric = [] #6

for values in neo_person:
    age_metric.append(int(values[0]))
    sex_metric.append(values[1])
    bmi_metric.append(float(values[2]))
    children_metric.append(int(values[3]))
    smoker_metric.append(values[4])
    geo_metric.append(values[5])
    cost_metric.append(float(values[6]))

average_age = sum(age_metric)/len(age_metric) #39.20
average_sex = (sex_metric.count("male")/len(sex_metric)) #Male, 50.5%
average_bmi = sum(bmi_metric)/len(bmi_metric) #30.66
average_children = sum(children_metric)/len(children_metric) #1.095
average_smoker = (smoker_metric.count("yes")/len(smoker_metric)) #0.2048
geo_loc1 = (geo_metric.count("northwest")/len(geo_metric)) #0.243
geo_loc2 = (geo_metric.count("northeast")/len(geo_metric)) #0.242
geo_loc3 = (geo_metric.count("southeast")/len(geo_metric)) #0.272
geo_loc4 = (geo_metric.count("southwest")/len(geo_metric)) #0.243
average_cost = sum(cost_metric)/len(cost_metric) #13270

# print(f"Our archetypal medical insurance customer is a {round(average_age)} year old male with a BMI of {round(average_bmi)}, who has \
# {round(average_children)} child, is a non-smoker, can be found in the southeast region and pays ${round(average_cost)} in insurance costs.")

#Let's play around with some other data. First create a variable that can parse out the qualitative data.

def metric_explorer(list_of_data, value_to_search, metric_to_check):
    val1 = 0
    val2 = 0
    i = 0
    j = 0

    for value in list_of_data:
        if value[metric_to_check] == value_to_search:
            i += 1
            val1 += float(value[6]) #cost
        else:
            j += 1
            val2 += float(value[6]) #cost     

    return val1/i, val2/j     

#Impact of smoking on cost
smoker_val, non_smoker_val = metric_explorer(neo_person, "yes", 4)

# print(smoker_val/non_smoker_val)

#A smoker can expect to pay 3.8 times as much as a non-smoker, accounting for confounding variables like age, bmi, etc., which are beyond the
#scope of this project.

male_val, female_smoker_val = metric_explorer(neo_person, "male", 1)

# print(male_val/female_smoker_val)

#A male can expect to pay 1.1 times as much as a female, accounting for confounding variables like age, bmi, etc., which are beyond the
#scope of this project.

nw_val, fudge = metric_explorer(neo_person, "northwest", 5)
ne_val, fudge = metric_explorer(neo_person, "northeast", 5)
se_val, fudge = metric_explorer(neo_person, "southeast", 5)
sw_val, fudge = metric_explorer(neo_person, "southwest", 5)

# print(nw_val, ne_val, se_val, se_val)
# print(se_val/nw_val)

#Those in the south will spend more than those in the north. For example, someone in the SE will be charged on average 18% more than someone in
#the NW. Interestingly, the SE and SW are changed the same on average.

#Finally, let's look at what happens when you have at least one child.

childless_val, children_val = metric_explorer(neo_person, '0', 3)

# print(childless_val/children_val)

#Those witout children spend less than those with, 0.88 of to be exact.

#I think we more or less get the idea of what this analysis has accomplished, let me round it off by making a class for practise.

class Person: #Define a new class of person to add to the list

    def __init__(self, age, sex, bmi, children, smoker, geo, cost):
        self.age = age
        self.sex = sex
        self.bmi = bmi
        self.children = children
        self.smoker = smoker
        self.geo = geo
        self.cost = cost

    def suggest_cost(self):
        i = 0
        if self.age > average_age:
            i += 1

        if self.sex == "male":
            i += 1
    
        if self.bmi > average_bmi:
            i += 1
    
        if self.children > average_children:
            i += 1
    
        if self.smoker == "yes":
            i += 1
    
        if self.geo[0:5] == "south":
            i += 1
    
        if i == 6:
            return "You will likely be charged well above the average rate on average."
        elif i > 3:
            return "You will likely be charged a fairly high rate compared to the average."
        elif i > 0:
            return "You will likely be charged a fairly moderate rate compared to the average."
        else:
            return "You likely will not be chaged much at all compared to the average!"

Steingar = Person(25, "male", 22.1, 0, "no", "southeast", 1500.2)
Tracy = Person(26, "female", 24.3, 0, "no", "northeast", 1700)
Sam = Person(31, "male", 32.6, 2, "yes", "southwest", 1500)

print(Steingar.suggest_cost())
print(Tracy.suggest_cost())
print(Sam.suggest_cost())