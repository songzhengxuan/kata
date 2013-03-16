#include "PayrollDatabase.h"
#include "Employee.h"

PayrollDatabase GPayrollDatabase;

PayrollDatabase::~PayrollDatabase() {
}

Employee* PayrollDatabase::GetEmployee(int empid) {
	return itsEmployees[empid];
}

void PayrollDatabase::AddEmployee(int empid, Employee* e) {
	itsEmployees[empid] = e;
}


