#include "AddCommissionedEmployee.h"
AddCommissionedEmployee::AddCommissionedEmployee(int empid, string name, string address, double salary, double rate) : AddEmployeeTransaction(empid, name, address) {
	Salary = salary;
	Rate = rate;
}

PaymentClassification* AddCommissionedEmployee::GetClassification() const {
	return NULL;
}

PaymentSchedule* AddCommissionedEmployee::GetSchedule() const {
	return NULL;
}

