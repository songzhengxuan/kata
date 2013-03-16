#ifndef BIWEEKLYSCHEDULE_H
#define BIWEEKLYSCHEDULE_H
#include "PaymentSchedule.h"
class BiweeklySchedule : public PaymentSchedule {
	public:
		~BiweeklySchedule() {}
		bool isPayday(long day);
};

#endif
