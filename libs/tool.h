#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include <ctime>

/*
TOOLS
These are non-consumable items that can be checked out to a person.
They have due dates and a price.
*/

struct checkoutHistoryInfo_tool{
	int MUID;
	std::string name;
	time_t startDate;
	time_t endDate;
	time_t returnDate;
};

class Tool{
	std::string number;
	std::string name;
	std::string location;
	bool checkedOut; //weither someone has checked it out
	double price;
	std::vector<struct checkoutHistoryInfo_tool> checkoutHistory;

	Tool(std::string number); //loads basic info from the file Tools/number.info
}
