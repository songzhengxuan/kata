#ifndef HOURLYCLASSIFICATION_H
#define HOURLYCLASSIFICATION_H
#include "PaymentClassification.h"
class HourlyClassification : public PaymentClassification {
	public:
		HourlyClassification(double rate);
		~HourlyClassification() {}
		double GetSalary() const;
	private:
		double HourlyRate;
};

#endif

