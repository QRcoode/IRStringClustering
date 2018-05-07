const gplay = require("google-play-scraper");
const reviews_file_name = "reviews.txt";
const appID = "com.fsck.k9";
const fs = require('fs');
const writter = fs.createWriteStream("../files/" + reviews_file_name); // will save in the current directory

for (let i = 0; i <= 111; i++) {
	Promise.resolve(gplay.reviews({
		appId: appID, //change this to change the app
		throttle: 10, //this limits the number of requests to the Google Play Store (e.g. 10 = 10 requests per second). 10 may be too high if you're planning to do >111 pages.
		page: i,
		sort: gplay.sort.HELPFULNESS //can be HELPFULNESS, NEWEST, OR RATING
	})
	).then(value => {
		for (let j = 0; j < Object.keys(value).length; j++) {
			writter.write(value[j].text + '\r\n'); //value[j].<INSERT TAG> to change what you get from the JSON
		}
	}
	).catch(error => console.log(error));
}