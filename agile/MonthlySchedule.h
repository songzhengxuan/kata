#ifndef MONTHLYSCHEDULE_H
#define MONTHLYSCHEDULE_H
#include "PaymentSchedule.h"
class MonthlySchedule : public PaymentSchedule {
	public:
		~MonthlySchedule() {}
		bool isPayday(long day);
};

#endif
