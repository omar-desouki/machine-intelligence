from typing import Any, Dict, List, Optional
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint
from helpers.utils import NotImplemented

# This function applies 1-Consistency to the problem.
# In other words, it modifies the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints are removed from the problem (they are no longer needed).
# The function returns False if any domain becomes empty. Otherwise, it returns True.
def one_consistency(problem: Problem) -> bool:
    remaining_constraints = []
    solvable = True
    for constraint in problem.constraints:
        if not isinstance(constraint, UnaryConstraint):
            remaining_constraints.append(constraint)
            continue
        variable = constraint.variable
        new_domain = {value for value in problem.domains[variable] if constraint.condition(value)}
        if not new_domain:
            solvable = False
        problem.domains[variable] = new_domain
    problem.constraints = remaining_constraints
    return solvable

# This function returns the variable that should be picked based on the MRV heuristic.
# NOTE: We don't use the domains inside the problem, we use the ones given by the "domains" argument 
#       since they contain the current domains of unassigned variables only.
# NOTE: If multiple variables have the same priority given the MRV heuristic, 
#       we order them in the same order in which they appear in "problem.variables".
def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:
    _, _, variable = min((len(domains[variable]), index, variable) for index, variable in enumerate(problem.variables) if variable in domains)
    return variable



# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned values
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def forward_checking(problem: Problem, assigned_variable: str, assigned_value: Any, domains: Dict[str, set]) -> bool:
    
    for constraint in problem.constraints:  # haloop 3la kol el constraints ely fe el ms2la

        if assigned_variable in  constraint.variables: # hadkhol el if condition lw el variable dah 3ando constraint m3 variable tany
            other_variable = constraint.get_other(assigned_variable) # get the other involved variable in the binary constraint

            if other_variable not in domains: # lw el variable el tany et3mlo assign
                continue #yro7 lel iteration ely b3daha

            other_var_domain = domains[other_variable].copy() #3shan maynf3sh aedit we ana baloop 3aleh fa basevo fe variable tany

            for domain_of_other_variable in other_var_domain: #haloop 3la kol element fe el domain bta3 kol unassigned variable
                assignment = {assigned_variable: assigned_value, other_variable: domain_of_other_variable} # el assignment ely h3mlha 3shan a3rf lw fe moshkela fe el assignment dah m3 el constraint

                if not constraint.is_satisfied(assignment): #lw el assignment msh btsfyy el constraint
                    domains[other_variable].remove(domain_of_other_variable) #remove the value from the domain of the other variable
                    
                    if not domains[other_variable]: #check 3shan lw el domain fdy
                        return False
                    
    #problem.domains = domains #update the domains in the problem
    return True
        



# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neigbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic, 
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def least_restraining_values(problem: Problem, variable_to_assign: str, domains: Dict[str, set]) -> List[Any]:

    assigned_var_domain = domains[variable_to_assign].copy()
    count_dict : dict = {}
    
    for domain_of_assigned_var in assigned_var_domain: #baloop 3la kol el possible values
        value = 0
        var = domain_of_assigned_var

        for constraint in problem.constraints:  # haloop 3la kol el constraints ely fe el ms2la


            if variable_to_assign in  constraint.variables: # hadkhol el if condition lw el variable dah 3ando constraint m3 variable tany

                other_variable = constraint.get_other(variable_to_assign) # get the other involved variable in the binary constraint
                other_var_domain = domains[other_variable].copy() #3shan maynf3sh aedit we ana baloop 3aleh fa basevo fe variable tany

                for domain_of_other_variable in other_var_domain: #haloop 3la kol element fe el domain bta3 kol unassigned variable

                    assignment = {variable_to_assign: domain_of_assigned_var, other_variable: domain_of_other_variable} # el assignment ely h3mlha 3shan a3rf lw fe moshkela fe el assignment dah m3 el constraint

                    if constraint.is_satisfied(assignment): #lw el assignment bysatisfy el constraint
                        value += 1 #increase the count of the value by 1    

                count_dict[var] = value #b3mel dict feha kol value lel assigned vaiable we ba3mel count lel number of values ely tnf3 mn el domains el tanya
    
    #byakhod el dict we byrato 3la hasab el count we byhot el values fe list bel tarteb dah
    count_list = sorted(count_dict, key=lambda k: (count_dict[k], -k) , reverse= True)#reverse = true 3shan yrtbhom DESC we -k 3shan lw etnen variables have the same values byratbhom asc

    return count_list

# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
# Unary constraints should be handled using 1-Consistency before starting the backtracking search.
# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.
# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#            Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.
def solve(problem: Problem) -> Optional[Assignment]:
    #TODO: Write this function

    #bnkhtar el var 3la hasab el MRV 
    #byoreder el values bta3to 3la hasab el list ely hatrg3lo mn (least_restraining_values) fn
    #e3mel handle lel 1-consistency before starting

    testcount = 0

    if not one_consistency(problem): #3shan a3mel 1-consistency abl ma astart el backtracking lw be false yb2a mafesh solution
        #print("none1")
        return None
    
    domain = problem.domains
    var_to_assign = minimum_remaining_values(problem,domain) #bageb el var ely el mafrod a3mlo assign 3n tare2 el mrv
    least_res_val = least_restraining_values(problem,var_to_assign,domain) #bageb el list lleast restraining order lel var dah be el tarteb
    assig : Assignment =  {}    #initializing the assignment
    count = len(least_res_val) #basave el count le awel element 3shan a3rf lw mafesh hal khlas

    #noskhten mn el domain 3shan fe el mrv mhtag ashel ely et3mlo assign we fe el least restraining value mhtag asebo 
    domain_mrv = domain.copy()
    domain_least = domain.copy()

    #3shan a3rf a3mel backtrack
    var_list = [] 
    least_list = [] 
    count_list = []
    domain_mrv_list = []
    domain_least_list = []

    #initializing the lists
    var_list.append(var_to_assign)
    least_list.append(least_res_val)
    count_list.append(count)
    domain_mrv_list.append(domain)
    domain_least_list.append(domain)

#####7,8

    if problem.is_complete(assig):#kol mara batcheck lw ana khlst wala la2
        return assig

    while True:

        for least in least_res_val:#haloop 3ala el least restraining variable be el tarteb

            assig[var_to_assign] = least #assign the least restraining value to the variable        
            
            if forward_checking(problem,var_to_assign,least,domain):#lw nf3 yb2a emsek var tany we nloop 3aleh nafs el loop we nzwed el assignment

                if problem.is_complete(assig):#kol mara batcheck lw ana khlst wala la2
                    return assig
                
                del domain_mrv [var_to_assign] #removo mn el domain khales 3shan el mrv y3rf ykhtar 8ero
                domain_least [var_to_assign] = {least} #bassign el element fe el domain / {} 3shan lazem set

                #setting the new values
                var_to_assign = minimum_remaining_values(problem,domain_mrv) #bageb el var ely el mafrod a3mlo assign 3n tare2 el mrv
                least_res_val = least_restraining_values(problem,var_to_assign,domain_least) #bageb el list lleast restraining order lel var dah be el tarteb
                count = len(least_res_val) #basave el count le awel element 3shan a3rf lw mafesh hal khlas

                #saving the new values
                var_list.append(var_to_assign)
                least_list.append(least_res_val)
                count_list.append(count)
                domain_mrv_list.append(domain_mrv)
                domain_least_list.append(domain_least)

                break #3shan a3ed el loop tany
            
            else:#lw el 3add ely fe el least_res_val manf3osh yb2a nbacktrack

                count -= 1 #decrease the count by 1 lhad ma ywsl zero fa dah m3nah eny lafet 3al values kolha we mafesh solution

                if count == 0: #nback-track

                    del assig[var_to_assign] #hashel el assign. ely kont 3mltholo

                    if len(assig) == 0: #3shan lw el assignment fady we el count == 0  yb2a mafesh solution
                        #print("none2")
                        return None
                    
                    #shelt el variables el adema
                    var_list.pop()
                    least_list.pop()
                    count_list.pop()
                    domain_mrv_list.pop()
                    domain_least_list.pop()

                    if(len(var_list) == 0): #lw el list fady yb2a mafesh solution / azon malosh lazma 3hsan el if ely fo2eh
                        #print("none3")
                        return None

                    #restoring the old values / lma shelt akher elemnet b2a akher element hwa ely elmafrod a3mlo backtrack
                    var_to_assign = var_list[-1] #-1 3shan ageb el last element
                    least_res_val = least_list[-1]
                    count = count_list[-1]
                    domain_mrv = domain_mrv_list[-1]
                    domain_least = domain_least_list[-1]

                    break #3shan a3ed el loop tany


#notes

# one_consistency fn 3shan el unary constraints

# minimum_remaining_values fn 3shan tgeb el MRV heuristic
