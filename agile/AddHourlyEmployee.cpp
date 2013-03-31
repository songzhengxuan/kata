#include "AddHourlyEmployee.h"
#include "HourlyClassification.h"
#include "MonthlySchedule.h"

AddHourlyEmployee::~AddHourlyEmployee() {
}

AddHourlyEmployee::AddHourlyEmployee(int empid, string name,
		string address, double salary) 
: AddEmployeeTransaction(empid, name, address), itsSalary(salary) {
}

PaymentClassification* AddHourlyEmployee::GetClassification() const {
	return new HourlyClassification(itsSalary);
}

PaymentSchedule* AddHourlyEmployee::GetSchedule() const {
	return new MonthlySchedule();
}
