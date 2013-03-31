#include "HourlyClassification.h"
HourlyClassification::HourlyClassification(double rate) {
	HourlyRate = rate;
}

double HourlyClassification::GetSalary() const {
	return HourlyRate;
}
