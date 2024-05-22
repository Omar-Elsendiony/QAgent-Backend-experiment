class CovergaeResults:
    """A class to wrap the coverage results."""
     # default is true, if no branch exists, it will be set to false
    def __init__(self, time_consumed_minutes: int, count_offspring_generated:int):
        """Constructor that sets the time consumed during the algorithm run and the count of offsprings generated."""
        self.time_consumed_min = time_consumed_minutes
        self.count_offspring_generated=count_offspring_generated
        self.targets_best_solutions_dict = {}
        self.contains_branches=0
        self.count_covered_targets=0
        self.all_targets_count=0
        self.branch_coverage_percent=0
        self.is_branch_exists=True
    
    def set_statistics(self, branch_cov_percent, count_covered_targets, all_targets_count):
        """Sets the final coverage statistics about the module under test."""
        self.branch_coverage_percent = branch_cov_percent
        self.count_covered_targets = count_covered_targets
        self.all_targets_count = all_targets_count  
    
    def add_target_sol_pair(self,target_tuple,best_test_case):
        """Adds a taregt and its best solution (best test case that covers this target)."""
        self.targets_best_solutions_dict[f"({target_tuple[0]},{target_tuple[1]})"]=best_test_case
    
    def set_is_branch_exists(self,is_branch_exists):
        """Sets if any branch exists in the module under test."""
        self.is_branch_exists = is_branch_exists

    def get_is_branch_exists(self):
        """Returns if any branch exists in the module under test."""
        return self.is_branch_exists