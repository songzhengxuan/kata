#ifndef COMMISSIONEDCLASSIFICATION_H 
#define COMMISSIONEDCLASSIFICATION_H 
#include "PaymentClassification.h"
class CommissionedClassification : public PaymentClassification {
	public:
		~CommissionedClassification() {}

	private:
		double CommissionRate;
		double Salary;
};
#endif
