#ifndef WEEKLYSCHEDULE_H
#define WEEKLYSCHEDULE_H
#include "PaymentSchedule.h"
class WeeklySchedule : public PaymentSchedule {
	public:
		~WeeklySchedule() {}
		bool isPayday(long day);
};

#endif
