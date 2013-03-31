#ifndef ADDCOMMISSIONEDEMPLOYEETRANSACTION_H
#define ADDCOMMISSIONEDEMPLOYEETRANSACTION_H

#include "AddEmployeeTransaction.h"
class AddCommissionedEmployee : public AddEmployeeTransaction {
	public:
		AddCommissionedEmployee(int empid, string name, string address, double salary, double rate);
		PaymentClassification* GetClassification() const;
		PaymentSchedule* GetSchedule() const;
	private:
		double Salary;
		double Rate;
};

#endif
