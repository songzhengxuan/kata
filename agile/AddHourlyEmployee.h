#ifndef ADDHOURLYEMPLOYEE_H
#define ADDHOURLYEMPLOYEE_H

#include "AddEmployeeTransaction.h"

class AddHourlyEmployee : public AddEmployeeTransaction {
	public:
		virtual ~AddHourlyEmployee();
		AddHourlyEmployee(int empid, string name, string address, double salary);
		PaymentClassification* GetClassification() const;
		PaymentSchedule* GetSchedule() const;

	private:
		double itsSalary;
};

#endif
