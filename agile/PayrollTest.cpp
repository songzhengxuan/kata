#include "Employee.h"
#include "PayrollDatabase.h"
#include "AddSalariedEmployee.h"
#include <gtest/gtest.h>

TEST(PayRollTest, TestAddSalariedEmployee) {
	int empId = 1;
	AddSalariedEmployee t(empId, "Bob", "Home", 1000.00);
	t.Execute();
	
	Employee* e = GPayrollDatabase.GetEmployee(empId);
	ASSERT_TRUE("Bob" == e->GetName());
}
