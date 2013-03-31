#include "Employee.h"
#include "PayrollDatabase.h"
#include "AddSalariedEmployee.h"
#include "AddHourlyEmployee.h"
#include "AddCommissionedEmployee.h"
#include "DeleteEmployeeTransaction.h"
#include "SalariedClassification.h"
#include "HourlyClassification.h"
#include "MonthlySchedule.h"
#include "HoldMethod.h"
#include <gtest/gtest.h>

// checked, source code 19.2 on page 184
TEST(PayRollTest, TestAddSalariedEmployee) {
	int empId = 1;
	AddSalariedEmployee t(empId, "Bob", "Home", 1000.00);
	t.Execute();
	
	Employee* e = GPayrollDatabase.GetEmployee(empId);
	ASSERT_TRUE("Bob" == e->GetName());

	PaymentClassification* pc = e->GetClassification();
	SalariedClassification* sc = dynamic_cast<SalariedClassification*>(pc);
	ASSERT_TRUE(sc != NULL);

	ASSERT_NEAR(1000.00, sc->GetSalary(), 0.001);
	PaymentSchedule* ps = e->GetSchedule();
	MonthlySchedule* ms = dynamic_cast<MonthlySchedule*>(ps);
	ASSERT_TRUE(ms != NULL);
	PaymentMethod* pm = e->GetMethod();
	HoldMethod* hm = dynamic_cast<HoldMethod*>(pm);
	ASSERT_TRUE(hm != NULL);
}

TEST(PayRollTest, TestAddHourlyEmployee) {
	int empId = 2;
	AddHourlyEmployee t(empId, "Sam", "Home", 25.00);
	t.Execute();
	
	Employee* e = GPayrollDatabase.GetEmployee(empId);
	ASSERT_TRUE("Sam" == e->GetName());

	PaymentClassification* pc = e->GetClassification();
	HourlyClassification* sc = dynamic_cast<HourlyClassification *>(pc);
	ASSERT_TRUE(sc != NULL);

	ASSERT_NEAR(25.00, sc->GetSalary(), 0.001);
}

TEST(PayRollTest, TestDeleteEmployee) {
	int empId = 3;
	AddCommissionedEmployee t(empId, "Lance", "Home", 2500, 3.2);
	t.Execute();
	{
		Employee* e = GPayrollDatabase.GetEmployee(empId);
		assert(e);
	}
	DeleteEmployeeTransaction dt(empId);
	dt.Execute();
	{
		Employee* e = GPayrollDatabase.GetEmployee(empId);
		assert(e == NULL);
	}
}
