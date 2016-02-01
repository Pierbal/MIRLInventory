#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <vector>
#include <ctime>

/*
CONSUMABLES
These are things that we dont care about if a person uses them. We only ask that they let us know
how many they have used so that we can get more.
*/

struct checkoutHistoryInfo_consumable{
	int MUID;
	std::string name;
	time_t date;
};

class Consumable{
	std::string number;
	std::string name;
	std::string location;
	double price;
	std::vector<struct checkoutHistoryInfo_consumable> checkoutHistory;
	std::string refillURL;
	long quantity;

	Consumable(std::string number); //loads basic info from the file Tools/number.info
}
