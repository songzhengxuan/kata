#ifndef SALARIEDCLASSIFICATION_H
#define SALARIEDCLASSIFICATION_H
#include "PaymentClassification.h"
class SalariedClassification : public PaymentClassification {
	public:
		~SalariedClassification() {}
		SalariedClassification(double itsSalary);

	private:
		double Salary;
};
#endif
