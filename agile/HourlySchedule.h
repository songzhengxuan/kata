#ifndef HOURLYSCHEDULE_H
#define HOURLYSCHEDULE_H
#include "PaymentSchedule.h"
class HourlySchedule : public PaymentSchedule {
	public:
		~HourlySchedule() {}
		bool isPayday(long day);
};

#endif
